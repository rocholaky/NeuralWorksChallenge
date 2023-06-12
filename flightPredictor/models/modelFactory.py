import sklearn
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import  GridSearchCV, StratifiedKFold
from flightPredictor.dataHandler import transformations
from sklearn.pipeline import Pipeline
import joblib
from sklearn.base import BaseEstimator
from abc import ABC, abstractmethod


class absModel: 
    def grid_search(self, data_dict, param_grid, encoding_dict, cv=3):
            # generate a grid search object, with cv cross validation sets
        try: 
            # create a model with basic parameters
            model = self.build()
            # create a pipeline to encode the data 
            pipeline = self.create_pipeline(encoding_dict)
            # generate a grid search object on the model 
            grid_search= GridSearchCV(model, param_grid=param_grid,
                                    cv = cv, verbose=1)
            
           
            # extract the training set: 
            x_train, y_train = data_dict["train"]     
            # fit the pipeline       
            pipeline.fit(x_train, y_train)
            # transform the training set
            x_train = pipeline.transform(x_train)
            # if theres a validation set we add it to the fit
            if "validation" in data_dict:
                # get the validation set
                x_val, y_val = data_dict["validation"]
                # transform the validation set
                x_val = pipeline.transform(x_val)
                # procede to the grid search
                grid_search.fit(x_train, y_train, eval_set=[(x_val, y_val)], verbose=False)
            else: 
                grid_search.fit(x_train, y_train)
            # obtain and save best model and parameters:
            self._parameters.update(grid_search.best_params_)
            self._model = self.insert_model_to_pipeline(grid_search.best_estimator_, pipeline)
        except:
           raise ValueError("Check the parameters of the model")
        
        
    @abstractmethod
    def build(self):
        raise NotImplementedError()
        

    @property
    def parameters(self): 
        # function to return the parameters of the actual model
        return self._parameters

    @property
    def estimator(self): 
        # returning the base estimator. 
        return self._model 
    
    def create_pipeline(self, encoding_dict): 
        pipelineFactory = transformations.pipeGenerator()
        encoder = pipelineFactory.generate_pipeline(encoding_dict)
        return encoder
    
    def insert_model_to_pipeline(self, model, pipeline=None,encoding_dict= None):
        if pipeline is None: 
            encoder = self.create_pipeline(encoding_dict=encoding_dict)
        else: 
            encoder = pipeline
        return Pipeline([("encoder", encoder),
                                ("classifier", model)])

    def fit(self, data_dict, encoding_dict):
        """
        fit: function that trains the model 
        parameters: 
            data_dict[dictionary]: the data dictionary with train, validation data. 
        """
        # get training data
        x_train, y_train = data_dict["train"]
        self._model = self.insert_model_to_pipeline(self.build(), encoding_dict=encoding_dict)
        self._model.fit(x_train, y_train)

    def predict(self, x): 
        """
        predict: function that works in trained models and 
        generates the predicted outputs of the models. 
        """
        return self._model.predict(x)
    
    def predict_probability(self, x): 
        """
        predict probability: function that outputs the probabilities of the given data. 
        """
        return self._model.predict_proba(x)
    
    def save_model(self, path):
        joblib.dump(self, path) 



class ModelFactory:
    ## model factory generates different classifiers. 
    # The supported classifiers are decision tree, random forest and xgboost. 
    # you never work with the classifier class, you just create it with this factory class. 
    def build_model(self, model_type, **model_parameters): 
        model_parameters["random_state"] = 1
        if model_type=="xgboost": 
            return xgbModel(**model_parameters)
        elif model_type=="random_forest":
            return randomForestModel(**model_parameters)
        elif model_type=="decision_tree":
            return decisionTreeModel(**model_parameters)
        else: 
            raise ValueError(f"Model type {model_type} is not an option")




class xgbModel(absModel, BaseEstimator): 
    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self._parameters = model_parameters
        self._parameters["objective"] =  "binary:logistic"
        self._model = self.build()
    
    def build(self):
        return xgb.XGBClassifier(**self.parameters)

class randomForestModel(absModel, BaseEstimator): 

    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self._parameters = model_parameters
        self._model = self.build()

    def build(self):
        return RandomForestClassifier(**self.parameters)
    
class decisionTreeModel(absModel, BaseEstimator): 
    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self._parameters = model_parameters
        self.model = self.build()

    def build(self):
        return DecisionTreeClassifier(**self.parameters)
