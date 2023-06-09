import sklearn
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import  GridSearchCV, StratifiedKFold
from flightPredictor.dataHandler import transformations
from sklearn.pipeline import Pipeline

class absModel: 
    def grid_search(self, data_dict, param_grid, scoring="accuracy"):
        # generate a grid search object, with 5 cross validation sets
        try: 
            self._model= GridSearchCV(self._model, param_grid=param_grid,
                                    cv = 5, verbose=1)
            # extract the training set: 
            x_train, y_train = data_dict["train"]
            self.prepare_model(x_train)
            # if theres a validation set we add it to the fit
            if "validation" in data_dict:
                self._model.fit(x_train, y_train, eval_set=[data_dict["validation"]], scoring=scoring)
            else: 
                self._model.fit(x_train, y_train, scoring=scoring)
        except:
            ValueError("Check the parameters of the model")
        
        # obtain and save best model and parameters
        self._model = self._model.best_estimator_
        self._parameters = self._model.best_params_
        

    @property
    def parameters(self): 
        # function to return the parameters of the actual model
        return self._parameters

    @property
    def estimator(self): 
        # returning the base estimator. 
        return self._model 
    
    def prepare_model(self, x_train):
        pipelineFactory = transformations.pipeGenerator()
        column_dtypes = x_train.column_dtypes
        encoder = pipelineFactory(column_dtypes)
        self._model = Pipeline([("encoder", encoder),
                                ("classifier", self._model)])

    def fit(self, data_dict):
        """
        fit: function that trains the model 
        parameters: 
            data_dict[dictionary]: the data dictionary with train, validation data. 
        """
        # get training data
        x_train, y_train = data_dict["train"]
        self.prepare_model(x_train)
        if "validation" in data_dict: 
            self._model = self._model.fit(x_train, y_train, eval_set=[data_dict["validation"]])
        else: 
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