from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from abc import ABC, abstractmethod
import numpy as np

class absFactoryEncoder(ABC):
    
    @abstractmethod
    def create_encoder(self, encoding_method, column_to_encode):
        raise NotImplementedError("The encoder is not set for this configuration") 




class SuperEncoderFactory:
    def __init__(self, categorical_handle, number_handle) -> None:
        self.categorical_handle = categorical_handle
        self.number_handle = number_handle

    def create_encoder(self, encoder_type, column_to_encode, encoding_method=None): 
       if encoder_type=="str": 
           encoding_method = encoding_method if encoding_method else self.categorical_handle
           return CategoricalEncoderFactory().create_encoder(encoding_method, column_to_encode)
       elif encoder_type=="int" or encoder_type=="float" :
           encoding_method = encoding_method if encoding_method else self.number_handle
           return NumberEncoderFactory().create_encoder(encoding_method, column_to_encode)
       else: 
           ValueError("The encoder type is not supported")


## Categorical encoder Factory 
class CategoricalEncoderFactory(absFactoryEncoder):
    def create_encoder(encoding_method, column_to_encode):
        if encoding_method == "one-hot":
                return OneHot(column_to_encode)
        elif encoding_method== "ordinal": 
            return Ordinal(column_to_encode)
        else: 
            raise ValueError(f"Invalid Encoder type: {encoding_method}")

class OneHot(BaseEstimator, TransformerMixin): 
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

class Ordinal(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_encode) -> None:
        super().__init__()
        self.column_to_encode = column_to_encode

    def transform(self, X): 
        X[self.column_to_encode] = self.enc.transform(X[self.column_to_encode])
        return X

    def fit(self, X, y=None): 
        enc = OrdinalEncoder(handle_unknown='ignore')
        self.enc = enc.fit(X[self.column_to_encoder])


#Todo: integer encoder

class NumberEncoderFactory(absFactoryEncoder):
    def create_encoder(self, encoding_method, column_to_encode):
        if encoding_method == "cyclical":
            return CyclicalHour(column_to_encode)
        elif encoding_method== "scale": 
            return Scale(column_to_encode)
        elif encoding_method == "identity": 
            return Identity(column_to_encode)
        else: 
            raise ValueError(f"Invalid Encoder type: {encoding_method}")

class CyclicalHour(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_encode) -> None:
        super().__init__()
        self.column_to_encode = column_to_encode

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[f"sin_{self.column_to_encode}"] = np.sin(2 * np.pi * X[self.column_to_encode] / 24)
        X[f'cos_{self.column_to_encode}'] = np.cos(2 * np.pi * X[self.column_to_encode] / 24)
        return X.drop(columns=[self.column_to_encode])
    
class Identity(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_encode) -> None:
        super().__init__()
        self.column_to_encode = column_to_encode
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X): 
        return X

class Scale(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_encode) -> None:
        super().__init__()
        self.column_to_encode = column_to_encode
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        self.scaler.fit(X[self.column_to_encode])
        return self

    def transform(self, X): 
        return self.scaler.transform(X[self.column_to_encode])

        




