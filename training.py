### package importing: 
from flightPredictor.dataHandler import splitter, encoders
from flightPredictor.models import modelFactory as mf
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
COLUMNAS_BASALES = ["OPERA", "TIPOVUELO", "MES"]
model_dictionary = {}

# IMPORTAMOS LOS DATOS DE LA BASE DE DATOS ORIGINAL
df_real = pd.read_csv("Datasets/dataset_SCL.csv", low_memory=False)
# IMPORTAMOS LAS FEATURES SINTETICAS
df_synthetic = pd.read_csv("Datasets/synthetic_features.csv", low_memory=False)
# UNIMOS AMBOS DATAFRAMES
df = pd.concat([df_real, df_synthetic], axis=1)
# LOS MOSTRMOS:
df.head()

TEST_SIZE = 0.2
VAL_SIZE = 0.2
splitter_obj = splitter.dataSplitter(test_size=TEST_SIZE, val_size=VAL_SIZE)


X = df[COLUMNAS_BASALES].astype({"OPERA": 'category', "TIPOVUELO": 'category'})
Y = df["atraso_15"]

split_dict = splitter_obj.split(X, Y)
classifier_factory = mf.ModelFactory()
x_test, y_test = split_dict["test"]
encoding_dict = {"one-hot": ["OPERA", "TIPOVUELO"]}
modelxgb_base = classifier_factory.build_model("xgboost", objective= 'binary:logistic', learning_rate=0.01\
                                                , subsample = 0.5, max_depth = 10)


modelxgb_base.fit(split_dict, encoding_dict=encoding_dict)
predicted_xgb = modelxgb_base.predict(x_test)
print(classification_report(y_test, predicted_xgb))

modelxgb_base.fit(split_dict, encoding_dict=encoding_dict)
predicted_xgb = modelxgb_base.predict(x_test)
print(classification_report(y_test, predicted_xgb))

'''
param_grid = parameters = {
    "scale_pos_weight": [1, 3],
    "reg_lambda": [0, 0.5],
}

modelxgb_base.grid_search(split_dict, param_grid, encoding_dict)
predicted_xgb = modelxgb_base.predict(x_test)
print(classification_report(y_test, predicted_xgb))

'''

