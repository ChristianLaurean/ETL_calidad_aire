CREATE TABLE calidad_aire (
    fecha_hora_medicion TIMESTAMP,
    ciudad VARCHAR(100),
    latitud FLOAT,
    longitud FLOAT,
    aqi INT,
    dominante_contaminante VARCHAR(50),
    pm10 FLOAT,
    pm25 FLOAT,
    so2 FLOAT,
    temperatura FLOAT,
    humedad_relativa FLOAT,
    presion_atmosferica FLOAT,
    punto_rocio FLOAT,
    velocidad_viento FLOAT,
    rafaga_viento FLOAT,
    fecha_hora_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(fecha_hora_medicion, ciudad)
);

