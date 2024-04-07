import pandas as pd
import requests
import os
import logging
import psycopg2
from dotenv import load_dotenv
# importamos el tipo de dato
from typing import Generator
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from constants import LIST_COLUMNAS_DF, LIST_NOMBRE_COLUMNAS, LIST_CIUDADES, URL, PARAMS




class ETLdeCalidadAire:


    def __init__(self,url_base : str, params : dict):
        self.url_base = url_base
        self.params = params




    def extraer_datos_api(self, ciudad : str)-> dict:
        """
        Consultar una API para obtener datos sobre la calidad del aire.

        Args:
            ciudad (str): Es el endpoint de la url.

        Returns:
            dict: Datos de calidad del aire en formato json.
        """
        try:

            response = requests.get(self.url_base+ciudad,params=self.params)
            response.raise_for_status()
            return response.json()['data']
        
        except requests.exceptions.RequestException as err:
            logging.error(f'Error al consultar la API: {err}')
        
    


    def obtener_datos_ciudades(self, ciudades:list)-> Generator:
        """
        Extrae los datos de calidad del aire para las ciudades especificadas.

        Args:
            ciudades (list): Lista de nombres de ciudades.

        Yield:
            Generator[Tuple[dict, str]: Generador que produce tuplas donde el primer elemento
                                                    es un diccionario de datos de calidad del aire y el segundo
                                                    elemento es el nombre de la ciudad correspondiente.
        """

        for ciudad in ciudades:
            logging.info(f'Extraemos los datos...{ciudad}')
            #Extraemos los datos de la Api por ciudad.
            dict_datos = self.extraer_datos_api(ciudad)

            yield dict_datos, ciudad




    def transformar_datos(self,datos:Generator) -> pd.DataFrame:
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

                # Convertir la columna 'Fecha_Hora_Medicion' a objetos Timestamp
                df_calidad_aire['fecha_hora_medicion'] = pd.to_datetime(df_calidad_aire['fecha_hora_medicion'])
                
        
            except Exception as err:
                logging.error(f'No Hay datos en esa ciudad: {ciudad}')

        # Devolver el DataFrame con los datos transformados
        return df_calidad_aire
        
        


class RedShift:


    def establecer_conexion_db(self) -> object:
        """
        Establece una conexión con la base de datos.

        Returns:
            object: Objeto de sesión de la base de datos.
        """
        try:
            engine = create_engine(f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB')}")
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except Exception as e:
            logging.error("Error al conectarse a la base de datos:", e)




    def cargar_datos_nuevos(self,df_nuevos_datos : pd.DataFrame, session : object) -> pd.DataFrame:
        """
        Carga los nuevos datos en el DataFrame.

        Args:
            df_nuevos_datos (pd.DataFrame): DataFrame que contiene los nuevos datos a cargar.
            session (object): Objeto de sesión de la base de datos.

        Returns:
            pd.DataFrame: DataFrame con los nuevos datos.
        """
        # query a redshift
        datos_existentes_db = pd.read_sql_query("SELECT fecha_hora_medicion, ciudad FROM calidad_aire", session)

        # Unimos los datos que se encuentren en la tabla de Redshift y de mi DataFrame medianto las clave compeusta
        df_existente = df_nuevos_datos.merge(datos_existentes_db, on=['fecha_hora_medicion', 'ciudad'])

        #filtramos los datos que ya se encuentran en la db y retornamos los datos que no están en la db
        datos_nuevos = df_nuevos_datos[~df_nuevos_datos.set_index(['fecha_hora_medicion', 'ciudad']).index.isin(df_existente.set_index(['fecha_hora_medicion', 'ciudad']).index)]

        return datos_nuevos




    def cargar_datos(self,df_calidad_aire: pd.DataFrame):
        """
        Carga los datos en la base de datos.

        Args:
            df_calidad_aire (pd.DataFrame): DataFrame que contiene los datos a cargar.
        """
        logging.info('cargando los datos a Redshift')
        
        session = self.establecer_conexion_db()
        try:
            #si no hay datos en la db se insertan.
            df_registros = pd.read_sql_query(f"SELECT * FROM calidad_aire LIMIT 1", session.bind)

            if len(df_registros) == 0:
                df_calidad_aire.to_sql('calidad_aire', session.bind, if_exists='append', index=False)
                logging.info('Datos insertados exitosamente')

            else:
                # insertamos los datos nuevos a la db
                self.cargar_datos_nuevos(df_calidad_aire, session.bind).to_sql('calidad_aire', session.bind, if_exists='append', index=False)
                logging.info('Datos insertados exitosamente')

        except TypeError as e:
            logging.error("Error durante la carga de datos:", e)
        finally:
            session.close()
            logging.info('Conexión cerrada')




if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s - Message: %(message)s", datefmt="%Y-%m-%d")
    load_dotenv()

    #Extract
    conector = ETLdeCalidadAire(URL, PARAMS)
    datos = conector.obtener_datos_ciudades(LIST_CIUDADES)

    #Transform
    df_calidad_aire = conector.transformar_datos(datos)

    if df_calidad_aire.empty:
    
        logging.info('Hubo un error al obtener los datos')

    else:
        #carga

        cargar_datos_redshift = RedShift()
        cargar_datos_redshift.cargar_datos(df_calidad_aire)

        logging.info('Terminado')