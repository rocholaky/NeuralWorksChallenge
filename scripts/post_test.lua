wrk.method = "POST"
wrk.body = '{"vuelos": [{"MES": 3,"TIPOVUELO": "N", "OPERA": "K.L.M.", "VLO_I": 226}, {"MES": 12,"TIPOVUELO": "I", "OPERA": "Air Canada", "VLO_I":226}]}'
wrk.headers["Content-Type"] = "application/json"