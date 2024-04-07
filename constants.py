import os
from dotenv import load_dotenv

load_dotenv()



# Url base de la Api
URL = 'https://api.waqi.info/feed/'

# Parametros neecesario de la API
PARAMS = {
    'token': os.getenv('API_KEY') 
    }

# Son las columnas del DataFrame que se necesitan 
LIST_COLUMNAS_DF = [
    'time.s',
    'ciudad',
    'latitud',
    'longitud',
    'aqi',
    'dominentpol',
    'iaqi.pm10.v',
    'iaqi.pm25.v',
    'iaqi.so2.v',
    'iaqi.t.v', 
    'iaqi.h.v', 
    'iaqi.p.v',
    'iaqi.dew.v',
    'iaqi.w.v',
    'iaqi.wg.v']




# Nombre de las columnas
LIST_NOMBRE_COLUMNAS = [
    'fecha_hora_medicion',
    'ciudad',
    'latitud',
    'longitud',
    'aqi',
    'dominante_contaminante',
    'pm10',
    'pm25',
    'so2',
    'temperatura',
    'humedad_relativa',
    'presion_atmosferica',
    'punto_rocio',
    'velocidad_viento',
    'rafaga_viento'
]




# Ciudades que quiero extraer sus datos.
LIST_CIUDADES = [
     'Guadalajara',
     'Monterrey',
     'Mexico City',
     'Puebla',
     'Aguascalientes',
     'Merida',
     'Toluca',
     'Durango',
     'Chihuahua',
     'San luis Potosi',
     'Leon',
     'Buenos Aires',
     'Medellin']


