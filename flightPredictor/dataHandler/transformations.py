from sklearn.pipeline import Pipeline, make_pipeline
from flightPredictor.dataHandler.encoders import EncoderFactory
from sklearn.compose import ColumnTransformer

class pipeGenerator: 
    def generate_pipeline(self, encoding_dict): 
        encoder_factory = EncoderFactory()
        pipeline_list = [(method, encoder_factory.create_encoder(method), columns) for method, columns in encoding_dict.items()]
        return ColumnTransformer(transformers=pipeline_list, remainder='passthrough')


