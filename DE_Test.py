import requests
import pandas as pd

# Hago el request a las apis que usare

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiPasajeros2016/ecfb5fc7-0932-590f-832c-6d6055f2be07")
dfMPasajero2016 = pd.DataFrame.from_dict(response.json())
#dfMPasajero2016["Year"] = 2016 # añado campo año y 2016 para saber los datos de que año son

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiPasajeros2017/faabd632-cc39-552d-a68b-02de4242f636")
dfMPasajero2017 = pd.DataFrame.from_dict(response.json())
#dfMPasajero2017["Year"] = 2017 # añado campo año y 2017 para saber los datos de que año son

dfResultPasa = dfMPasajero2016.append(dfMPasajero2017) #Use Appen para poner los datos como  lista, usando merge los ponia los datos 2016 continuos al 2017
dfResultPasa