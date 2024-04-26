import json
import pandas as pd




def load_config(config_file: dict) -> dict:
    """
    Load configuration settings from a JSON file.

    Args:
        config_file (dict): The file config json

    Returns:
        dict: A dictionary containing the configuration settings loaded from the file.
    """
    
    with open(config_file) as file:
        config = json.load(file)
    return config




def generate_alerts(data: pd.DataFrame, config: dict) -> str:
    """
    Generate alerts based on air quality data and configuration settings.

    Args:
        data (pd.DataFrame): The air quality data as a pandas DataFrame.
        config (dict): The configuration settings loaded from a JSON file.

    Returns:
        str: A string containing the generated alerts.
    """

    # Filter the data for the specified cities in the configuration
    city_data = data[data["city_name"].isin(config["cities"])]
    alerts = []

    # Iterate over the contaminants and check if any exceeds the configured limits
    for contaminant, limits in config["contaminants"].items():
        min_limit = limits["min"]
        max_limit = limits["max"]
        
        # Check if any value exceeds the configured limits
        for city, value, timestamp in city_data[["city_name", contaminant, "measurement_hour"]].values:
            if value >= max_limit:
                # Generate an alert if the value exceeds the maximum limit
                alerts.append(f"Alert: {timestamp} - The value of {contaminant} ({value}) exceeds the permitted limits in {city}.")
            elif value <= min_limit:
                # Generate an alert if the value is below the minimum limit
                alerts.append(f"Alert: {timestamp} - The value of {contaminant} ({value}) is at the minimum permitted limits in {city}.")

    return "\n".join(alerts)




def air_quality_alerts() -> str:
    """
    Generate air quality alerts based on configuration settings and air quality data.

    Returns:
        str: A string containing the generated alerts.
    """
    # Load the air quality data from the CSV file
    data = pd.read_csv("air_quality_data.csv")
    # Load the configuration settings
    config = load_config("src/alert_config.json")
    # Generate alerts based on the loaded data and configuration
    alerts = generate_alerts(data, config)

    
    return alerts
