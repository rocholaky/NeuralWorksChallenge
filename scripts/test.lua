aerolineas = { "Grupo LATAM", "Sky Airline", "Aerolineas Argentinas", "Copa Air", "Latin American Wings" }
mes = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
tipovuelo = {"N", "I"}
vloi = {224, 225, 226}

request1 = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    body = '{"OPERA": ' .. names[math.random(#aerolineas)] .. '}'
    return wrk.format("POST", "/test1", headers, body)
end

request2 = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    body = '{"name": ' .. names[math.random(#names)] .. '}'
    return wrk.format("POST", "/test2", headers, body)
end

request3 = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    body = '{"name": ' .. names[math.random(#names)] .. '}'
    return wrk.format("GET", "/test3", headers, body)
end

requests = {}
requests[0] = request1
requests[1] = request2
requests[2] = request3
requests[3] = request3

request = function()
    return requests[math.random(0, 3)]()
end

response = function(status, headers, body)
    if status ~= 200 then
        io.write("------------------------------\n")
        io.write("Response with status: ".. status .."\n")
        io.write("------------------------------\n")
        io.write("[response] Body:\n")
        io.write(body .. "\n")
    end
end