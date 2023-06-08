from sklearn.model_selection import train_test_split
from flightPredictor.dataHandler.sampler import samplerFactory


class dataSplitter: 
    def __init__(self, test_size=0.3, val_size=0) -> None:
        assert (0<test_size) and (test_size<1),  "test percentage is of the [0, 1] interval"
        assert (0<=val_size) and (val_size<1), "validation percentage is of the [0, 1] interval"
        assert (val_size+test_size<1), "test and validation sets sum more than 1"
        self.test_size = test_size
        self.val_size = val_size


    def split(self, X, Y):
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=self.test_size, shuffle=True, random_state=30)
        split_dict = {"train": (x_train, y_train), 
                      "test": (x_test, y_test)}
        if self.val_size>0: 
            x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=self.val_size, shuffle=True, random_state=30)
            split_dict.update({"train": (x_train, y_train), 
                               "validation": (x_val, y_val)})
        return split_dict
    
    def resample_split(self, X, y, sampler="under", percentage=0.4): 
        sampler = samplerFactory().create_sampler(sampler_type=sampler, percentage=percentage)
        split_dict = self.split(X, y)
        x_train, y_train = split_dict["train"]
        x_train, y_train = sampler.fit_resample(x_train, y_train)
        split_dict["train"] = (x_train, y_train)
        return split_dict
    

        