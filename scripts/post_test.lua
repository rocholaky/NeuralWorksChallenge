wrk.method = "POST"
wrk.body = '{"FECHA": "2017-01-01 23:30:00",\
"OPERA": "American Airlines",\
"TIPOVUELO": "I",\
"MES": 1,\
"temporada_alta": 1,\
"DIA": 1,\
"DIANOM": "Domingo",\
"periodo_dia": "noche",\
"SIGLADES": "Miami",\
"SIGLAORI": "Santiago"}'
wrk.headers["Content-Type"] = "application/json"