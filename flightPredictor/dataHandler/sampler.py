from imblearn.over_sampling import SMOTENC, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from abc import ABC, abstractmethod

class absSampler(ABC): 
    @abstractmethod
    def init_sampler(self, x): 
        pass

    def fit_resample(self, X, y):
        sampler = self.init_sampler(X)
        return sampler.fit_resample(X, y)


class samplerFactory: 
    def create_sampler(self, sampler_type, *percentage):
        assert isinstance(sampler_type, str), "Value should be a string"
        sampler_type = sampler_type.lower()
        if sampler_type =="smote": 
            return smoteSampler(*percentage)
        elif sampler_type =="over": 
            return overSampler(*percentage)
        elif sampler_type=="under": 
            return underSampler(*percentage)
        elif sampler_type=="smote-under":
            return smoteAndUnderSampler(*percentage)
        else: 
            raise ValueError(f"Invalid Encoder type: {sampler_type}")
        



class smoteSampler(absSampler):
    
    def __init__(self, *percentage) -> None:
        assert len(percentage)==1, ValueError("smoteSampler needs just one percentage")
        super().__init__()
        self.percentage = percentage[0]
        self.sampler = SMOTENC
    
    def init_sampler(self, x): 
        object_columns_in_x= x.select_dtypes(include="object").columns.tolist()
        x_columns = x.columns    
        sampler = self.sampler(sampling_strategy=self.percentage, random_state=42, k_neighbors=10,
                                categorical_features=[x_columns.get_loc(a_column) for a_column in object_columns_in_x])
        return sampler
    

class overSampler(absSampler): 
    def __init__(self, *percentage) -> None:
        assert len(percentage)==1, ValueError("overSampler needs just one percentage")
        super().__init__()
        self.percentage = percentage
        self.sampler = RandomOverSampler

    def init_sampler(self, x):
        sampler = self.sampler(sampling_strategy=self.percentage[0], random_state=42)
        return sampler

    

class underSampler(absSampler):
    def __init__(self, *percentage) -> None:
        assert len(percentage)==1, ValueError("underSampler needs just one percentage")
        super().__init__()
        self.percentage = percentage
        self.sampler = RandomUnderSampler

    def ini_sampler(self, x): 
        sampler = self.sampler(sampling_strategy=self.percentage[0], random_state=42)
        return sampler

    def fit_resample(self, X, y):
        return self.sampler.fit_resample(X, y)
    

class smoteAndUnderSampler(absSampler): 
    def __init__(self, *percentage) -> None:
        super().__init__()
        assert len(percentage)>1, ValueError("needs more percentage parameters")
        self.percentage = percentage
        self.sampler_smote = SMOTENC
        self.sampler_under = RandomUnderSampler


    def init_sampler(self, x): 
        sampler = []
        object_columns_in_x= x.select_dtypes(include="object").columns.tolist()
        x_columns = x.columns
        sampler.append(self.sampler_smote(sampling_strategy=self.percentage[0], random_state=42, k_neighbors=10,
                                categorical_features=[x_columns.get_loc(a_column) for a_column in object_columns_in_x]))
        sampler.append(self.sampler_under(sampling_strategy=self.percentage[1], random_state=42))
        return sampler
    
    def fit_resample(self, X, y):
        sampler = self.init_sampler(X)
        X, y = sampler[0].fit_resample(X, y)
        X, y = sampler[1].fit_resample(X, y)
        return X, y
    
    