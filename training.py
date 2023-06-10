### package importing: 
from flightPredictor.dataHandler import splitter, encoders
from flightPredictor.models import modelFactory as mf
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
COLUMNAS_BASALES = ["OPERA", "TIPOVUELO", "MES"]
model_dictionary = {}

# IMPORTAMOS LOS DATOS DE LA BASE DE DATOS ORIGINAL
df= pd.read_csv("Datasets/MLFeatures.csv", low_memory=False)

TEST_SIZE = 0.2
VAL_SIZE = 0.2
splitter_obj = splitter.dataSplitter(test_size=TEST_SIZE, val_size=VAL_SIZE)


X = df[COLUMNAS_BASALES]
Y = df["atraso_15"]

split_dict = splitter_obj.split(X, Y)
classifier_factory = mf.ModelFactory()
x_test, y_test = split_dict["test"]
encoding_dict = {"one-hot": ["OPERA", "TIPOVUELO"]}
modelxgb_base = classifier_factory.build_model("xgboost")

'''
modelxgb_base.fit(split_dict, encoding_dict=encoding_dict)
predicted_xgb = modelxgb_base.predict(x_test)
print(classification_report(y_test, predicted_xgb))

'''



parameters = {
    'learning_rate': [0.1, 0.01],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300],
    'gamma': [0, 0.5, 1]
}

modelxgb_base.grid_search(split_dict, parameters, encoding_dict)
predicted_xgb = modelxgb_base.predict(x_test)
print(classification_report(y_test, predicted_xgb))


