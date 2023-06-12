from sklearn.model_selection import train_test_split
from flightPredictor.dataHandler.sampler import samplerFactory

'''
DATA SPLITTER: 
The data splitter class helps us split data, it works with dataframes or numpy arrays. 

The user needs to provide the test_size and val_size that will help define if the dataset should be divided into 

test set, training set or test, validation and training sets. 

The data splitter class works with the sampler class so all data sampling and splitting is done through the data splitter class and not 
through the samplers.

'''
class dataSplitter: 
    def __init__(self, test_size=0.3, val_size=0) -> None:
        assert (0<test_size) and (test_size<1),  "test percentage is of the [0, 1] interval"
        assert (0<=val_size) and (val_size<1), "validation percentage is of the [0, 1] interval"
        assert (val_size+test_size<1), "test and validation sets sum more than 1"
        self.test_size = test_size
        self.val_size = val_size


    def split(self, X, Y):

        # the split method splits data into training, test and possibly val datasets in order to train and evaluate models. 
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=self.test_size, shuffle=True, random_state=30)
        split_dict = {"train": (x_train, y_train), 
                      "test": (x_test, y_test)}
        if self.val_size>0: 
            x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=self.val_size, shuffle=True, random_state=30)
            split_dict.update({"train": (x_train, y_train), 
                               "validation": (x_val, y_val)})
        return split_dict
    
    def resample_split(self, X, y, sampler="under", percentage=[0.4]): 
        # resample split generates samples and then splits the results in a train_test split using the split method. 
        sampler = samplerFactory().create_sampler(sampler, *percentage)
        split_dict = self.split(X, y)
        x_train, y_train = sampler.fit_resample(*split_dict.pop("train"))
        split_dict["train"] = (x_train, y_train)
        return split_dict

    def show_split(self, split_dict): 
        # the show split function shows the distribution of possitive and negative classes you can find in a dataset. 
        _, y_train = split_dict["train"]
        _, y_test = split_dict["test"]
        print(f"Cantidad de vuelos train {y_train.count()}", f"Cantidad de atrasos {y_train.sum()}", f"Porcentaje de vuelos atrasados en dataset:{y_train.sum()/y_train.count()}")
        if self.val_size: 
            _, y_val = split_dict["validation"]
            print(f"Cantidad de vuelos validación {y_val.count()}", f"Cantidad de atrasos {y_val.sum()}", f"Porcentaje de vuelos atrasados en dataset:{y_val.sum()/y_val.count()}")
        print(f"Cantidad de vuelos test {y_test.count()}", f"Cantidad de atrasos {y_test.sum()}", f"Porcentaje de vuelos atrasados en dataset:{y_test.sum()/y_test.count()}")
    

        