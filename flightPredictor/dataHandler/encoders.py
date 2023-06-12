from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim 
import os


class EncoderFactory:
    def create_encoder(self, encoding_method): 
        if encoding_method == "one-hot":
                return OneHot()
        elif encoding_method== "ordinal": 
            return Ordinal()
        elif encoding_method == "cyclical-hour":
            return CyclicalHour()
        elif encoding_method == "cyclical-month":
            return CyclicalMonth()
        elif encoding_method == "cyclical-day":
            return CyclicalDay()
        elif encoding_method== "scale": 
            return Scale()
        elif encoding_method=="city": 
            return LongLangEncoder()
        else: 
            raise ValueError(f"Invalid Encoder type: {encoding_method}")
    
        
class OneHot(BaseEstimator, TransformerMixin): 
    def __init__(self) -> None:
        super().__init__()
        self.enc = OneHotEncoder(handle_unknown='ignore')
    
    def transform(self, X): 
       return self.enc.transform(X)
       

    def fit(self, X, y=None): 
        self.enc = self.enc.fit(X)
        return self

class Ordinal(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()
        self.enc = OrdinalEncoder()

    def transform(self, X): 
        return self.enc.transform(X)

    def fit(self, X, y=None): 
        self.enc.fit(X)
        return self


#Todo: integer encoder
class CyclicalHour(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        name = X.columns[0]
        X[f"{name}_sin"] = np.sin(2 * np.pi * X[name].astype(float)/ 2400)
        X[f"{name}_cos"] = np.cos(2 * np.pi * X[name].astype(float)/ 2400)

        return X.drop(columns=[name])

class CyclicalMonth(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        name = X.columns[0]
        X[f"{name}_sin"] = np.sin(2 * np.pi * X[name].astype(float)/ 12)
        X[f"{name}_cos"] = np.cos(2 * np.pi * X[name].astype(float)/ 12)

        return X.drop(columns=[name])
    
class CyclicalDay(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        name = X.columns[0]
        X[f"{name}_sin"] = np.sin(2 * np.pi * X[name].astype(float)/ 31)
        X[f"{name}_cos"] = np.cos(2 * np.pi * X[name].astype(float)/ 31)

        return X.drop(columns=[name])
    
    
class Scale(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        self.scaler.fit(X)
        return self

    def transform(self, X): 
        return self.scaler.transform(X)


class LongLangEncoder(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()
        self.LONGLANG = ["LONGITUDE", "LATITUDE"]

    def geocode_city(self, city):
        
        if pd.isna(city):
            raise ValueError("There's a row without a city")
        
        location = self.geolocator.geocode(city.split(",")[0])
        if location:
            return location.longitude, location.latitude
        else: 
            raise ValueError(f"Ciudad: {city} is misspelled")
        
    def fit(self, X, y=None):
        self.geolocator = Nominatim(user_agent="EDA")
        self.city = pd.DataFrame(np.concatenate([X[a_column].unique() for a_column in X.columns]), columns=["city"])
        self.city[self.LONGLANG]  = self.city.apply(lambda x: self.geocode_city(x["city"]), axis=1, result_type="expand")
        self.city.to_json(orient="records")
        delattr(self, "geolocator")
        return self
    
    def transform(self, X):
        names = X.columns.tolist()
        city = pd.DataFrame(self.city)
        for a_name in names: 
            X = X.merge(city[self.LONGLANG+["city"]], left_on=a_name, right_on="city", how="left")
            X.rename(columns={"LONGITUDE": f"Longitude_{a_name}", "LATITUDE":f"Latitude_{a_name}"}, inplace=True)
            X.drop(columns=["city"], inplace=True)
        return X.drop(columns=names)

            




