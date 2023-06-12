### package importing: 
from flightPredictor.dataHandler import splitter, encoders
from flightPredictor.models import modelFactory as mf
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from datetime import datetime

TEST_SIZE = 0.2
VAL_SIZE = 0.2
SPLITTER = splitter.dataSplitter(test_size=TEST_SIZE, val_size=VAL_SIZE)
CLASSIFIER_FACTORY = mf.ModelFactory()
# IMPORTAMOS LOS DATOS DE LA BASE DE DATOS ORIGINAL
df_real = pd.read_csv("Datasets/dataset_SCL.csv", low_memory=False)
# IMPORTAMOS LAS FEATURES SINTETICAS
df_synthetic = pd.read_csv("Datasets/synthetic_features.csv", low_memory=False)
# UNIMOS AMBOS DATAFRAMES
df = pd.concat([df_real, df_synthetic], axis=1)


EXPANDED_FEATURES = ["OPERA", "TIPOVUELO", "MES", "temporada_alta", "DIA", "DIANOM", "periodo_dia","HOUR-I", "SIGLADES", "SIGLAORI"]
def get_periodo_dia(fecha):
    fecha_time = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').time()
    mañana_min = datetime.strptime("05:00", '%H:%M').time()
    mañana_max = datetime.strptime("11:59", '%H:%M').time()
    tarde_min = datetime.strptime("12:00", '%H:%M').time()
    tarde_max = datetime.strptime("18:59", '%H:%M').time()
    noche_min1 = datetime.strptime("19:00", '%H:%M').time()
    noche_max1 = datetime.strptime("23:59", '%H:%M').time()
    noche_min2 = datetime.strptime("00:00", '%H:%M').time()
    noche_max2 = datetime.strptime("4:59", '%H:%M').time()
    
    if(fecha_time >= mañana_min and fecha_time <= mañana_max):
        return 'mañana'
    elif(fecha_time >= tarde_min and fecha_time <= tarde_max):
        return 'tarde'
    elif((fecha_time >= noche_min1 and fecha_time <= noche_max1) or
         (fecha_time >= noche_min2 and fecha_time <= noche_max2)):
        return 'noche'
    
df['periodo_dia'] = df['Fecha-I'].apply(get_periodo_dia)
df.loc[df["SIGLADES"]=="Ushuia", "SIGLADES"] = "Ushuaia"
df["Fecha-I"] = pd.to_datetime(df["Fecha-I"],  format='%Y-%m-%d %H:%M:%S')
df["HOUR-I"] = df.apply(lambda x: 100*x["Fecha-I"].hour+x["Fecha-I"].minute, axis=1)
X_expanded = df[EXPANDED_FEATURES]
Y_expanded = df["atraso_15"].astype(bool)
smote_under_data_dict = SPLITTER.resample_split(X_expanded, Y_expanded, sampler='smote-under', percentage=[0.25, 0.7])
encoding_dict = {"one-hot": ["OPERA", "TIPOVUELO" , "temporada_alta", "DIANOM", "MES", "periodo_dia"],
                 "cyclical-hour": ["HOUR-I"],
                 "city": ["SIGLADES", "SIGLAORI"]}
xgb_smote_grid = CLASSIFIER_FACTORY.build_model("xgboost", objective= 'binary:logistic', learning_rate=0.1,n_estimators= 100, subsample= 0.5, eval_metric='aucpr')
parameters = {
    'learning_rate': [0.1, 0.01],
    'max_depth': [3, 5, 7],
}
xgb_smote_grid.grid_search(smote_under_data_dict, parameters, encoding_dict, cv=2)