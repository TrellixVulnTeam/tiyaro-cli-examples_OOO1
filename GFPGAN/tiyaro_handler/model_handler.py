from tiyaro.sdk.base_handler import TiyaroBase
from marshmallow import fields
import argparse
import cv2
import glob
import numpy as np
import os
import torch
import base64
# from basicsr.utils import imwrite

from gfpgan import GFPGANer

bg_upsampler = None



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
                                        )
        })

        self.defOutputSchema({
            "outputImage": fields.String(required=True,
                            metadata={
                            "description": "Base64 encoded image."})
        })

    def setup_model(self, pretrained_file_path):
        self.model = None
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        restorer = GFPGANer(
            model_path=pretrained_file_path,
            upscale=2,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=bg_upsampler)
        self.model = restorer

    def __pre_process(self, json_input):
        # Example of how the user provided fields are extracted in infer for
        inputImage = json_input.get("inputImage")
        base_64_img_bytes = inputImage.encode('utf-8')
        img_str = base64.decodebytes(base_64_img_bytes)
        nparr = np.frombuffer(img_str, np.uint8)
        img = cv2.imdecode(
            nparr, cv2.IMREAD_COLOR)

        return img

    def infer(self, json_input):
        # Example of inference
        input = self.__pre_process(json_input)

        cropped_faces, restored_faces, restored_img = self.model.enhance(
            input, paste_back=True)
        # output = model.infer(input)

        return self.__post_process(restored_img)

    def __post_process(self, model_output):
        output = model_output
        # cv2.imwrite('/home/sharvil/Desktop/sharvil.jpg', output)
        # output = (output * 255.0).round().astype(np.uint8)  # float32 to uint8
        x, y = cv2.imencode(".jpg", output)
        base_64_img_bytes = base64.encodebytes(y)
        base_64_img_str = base_64_img_bytes.decode('utf-8')
        return {"outputImage": base_64_img_str}
