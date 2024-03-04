import pandas as pd
import requests
import os
import logging
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s - Message: %(message)s", datefmt="%Y-%m-%d")
load_dotenv()




def extraer_datos_api(url:str,params=None)-> dict:
    """
    Consultar una API para obtener datos sobre la calidad del aire.

    Args:
        url (str): La URL de la API.
        params (dict): Parametros de consulta para enviar a la API.

    Returns:
        dict: Datos de calidad del aire en formato json.
    """
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as err:
        logging.error(f'Error al consultar la API: {err}')
        return None
    



def transformar_datos(datos:dict,ciudad:str):
    """
    Trasformar los datos en el formato deseado

    Args:
        datos (dict): datos de calidad del aire

    Returns:
        DataFrame: DataFrame con los datos trasformados
    """
    # Nombre de las columnas
    nombre_columnas = ['Fecha_Hora_Medicion','AQI','Dominante_Contaminante','PM10','PM2.5','SO2','Temperatura','Humedad_Relativa',
                       'Presion_Atmosferica','Punto_Rocio','Velocidad_Viento','Rafaga_Viento','Ciudad','Latitud','Longitud']
    
    try:
        df_datos = pd.json_normalize(datos)

        #Extraer información de las ciudades y cordenadas geograficas    
        df_datos['ciudad'] = ciudad
        df_datos['latitud'] = df_datos['city.geo'][0][0]
        df_datos['longitud'] = df_datos['city.geo'][0][1]

        # Son las columnas del DataFrame que se necesitan 
        list_columnas_df = ['time.s','aqi','dominentpol','iaqi.pm10.v','iaqi.pm25.v','iaqi.so2.v', 'iaqi.t.v', 'iaqi.h.v', 'iaqi.p.v','iaqi.dew.v','iaqi.w.v',
                            'iaqi.wg.v','ciudad','latitud','longitud']

        # Verificamos que todas las ciudades tengan las mismas columnas.
        for columna in list_columnas_df:
            if columna not in df_datos:
                df_datos[columna] = 0

        #Seleccionamos las columnas necesarias y les cambiamos el nombre
        df_ciudad = df_datos[list_columnas_df]
        df_ciudad.columns = nombre_columnas
        return df_ciudad
    except Exception as err:
        logging.error(f'No hay data en esa ciudad: {ciudad}')
        return None




def obtener_datos_ciudades(ciudades:list, url_base:str, params:dict):
    """
    Obtiene y transforma los datos de calidad del aire para las ciudades especificadas.

    Args:
        ciudades (list): Lista de nombres de ciudades.
        url_base (str): URL base de la API.
        params (dict): Parámetros de la API.

    Returns:
        DataFrame: DataFrame de Pandas con los datos de calidad del aire de todas las ciudades.
    """

    # DataFrame vacio
    df_calidad_aire = pd.DataFrame()

    
    for ciudad in ciudades:
        logging.info(f'Extraemos los datos...{ciudad}')
        #Extraemos los datos de la Api por ciudad.
        dict_datos = extraer_datos_api(url_base + ciudad, params)
        # Trasforma los datos por ciudad
        df_datos_ciudad = transformar_datos(dict_datos,ciudad)
        if df_datos_ciudad is not None:
            #Ingresamos los datos al DataFrame.
            df_calidad_aire = pd.concat([df_calidad_aire, df_datos_ciudad])
    return df_calidad_aire




def crear_archivo(df):
    # eliminamos el index
    df = df.reset_index(drop=True)
    # exportamos el archivo csv
    df.to_csv('calidad_aire.csv',index=False)




if __name__ == '__main__':
    PARAMS = {
    'token': os.getenv('API_KEY') 
    }
    # Ciudades que quiero extraer sus datos.
    ciudades = ['Guadalajara','Monterrey','Mexico City', 'Puebla','Aguascalientes','Merida','Toluca','Morelia','Durango','Chihuahua','San luis Potosi','Leon','Buenos Aires','Medellin']
    URL = f'https://api.waqi.info/feed/'
    df_calidad_aire = obtener_datos_ciudades(ciudades,URL,PARAMS)

    if df_calidad_aire is not None:
        # Creamos un csv
        crear_archivo(df_calidad_aire)
        logging.info('Terminado')
    else:
        logging.info('Hubo un error al obtener los datos')