from tiyaro.sdk.base_handler import TiyaroBase
from tiyaro_handler.base_handler import TiyaroBase
from marshmallow import fields

from magma import Magma
from magma.image_input import ImageInput


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
                                            "description": "URL of the Image."}
                                        ),
            "question": fields.String(required=True,
                                        metadata={
                                            "description": "Question for the model based on Image."}
                                        )
        })

        self.defOutputSchema({
            "answer": fields.String(reqruied=True, metadata={
                "description": "Answer from the model"})
        })

    def setup_model(self, pretrained_file_path):
        self.model = Magma.from_checkpoint(
            config_path = "configs/MAGMA_v1.yml",
            checkpoint_path = pretrained_file_path
            )

    def __pre_process(self, json_input):
        # Example of how the user provided fields are extracted in infer for
        inputImage = json_input.get("inputImage")
        question = json_input.get("question")
        inputs =[
            ImageInput(inputImage),
            question
            ] 
        embeddings = self.model.preprocess_inputs(inputs)  
        return embeddings

    def infer(self, json_input):
        # Example of inference
        input = self.__pre_process(json_input)

        output = self.model.generate(
            embeddings = input,
            max_steps = 6,
            temperature = 0.7,
            top_k = 0,
            )

        return self.__post_process(output)
        
    def __post_process(self, model_output):
        # Example of post-processing
        output = model_output[0]
        # Example of how infer returns multiple output
        return {"answer": output}