import resource
# Get the current soft and hard limits
soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
print("Current limits:", soft_limit, hard_limit)

# Set new limits
new_soft_limit = 80000  # Set your desired soft limit
new_hard_limit = 80000  # Set your desired hard limit
resource.setrlimit(resource.RLIMIT_NOFILE, (new_soft_limit, new_hard_limit))

from fastapi import FastAPI, Query, HTTPException
import uvicorn
from pydantic import BaseModel
import joblib
from datetime import datetime
import pandas as pd


# increasing amount of connections applied:
soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
print("New limits:", soft_limit, hard_limit)
# loading the model:
ModeloPredictivoAtrasos = joblib.load("api/flightPredictor.pkl")
# start the api: 
app = FastAPI()
# a mapping dictionary for output:
ATRASO_DICT = {1: "ATRASADO",
               0: "A TIEMPO"}


# Generating FlightDelayPredictor:
class FlightDelayPredictor(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES:str
    temporada_alta: str
    DIA:int
    DIANOM:str
    periodo_dia: str
    FECHA: str
    SIGLADES: str
    SIGLAORI: str
    
## Routes of the api: 
@app.post("/predecir_atraso")
async def atrasado(flight_query:FlightDelayPredictor):
        # get the date from the model and generate a datetime object
        datetime_obj = datetime.strptime(flight_query.FECHA, '%Y-%m-%d %H:%M:%S')
        # encode the hour of the flight
        hora = 100*datetime_obj.hour+datetime_obj.minute
        # generate the mapping json with the attributes for prediction: 
        flight_json = {"OPERA": flight_query.OPERA,
                       "TIPOVUELO": flight_query.TIPOVUELO,
                       "MES": flight_query.MES,
                       "temporada_alta": flight_query.temporada_alta,
                       "DIA": flight_query.DIA,
                       "DIANOM": flight_query.DIANOM,
                        "periodo_dia": flight_query.periodo_dia,
                        "SIGLADES": flight_query.SIGLADES,
                        "SIGLAORI": flight_query.SIGLAORI,
                        "HOUR-I": hora}
        # Generate the dataFrame with the data: 
        data_vuelo = pd.DataFrame(flight_json, index=[0])
        try:
            # predict delay
            prediccion = ModeloPredictivoAtrasos.predict(data_vuelo).tolist()[0]
            # return a json with the string of delayed or not 
            return {"Atraso": ATRASO_DICT[prediccion]}
        except: 
            raise HTTPException(status_code=400, detail="Revise la manera en que se está pasando los datos.")

if __name__=="__main__":
     uvicorn.run(app, host='127.0.0.1', port=8000, workers=5 )