from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.base import BaseEstimator, TransformerMixin




class EncoderFactory:
    def create_encoder(self, encoder_type, column_to_encode): 
        if encoder_type == "one-hot":
            return oneHot(column_to_encode)
        elif encoder_type== "categorical": 
            return categorical(column_to_encode)
        else: 
            raise ValueError(f"Invalid Encoder type: {encoder_type}")
        
class oneHot(BaseEstimator, TransformerMixin): 
    def __init__(self, column_to_encode) -> None:
        super().__init__()
        self.column_to_encode = column_to_encode
    
    def transform(self, X): 
       X[self.column_to_encode] = self.enc.transform(X[self.column_to_encode])
       return X

    def fit(self, X, y=None): 
        enc = OneHotEncoder(handle_unknown='ignore')
        self.enc = enc.fit(X[self.column_to_encode])
        return self

class categorical(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_encode) -> None:
        super().__init__()
        self.column_to_encode = column_to_encode

    def transform(self, X): 
        X[self.column_to_encode] = self.enc.transform(X[self.column_to_encode])
        return X

    def fit(self, X, y=None): 
        enc = OrdinalEncoder(handle_unknown='ignore')
        self.enc = enc.fit(X[self.column_to_encoder])

        




