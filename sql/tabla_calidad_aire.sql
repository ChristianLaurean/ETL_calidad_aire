CREATE TABLE air_quality (
    measurement_hour TIMESTAMP,
    city_name VARCHAR(50),
    country_name VARCHAR(50),
    aqi INT,
    co FLOAT,
    no FLOAT,
    no2 FLOAT,
    o3 FLOAT,
    so2 FLOAT,
    pm2_5 FLOAT,
    pm10 FLOAT,
    nh3 FLOAT,
    type_location VARCHAR(50),
    importance_location VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    extraction_date DATE,
    load_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(measurement_hour, city_name)
);



