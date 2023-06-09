import sklearn
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import  GridSearchCV, StratifiedKFold
from flightPredictor.dataHandler import transformations
from sklearn.pipeline import Pipeline
from tqdm import tqdm
from joblib import dump, load


class absModel: 
    def grid_search(self, data_dict, param_grid, encoding_dict):
            # generate a grid search object, with 5 cross validation sets
        #try: 
            
            grid_search= GridSearchCV(self._model, param_grid=param_grid,
                                    cv = 3, verbose=1)
            grid_search = self.insert_model_to_pipeline(grid_search, encoding_dict)
            
            param_grid = {f"classifier__{key}": value for key, value in param_grid.items()}
            # extract the training set: 
            x_train, y_train = data_dict["train"]            
            
            # if theres a validation set we add it to the fit
            if "validation" in data_dict:
                x_val, y_val = data_dict["validation"]
                pipeline = grid_search.named_steps["encoder"]
                pipeline.fit(x_train, y_train)
                x_val = pipeline.transform(x_val)
                grid_search = grid_search.fit(x_train, y_train, classifier__eval_set=[(x_val, y_val)], classifier__verbose=False)
            else: 
                grid_search.fit(x_train, y_train)
            # obtain and save best model and parameters:
            self._model = grid_search
        #except:
        #   raise ValueError("Check the parameters of the model")
        
        
        
        

    @property
    def parameters(self): 
        # function to return the parameters of the actual model
        return self._parameters

    @property
    def estimator(self): 
        # returning the base estimator. 
        return self._model 
    
    def insert_model_to_pipeline(self, model, encoding_dict):
        pipelineFactory = transformations.pipeGenerator()
        encoder = pipelineFactory.generate_pipeline(encoding_dict)
        return Pipeline([("encoder", encoder),
                                ("classifier", self._model)])

    def fit(self, data_dict, encoding_dict):
        """
        fit: function that trains the model 
        parameters: 
            data_dict[dictionary]: the data dictionary with train, validation data. 
        """
        # get training data
        x_train, y_train = data_dict["train"]
        self._model = self.insert_model_to_pipeline(self._model, encoding_dict)
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
        dump(self._model, path) 



class ModelFactory:

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




class xgbModel(absModel): 
    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self._parameters = model_parameters
        self._parameters["objective"] =  "binary:logistic"
        self._model = xgb.XGBClassifier(**model_parameters)


class randomForestModel(absModel): 

    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self._parameters = model_parameters
        self._model = RandomForestClassifier(**model_parameters)


class decisionTreeModel(absModel): 
    def __init__(self, **model_parameters) -> None:
        super().__init__()
        self._parameters = model_parameters
        self.model = DecisionTreeClassifier(**model_parameters)