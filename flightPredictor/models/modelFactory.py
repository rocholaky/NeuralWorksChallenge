import sklearn
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import  GridSearchCV, StratifiedKFold
from abc import ABC, abstractmethod


class absModel: 
    def grid_search(self, data_dict, param_grid, scoring="accuracy"):
        # generate a grid search object, with 5 cross validation sets
        try: 
            grid_search= GridSearchCV(self._model, param_grid=param_grid,
                                    cv = 5, verbose=1)
            # extract the training set: 
            x_train, y_train = data_dict["train"]
            # if theres a validation set we add it to the fit
            if "validation" in data_dict:
                grid_search.fit(x_train, y_train, eval_set=[data_dict["validation"]], scoring=scoring)
            else: 
                grid_search.fit(x_train, y_train, scoring=scoring)
        except:
            ValueError("Check the parameters of the model")
        
        # obtain and save best model and parameters
        self._model = grid_search.best_estimator_
        self.parameters = grid_search.best_params_
        

    @abstractmethod    
    def get_parameters(self): 
        pass

    @property
    def estimator(self): 
        return self._model 

    def fit(self, data_dict):
        x_train, y_train = data_dict["train"]
        if "validation" in data_dict: 
            self._model = self._model.fit(x_train, y_train, eval_set=[data_dict["validation"]])
        else: 
            self._model.fit(x_train, y_train)

    def predict(self, x): 
        return self._model.predict(x)



class ModelFactory:

    def build_model(self, model_type, **model_parameters): 
        model_parameters["random_state"] = 42
        if model_type=="xgboost": 
            return xgbModel(**model_parameters)
        elif model_type=="random_forest":
            return randomForestModel(**model_parameters)
        elif model_type=="decision_tree":
            return decisionTreeModel(**model_parameters)
        else: 
            raise ValueError(f"Model type {model_type} is not an option")




class xgbModel(absModel): 
    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self.parameters = model_parameters
        self.parameters["objective"] =  "binary:logistic"
        self._model = xgb.XGBClassifier(**model_parameters)


class randomForestModel(absModel): 

    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self.parameters = model_parameters
        self._model = RandomForestClassifier(**model_parameters)


class decisionTreeModel(absModel): 
    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self.parameters = model_parameters
        self.model = DecisionTreeClassifier(**model_parameters)