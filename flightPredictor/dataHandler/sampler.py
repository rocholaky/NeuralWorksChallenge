from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from abc import ABC, abstractmethod

class absSampler(ABC): 
    @abstractmethod
    def fit_resample(self, X, y): 
        pass


class samplerFactory: 
    def create_sampler(self, sampler_type, percentage):
        assert isinstance(sampler_type, str), "Value should be a string"
        sampler_type = sampler_type.lower()
        if sampler_type =="smote": 
            return smoteSampler(percentage)
        elif sampler_type =="over": 
            return overSampler(percentage)
        elif sampler_type=="under": 
            return underSampler(percentage)
        else: 
            raise ValueError(f"Invalid Encoder type: {sampler_type}")
        



class smoteSampler(absSampler):
    
    def __init__(self, percentage) -> None:
        super().__init__()
        self.percentage = percentage
        self.sampler = SMOTE(sampling_strategy=percentage, random_state=35, k_neighbors=10)


    def fit_resample(self, X, y):
        return self.sampler.fit_resample(X, y)
    

class overSampler(absSampler): 
    def __init__(self, percentage) -> None:
        super().__init__()
        self.percentage = percentage
        self.sampler = RandomOverSampler(sampling_strategy=percentage, random_state=35)

    def fit_resample(self, X, y):
        return self.sampler.fit_resample(X, y)

class underSampler(absSampler):
    def __init__(self, percentage) -> None:
        super().__init__()
        self.percentage = percentage
        self.sampler = RandomUnderSampler(sampling_strategy=percentage, random_state=35)

    def fit_resample(self, X, y):
        return self.sampler.fit_resample(X, y)