from tiyaro.sdk.base_handler import TiyaroBase
from marshmallow import fields

from models.network_swinir import SwinIR as net
import torch
import numpy as np
import base64
import cv2

class TiyaroHandler(TiyaroBase):
    # Kindly donot change the name of the class

    # Declaring a Schema is Mandatory because:
    #
    # 1. It helps users understand the input params and output params
    #    expected to and from your Model.
    # 2. Tiyaro will automatically generate an OpenAPI scpec for your Models API based on your schema
    # 3. Tiyaro will automatically generate sample code snippets for your user based on your schema
    #
    # Instead of reinventing a new way of declaring schema, we use the well known 'marshmallow' library
    # https://marshmallow.readthedocs.io/en/stable/index.html
    #
    #
    # Input and Output schema MUST be a valid JSON
    def declareSchema(self):
        # Example schema
        '''
        #
        # Define your input schema as a 'marshmallow' dict
        # https://marshmallow.readthedocs.io/en/stable/quickstart.html#creating-schemas-from-dictionaries
        #
        self.defInputSchema({
            "img": fields.String(required=True,
                                 metadata={
                                     "description": "Base64 encoded image."}
                                 ),
            "numLabels": fields.Number()
        })

        #
        # Define your output schema as a 'marshmallow' dict
        # https://marshmallow.readthedocs.io/en/stable/quickstart.html#creating-schemas-from-dictionaries
        #
        self.defOutputSchema({
            "img": fields.String(metadata={
                "description": "Base64 encoded image."})
        })
        '''

        self.defInputSchema({
            "inputImage": fields.String(required=True,
                                        metadata={
                                            "description": "Base64 encoded image."}
                                        ),
            "numLabels": fields.Number(),
            "imageSource": fields.String(),
            "rasterize": fields.Boolean(),
        })

        self.defOutputSchema({
            "outputImage": fields.String(reqruied=True, metadata={
                "description": "Base64 encoded image."}),
            "labelsFound": fields.Number(),
        })

    def setup_model(self, pretrained_file_path):
        self.model = None
        self.task = 'classical_sr'
        self.scale = 2
        self.patch_size = 48
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        print(f'Available device is: {self.device}')
        model = net(upscale=self.scale, in_chans=3, img_size=self.patch_size, window_size=8,
                    img_range=1., depths=[6, 6, 6, 6, 6, 6], embed_dim=180, num_heads=[6, 6, 6, 6, 6, 6],
                    mlp_ratio=2, upsampler='pixelshuffle', resi_connection='1conv')
        pretrained_model = torch.load(pretrained_file_path)
        param_key_g = 'params'
        model.load_state_dict(pretrained_model[param_key_g] if param_key_g in pretrained_model.keys() else pretrained_model, strict=True)
        model.eval()
        model = model.to(self.device)
        self.model = model

    def __pre_process(self, json_input):
        base_64_img_str = json_input.get("inputImage")
        window_size = 8
        base_64_img_bytes = base_64_img_str.encode('utf-8')
        img_str = base64.decodebytes(base_64_img_bytes)
        nparr = np.frombuffer(img_str, np.uint8)
        img_lq = cv2.imdecode(
            nparr, cv2.IMREAD_COLOR).astype(np.float32) / 255.
        img_lq = np.transpose(img_lq if img_lq.shape[2] == 1 else img_lq[:, :, [
                              2, 1, 0]], (2, 0, 1))  # HCW-BGR to CHW-RGB
        img_lq = torch.from_numpy(img_lq).float().unsqueeze(
            0).to(self.device)  # CHW-RGB to NCHW-RGB
        _, _, h_old, w_old = img_lq.size()
        h_pad = (h_old // window_size + 1) * window_size - h_old
        w_pad = (w_old // window_size + 1) * window_size - w_old
        img_lq = torch.cat([img_lq, torch.flip(img_lq, [2])], 2)[
            :, :, :h_old + h_pad, :]
        img_lq = torch.cat([img_lq, torch.flip(img_lq, [3])], 3)[
            :, :, :, :w_old + w_pad]
        return img_lq

    def infer(self, json_input):
        # Example of inference
        input = self.__pre_process(json_input)

        print("inferencing..")
        with torch.no_grad():
            output = self.model(input)
        print("inferencing done..")

        return self.__post_process(input, output)        

    def __post_process(self, input, model_output):
        output = model_output
        _, _, h_old, w_old = input.size()
        output = output[..., :h_old * self.scale, :w_old * self.scale]

        output = output.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        if output.ndim == 3:
            # CHW-RGB to HCW-BGR
            output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round().astype(np.uint8)  # float32 to uint8
        x, y = cv2.imencode(".jpg", output)
        base_64_img_bytes = base64.encodebytes(y)
        base_64_img_str = base_64_img_bytes.decode('utf-8')
        return {"outputImage": base_64_img_str}