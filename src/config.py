import os


# Environmental variables for API keys
API_KEY_LOCATION = os.getenv("API_KEY_LOCATION")
API_KEY_AIR_QUALITY = os.getenv("API_KEY_AIR_QUALITY")

# Environmental variables for Redshift
AWS_USER = os.getenv("AWS_USER")
AWS_PASSWORD = os.getenv("AWS_PASSWORD")
AWS_HOST = os.getenv("AWS_HOST")
AWS_PORT = os.getenv("AWS_PORT")
AWS_DB = os.getenv("AWS_DB")

# Environmental variables for email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Check for null values in environmental variables
null_vars = [
    var for var in (EMAIL_PASSWORD,API_KEY_LOCATION,API_KEY_AIR_QUALITY,AWS_USER,AWS_PASSWORD,AWS_HOST,AWS_PORT,AWS_DB)
    if var is None
]

# Raise an error if any environmental variable is missing
if null_vars:
    raise ValueError("Error: Missing environmental variables")

