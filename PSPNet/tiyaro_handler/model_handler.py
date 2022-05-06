from tiyaro.sdk.base_handler import TiyaroBase
from marshmallow import fields
import models
import dataloaders
from torchvision import transforms
import torch.nn.functional as F
import torch
import cv2
import numpy as np
from collections import OrderedDict
import base64
from io import BytesIO
from utils.helpers import colorize_mask
from PIL import Image
from utils import palette


class TiyaroHandler(TiyaroBase):
    # Declaring a Schema is Optional.  But, we highly recommend it because:
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
                                        )
        })

        self.defOutputSchema({ 
            "outputImage": fields.String(reqruied=True, metadata={
                "description": "Base64 encoded image."})
        })

    def setup_model(self, pretrained_file_path):
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.checkpoint = torch.load(pretrained_file_path, map_location=self.device)
        self.model = models.pspnet.PSPNet(num_classes=21, backbone="resnet50", freeze_bn=False, freeze_backbone=False)
        if isinstance(self.checkpoint, dict) and 'state_dict' in self.checkpoint.keys():
            self.checkpoint = self.checkpoint['state_dict']
        # If during training, we used data parallel
        if 'module' in list(self.checkpoint.keys())[0] and not isinstance(self.model, torch.nn.DataParallel):
            # for gpu inference, use data parallel
            if "cuda" in self.device.type:
                self.model = torch.nn.DataParallel(self.model)
            else:
            # for cpu inference, remove module
                new_state_dict = OrderedDict()
                for k, v in self.checkpoint.items():
                    name = k[7:]
                    new_state_dict[name] = v
                self.checkpoint = new_state_dict



        self.dataset_type = 'VOC'
        self.scales = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25]
        self.to_tensor = transforms.ToTensor()
        self.MEAN = [0.45734706, 0.43338275, 0.40058118]
        self.STD = [0.23965294, 0.23532275, 0.2398498]
        self.normalize = transforms.Normalize(self.MEAN, self.STD)
        self.num_classes = 21
        self.palette = palette.get_voc_palette(self.num_classes)
        
        self.model.load_state_dict(self.checkpoint)
        self.model.to(self.device) 
        self.model.eval()        

    def __pre_process(self, json_input):
        # Example of how the user provided fields are extracted in infer for
        inputImage = json_input.get("inputImage")
        base_64_img_bytes = inputImage.encode('utf-8')
        img_str = base64.decodebytes(base_64_img_bytes)
        nparr = np.frombuffer(img_str, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        self.img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.img = self.normalize(self.to_tensor(self.img)).unsqueeze(0)
        return self.img

    def infer(self, json_input):
        # Example of inference
        image = self.__pre_process(json_input)
        with torch.no_grad():
            prediction = self.model(image.to(self.device))
            prediction = prediction.squeeze(0).cpu().numpy()
            prediction = F.softmax(torch.from_numpy(prediction), dim=0).argmax(0).cpu().numpy()
        return self.__post_process(prediction)
        
    def __post_process(self, prediction):
        colorized_mask = colorize_mask(prediction, self.palette)
        # colorized_mask = cv2.cvtColor(np.float32(colorized_mask), cv2.COLOR_RGB2GRAY)
        
        # # Example of post-processing
        # x, y = cv2.imencode(".jpg", colorized_mask)
        buffered = BytesIO()
        colorized_mask.convert("RGB").save(buffered, format="JPEG")
        base_64_img_bytes = base64.b64encode(buffered.getvalue())
        base_64_img_str = base_64_img_bytes.decode('utf-8')
        return {"outputImage": base_64_img_str}
