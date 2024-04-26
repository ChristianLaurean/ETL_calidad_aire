import os
import logging 
import pandas as pd
from send_email import email_alert
from RedShiftLoader import RedShiftLoader
from LocationConnector import LocationAPIConnector
from air_quality_alerts import air_quality_alerts
from AirQualityConnector import AirQualityAPIConnector
from constants import (
    LOCATION_API_BASE_URL, 
    AIR_QUALITY_API_BASE_URL, 
    LIST_COLUMN_NAMES
)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s - Message: %(message)s", datefmt="%Y-%m-%d")

# Initialize connectors
location_api_connector = LocationAPIConnector(LOCATION_API_BASE_URL)
air_quality_api_connector = AirQualityAPIConnector(AIR_QUALITY_API_BASE_URL)




def extract_location_and_air_quality(**context):
    """
    Extract location data from LocationIQ API and air quality data from OpenWaterMap API.

    Args:
        **context: Keyword arguments containing the execution date.
    """

    # Extract metadata from LocationIQ API
    logging.info("Extracting location...")
    location_metadata = location_api_connector.extract_location()
    logging.info("Location extraction complete.")

    # Extract air quality data from OpenWaterMap API
    logging.info("Extracting air quality data...")
    air_quality_api_connector.extract_air_quality(location_metadata, context["ds"])
    logging.info("Air quality data extraction complete.")




def transform_data():
    """
    Transform extracted data.
    """
    # Transform location data
    logging.info("Transforming location data...")
    transformed_location_data = location_api_connector.transform_location()
    logging.info("Location data transformation complete.")

    # Transform air quality data
    logging.info("Transforming air quality data...")
    transformed_air_quality_data = air_quality_api_connector.transform_air_quality()
    logging.info("Air quality data transformation complete.")

    # Merge location and air quality data
    logging.info("Merging location and air quality data...")
    merged_data = pd.merge(transformed_location_data, transformed_air_quality_data, on="latitude", how="inner")
    logging.info("Location and air quality data merge complete.")

    # Select relevant columns
    selected_columns_data = merged_data[LIST_COLUMN_NAMES]
        
    # Save to CSV
    logging.info("Saving transformed data to CSV...")
    selected_columns_data.to_csv("air_quality_data.csv", index=False)
    logging.info("Transformed data saved to CSV.")




def load_data_into_redshift():
    """
    Load transformed data into Redshift.
    """
    # Load data into Redshift
    logging.info("Loading transformed data into Redshift...")
    redshift_loader = RedShiftLoader()
    redshift_loader.load_data()
    logging.info("Transformed data loaded into Redshift.")




def send_air_quality_alerts():
    """
    Send air quality alerts via email.
    """
    logging.info("Generating air quality alerts...")
    alert_message = air_quality_alerts()
    if alert_message:
        logging.info("Sending air quality alerts via email...")
        email_alert(subject="Air Quality Alert", body=alert_message)
        logging.info("Air quality alerts sent via email.")

    # Clean up temporary files
    logging.info("Cleaning up temporary files...")
    for file_name in ["air_quality_data.csv", "air_data.json", "location_data.json"]:
        os.remove(file_name)
    logging.info("Temporary files cleaned up.")
