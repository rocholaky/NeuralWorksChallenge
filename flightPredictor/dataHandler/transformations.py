from sklearn.pipeline import Pipeline, make_pipeline
from flightPredictor.encoders import SuperEncoderFactory


class pipeGenerator: 
    def generate_pipeline(self, column_dtypes, categorical_handle="one-hot", number_handle="scaler"): 
        super_factory = SuperEncoderFactory(categorical_handle, number_handle)
        pipeline_list = [(column_name, super_factory.create_encoder(a_dtype, column_name)) for column_name, a_dtype in column_dtypes.items()]
        return Pipeline(pipeline_list)


