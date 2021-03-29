import requests
import pandas as pd

# Hago el request a las apis que usare

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiPasajeros2016/ecfb5fc7-0932-590f-832c-6d6055f2be07")
dfMPasajero2016 = pd.DataFrame.from_dict(response.json())
#dfMPasajero2016["Year"] = 2016 # añado campo año y 2016 para saber los datos de que año son

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiPasajeros2017/faabd632-cc39-552d-a68b-02de4242f636")
dfMPasajero2017 = pd.DataFrame.from_dict(response.json())
#dfMPasajero2017["Year"] = 2017 # añado campo año y 2017 para saber los datos de que año son

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiVuelos2016/9ea3b836-6938-52dc-9626-a8e35db81dd5")
dfMViajes2016 = pd.DataFrame.from_dict(response.json())

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiVuelos2017/fc126260-1cf8-5a46-995d-ba639ff5868b")
dfMViajes2017 = pd.DataFrame.from_dict(response.json())

response = requests.get("http://analytics.deacero.com/Api/GetApi/ApiLineaAerea/1a8d9e13-ce30-50fc-bf34-6490eb799a75")
dfLAereas = pd.DataFrame.from_dict(response.json())

dfResFinalultPasa = dfMPasajero2016.append(dfMPasajero2017) #Use Appen para poner los datos como  lista, usando merge los ponia los datos 2016 continuos al 2017
dfResFinalultViaje =  dfResFinalultAppend = dfMViajes2016.append(dfMViajes2017) #Use Appen para poner los datos como  lista, usando merge los ponia los datos 2016 continuos al 2017

dfRelList = pd.merge(dfResFinalultPasa, dfResFinalultViaje, left_on = 'ID_Pasajero', right_on='Cve_Cliente', how='inner') #uso Inner para traer todo la informacion en un solo DF

dfNoDupsRelList  = dfRelList.drop_duplicates() #use drop par quitar duplicados

dfNoDupsRelList[['ID_Pasajero', 'Pasajero', 'Edad', 'Cve_LA', 'Viaje', 'Clase', 'Precio','Ruta']] #Seleccione las columnas a presentar, las columnas cve_cliente y ID_Pasajero deje solo ID_Pasajero para tener una mejor presetnacion y no duplicar dator

dfListPreliminar = pd.merge(dfNoDupsRelList, dfLAereas, left_on = 'Cve_LA', right_on = 'Code', how='left') #Uso left joing para cambiar la clave_la con el nombre de la Linea_Area

dfFinal = dfListPreliminar[['Viaje', 'Clase', 'Precio', 'Ruta', 'Edad', 'Linea_Aerea']] #selecciono orde de columnas y las que voy a usar para presentar

dfFinaly = dfFinal.rename(columns = {'Viaje': 'Fecha_de_Viaje'}) #Cambio de nombre Viaje a Fecha de Viaje para presentacion

dfFinaly ['Fecha_de_Viaje'] = pd.to_datetime(dfFinaly['Fecha_de_Viaje'].astype(str), format='%m/%d/%Y') #cambie el formato de Fecha

dfFinaly['Anio'] = dfFinaly['Fecha_de_Viaje'].dt.year #genere un campo para puro año y facilitar el analisis 
dfFinaly['Mes'] = dfFinaly['Fecha_de_Viaje'].dt.month #genere un campo para puro mes y facilitar el analisis 

#dfFinaly['Anio_Mes'] = (dfFinaly['Fecha_de_Viaje'].dt.year * 100) + dfFinaly['Fecha_de_Viaje'].dt.month #genero un id para combinando año y mes

dfFinaly['Flag_Semestre'] = dfFinaly['Mes'].apply(lambda x: 'Ene-Jun' if x <= 6 else 'Jul-Dic') #use lambda para crear la logica para sacar el promedio semestral

dfFinaly

dfResFinal = dfFinaly.groupby(['Anio','Clase', 'Ruta', 'Linea_Aerea', 'Flag_Semestre'])['Precio'].mean() #agrupo y uso mean para sacar el average o promedio del precio
dfResFinal = dfResFinal.to_frame() #La función se utiliza para convertir el objeto de la serie al DataFrame
dfResFinal = dfResFinal.rename(columns = {'Precio': 'Precio_Promedio'}) #Cambio el Header Precio a Precio promedio para una mejor vista
dfResFinal