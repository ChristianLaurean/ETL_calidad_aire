import pandas as pd
import requests
import os
import logging
from dotenv import load_dotenv
# importamos el tipo de dato
from typing import Generator
from constants import LIST_COLUMNAS_DF, LIST_NOMBRE_COLUMNAS, LIST_CIUDADES

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
        
    



def obtener_datos_ciudades(ciudades:list, url_base:str, params:dict)-> Generator:
    """
    Extrae los datos de calidad del aire para las ciudades especificadas.

    Args:
        ciudades (list): Lista de nombres de ciudades.
        url_base (str): URL base de la API.
        params (dict): Parámetros de la API.

    Yield:
        Generator[Tuple[dict, str]: Generador que produce tuplas donde el primer elemento
                                                es un diccionario de datos de calidad del aire y el segundo
                                                elemento es el nombre de la ciudad correspondiente.
    """

    for ciudad in ciudades:
        logging.info(f'Extraemos los datos...{ciudad}')
        #Extraemos los datos de la Api por ciudad.
        dict_datos = extraer_datos_api(url_base + ciudad, params)
        yield dict_datos, ciudad




def transformar_datos(datos:Generator) -> pd.DataFrame:
    """
    Transforma los datos de calidad del aire en el formato deseado.

    Args:
        datos (generator): Generador que produce tuplas (dict, str), donde el primer elemento
                           es un diccionario de datos de calidad del aire y el segundo elemento
                           es el nombre de la ciudad correspondiente.

    Returns:
        pd.DataFrame: DataFrame con los datos transformados de calidad del aire.


    """
    
    # DataFrame vacío para almacenar los datos transformados
    df_calidad_aire = pd.DataFrame()

    # Iterar sobre los datos de cada ciudad
    for data, ciudad in datos:
        try:
            # Normalizar los datos del JSON
            df_datos = pd.json_normalize(data)

            # Añadir información de la ciudad y coordenadas geográficas
            df_datos['ciudad'] = ciudad
            df_datos['latitud'] = df_datos['city.geo'][0][0]
            df_datos['longitud'] = df_datos['city.geo'][0][1]

            # Verificar que todas las ciudades tengan las mismas columnas
            for columna in LIST_COLUMNAS_DF:
                if columna not in df_datos:
                    df_datos[columna] = 0

            # Seleccionar y renombrar las columnas necesarias
            df_ciudad = df_datos[LIST_COLUMNAS_DF]
            df_ciudad.columns = LIST_NOMBRE_COLUMNAS

            # Concatenar el DataFrame de la ciudad actual al DataFrame final
            df_calidad_aire = pd.concat([df_calidad_aire, df_ciudad])
            
        except Exception as err:
            logging.error(f'No Hay datos en esa ciudad: {ciudad}')

    # Devolver el DataFrame con los datos transformados
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
    URL = f'https://api.waqi.info/feed/'

    #Extract
    datos = obtener_datos_ciudades(LIST_CIUDADES,URL,PARAMS)

    #Transform
    df_calidad_aire = transformar_datos(datos)

    if df_calidad_aire.empty:
        logging.info('Hubo un error al obtener los datos')
    else:
        # Creamos un csv
        crear_archivo(df_calidad_aire)
        logging.info('Terminado')