import time
import logging
import requests
import pandas as pd
from random import choice
from config import API_KEY_AIR_QUALITY
from datetime import datetime, timedelta
from constants import LIST_NUMBERS, LIST_COLUMN_NAMES_AIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s - Message: %(message)s", datefmt="%Y-%m-%d")




class AirQualityAPIConnector:

    def __init__(self, url_base: str) -> None:
        """
        Initializes the AirQualityAPIConnector object.

        Args:
            url_base (str): The base URL of the OpenWaterMap API.
        """
        self.url_base = url_base




    def get_air_quality(self, latitude: str, longitude: str, start: int, end: int) -> dict:
        """
        Fetches air quality data from the OpenWaterMap API for a given location and time range.

        Args:
            latitude (str): The latitude of the location.
            longitude (str): The longitude of the location.
            start (int): The start timestamp for the data query.
            end (int): The end timestamp for the data query.

        Returns:
            dict: The air quality data in JSON format.
        """
        params = {
            "lat": latitude,
            "lon": longitude,
            "start": start,
            "end": end,
            "appid": API_KEY_AIR_QUALITY
        }
        try:
            response = requests.get(self.url_base, params=params)
            response.raise_for_status()
            return response.json()["list"]
        except requests.exceptions.RequestException as err:
            logging.error(f"Error querying the API: {err}")
            return {}




    def extract_air_quality(self, df_metadata: pd.DataFrame, date: str) -> None:
        """
        Extracts air quality data from OpenWaterMap for multiple locations and saves it to a JSON file.

        Args:
            df_metadata (pd.DataFrame): DataFrame containing latitude and longitude of locations.
            date (str): The date for which to extract air quality data.

        """
        date_object = datetime.strptime(date, "%Y-%m-%d")
        date_plus_22_hours = date_object + timedelta(hours=22)
        unix_start = int(date_object.timestamp())
        unix_end = int(date_plus_22_hours.timestamp())

        df_air_quality = pd.DataFrame()
        for location in df_metadata.values:
            air_quality_data = self.get_air_quality(location[0], location[1], str(unix_start), str(unix_end))
            if air_quality_data:
                air_quality_df = pd.json_normalize(air_quality_data)
                air_quality_df["lat"] = location[0]
                df_air_quality = pd.concat([df_air_quality, air_quality_df])
            time.sleep(choice(LIST_NUMBERS))

        df_air_quality.reset_index(drop=True, inplace=True)
        df_air_quality.to_json("air_data.json")
        logging.info(f"Successfully Extracted air quality data: {df_air_quality.shape}")




    def transform_air_quality(self) -> pd.DataFrame:
        """
        Transforms the extracted air quality data.

        Returns:
            pd.DataFrame: Transformed air quality data DataFrame.
        """
        try:
            df_air = pd.read_json("air_data.json")
            df_air["dt"] = pd.to_datetime(df_air["dt"], unit='s')
            df_air.columns = LIST_COLUMN_NAMES_AIR
            logging.info("Successfully transformed DataFrame")
            logging.info(f"Shape of transformed DataFrame: {df_air.shape}")
            return df_air
        except Exception as e:
            logging.error(f"Error transforming DataFrame: {e}")
            return pd.DataFrame()
