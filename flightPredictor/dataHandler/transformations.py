from sklearn.pipeline import Pipeline, make_pipeline
from flightPredictor.dataHandler.encoders import EncoderFactory
from sklearn.compose import ColumnTransformer



## The Transformation script helps in the creation of pipelines that act through columns, 
# the user provides a encoding dict where it is decided how to encode each column, all columns that are not in the
# encoding dict will be passed through the encoder, meaning they wont be encoded, but will persist. 
class pipeGenerator: 
    def generate_pipeline(self, encoding_dict): 
        encoder_factory = EncoderFactory()
        pipeline_list = [(method, encoder_factory.create_encoder(method), columns) for method, columns in encoding_dict.items()]
        return ColumnTransformer(transformers=pipeline_list, remainder='passthrough')

