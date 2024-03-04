CREATE TABLE calidad_aire (
    Fecha_Hora_Medicion DATETIME,
    AQI INT,
    Dominante_Contaminante VARCHAR(50),
    PM10 FLOAT,
    PM2_5 FLOAT,
    SO2 FLOAT,
    Temperatura FLOAT,
    Humedad_Relativa FLOAT,
    Presion_Atmosferica FLOAT,
    Punto_Rocio FLOAT,
    Velocidad_Viento FLOAT,
    Rafaga_Viento FLOAT,
    Ciudad VARCHAR(100),
    Latitud FLOAT,
    Longitud FLOAT,
    Fecha_Hora_Carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_carga VARCHAR(100)
);
