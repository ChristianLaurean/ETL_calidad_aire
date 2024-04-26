# Urls base
AIR_QUALITY_API_BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"
LOCATION_API_BASE_URL = 'https://us1.locationiq.com/v1/search/structured'
LIST_NUMBERS = [1,2,3]
EMAIL_SENDER = "christianlaurean1@gmail.com"
EMAIL_RECIPIENT = "christianlaurean1@gmail.com"

LIST_COLUMN_NAMES_LOCATION = [
    "latitude",
    "longitude",
    "display_name",
    "class",
    "type_location",
    "importance_location",
    "city_name",
    "country_name"
]


LIST_COLUMN_NAMES_AIR = [
    "measurement_hour",
    "aqi",
    "co",
    "no",
    "no2",
    "o3",
    "so2",
    "pm2_5",
    "pm10",
    "nh3",
    "latitude",
    "extraction_date"
]

LIST_COLUMN_NAMES = [
    "measurement_hour",
    "city_name",
    "country_name",
    "aqi",
    "co",
    "no",
    "no2",
    "o3",
    "so2",
    "pm2_5",
    "pm10",
    "nh3",
    "type_location",
    "importance_location",
    "latitude",
    "longitude",
    "extraction_date"
]



DICT_CITIES = {
    'Guadalajara': 'MX',
    'Monterrey' : 'MX',
    'Mexico City': 'MX',
    'Puebla' : 'MX',
    'Merida' : 'MX',
    'Toluca' : 'MX',
    'Buenos Aires' : 'AR',
    'Medellin' : 'CO'
}


