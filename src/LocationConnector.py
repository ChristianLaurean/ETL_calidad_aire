import time
import logging
import requests
import pandas as pd
from random import choice
from config import API_KEY_LOCATION
from constants import (
    DICT_CITIES, 
    LIST_NUMBERS, 
    LIST_COLUMN_NAMES_LOCATION
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s - Message: %(message)s", datefmt="%Y-%m-%d")




class LocationAPIConnector:
    def __init__(self, base_url: str) -> None:
        """
        Initialize the LocationAPIConnector instance.

        Parameters:
            base_url (str): The base URL for the LocationIQ API.
        """
        self.base_url = base_url




    def get_location_data(self, city: str, country_code: str) -> dict:
        """
        Get location data for a specific city.

        Parameters:
            city (str): The name of the city.
            country_code (str): The country code.

        Returns:
            dict: Location data for the specified city.
        """
        params = {
            "city": city,
            "format": "json",
            "countrycodes": country_code,
            "key": API_KEY_LOCATION
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()[0]
        except requests.exceptions.RequestException as err:
            logging.error(f"Error querying the API {err}")
            return {}

        
    



    def extract_location(self) -> pd.DataFrame:
        """
        Extract location data for multiple cities.

        Returns:
            pd.DataFrame: DataFrame containing location data for all cities.
        """
        df_city = pd.DataFrame()
        for city, code in DICT_CITIES.items():
            logging.info(f"Extracting data for: {city}")

            df_city_code = pd.json_normalize(self.get_location_data(city, code))
            df_city = pd.concat([df_city, df_city_code])
            time.sleep(choice(LIST_NUMBERS))

        df_city.reset_index(drop=True, inplace=True)
        df_city.to_json("location_data.json")
        logging.info(f"Successfully Extracted Location data: {df_city.shape}")

        return df_city[["lat", "lon"]]




    def transform_location(self) -> pd.DataFrame:
        """
        Transform the extracted location data.

        Returns:
            pd.DataFrame: Transformed location data DataFrame.
        """
        
        try:
            df = pd.read_json("location_data.json")
            df_location = df.iloc[:, 5:-1].copy()
            df_location["city_name"] = df_location["display_name"].apply(lambda x: x.split(",")[0])
            df_location["country_name"] = df_location["display_name"].apply(lambda x: x.split(",")[-1])
            df_location.columns = LIST_COLUMN_NAMES_LOCATION
            
            logging.info("Successfully transformed DataFrame")
            logging.info(f"Shape of transformed DataFrame: {df_location.shape}")
            return df_location
        except Exception as e:
            logging.error(f"Error transforming DataFrame: {e}")
            return pd.DataFrame()


        
