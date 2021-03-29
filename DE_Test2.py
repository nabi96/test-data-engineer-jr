import requests
import pandas as pd

# Hago el request a las apis que usare

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiVuelos2016/9ea3b836-6938-52dc-9626-a8e35db81dd5")
dfMViajes2016 = pd.DataFrame.from_dict(response.json())

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiVuelos2017/fc126260-1cf8-5a46-995d-ba639ff5868b")
dfMViajes2017 = pd.DataFrame.from_dict(response.json())

dfResultViaje =  dfresultAppend = dfMViajes2016.append(dfMViajes2017) #Use Appen para poner los datos como  lista, usando merge los ponia los datos 2016 continuos al 2017
dfResultViaje