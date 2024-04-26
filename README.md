# Proyecto: Calidad del Aire

Este proyecto se centra en la extracción, transformación y carga de datos sobre la calidad del aire en diversas ciudades utilizando las APIs proporcionadas por [OpenWeatherMap](https://openweathermap.org/) y [LocationIQ](https://es.locationiq.com/).

## Descripción del Proyecto

La calidad del aire es un factor crítico que influye en la salud y el bienestar de las comunidades urbanas en todo el mundo. Este proyecto se enfoca en la extracción, transformación y carga de datos sobre la calidad del aire en ciudades específicas utilizando las APIs de [OpenWeatherMap](https://openweathermap.org/) y [LocationIQ](https://es.locationiq.com/). La combinación de estos dos conjuntos de datos enriquece la comprensión y el análisis de la calidad del aire al incorporar información tanto meteorológica como geográfica.

![img_air](https://github.com/ChristianLaurean/ETL_calidad_aire/blob/main/assets/img_air.jpg)

#### Niveles de Calidad del Aire

| AQI | Nivel de contaminación del aire       | Implicaciones para la salud                                                                                                                                                   |
| --- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Buena                                 | La calidad del aire es satisfactoria y la contaminación del aire representa poco o ningún riesgo para la salud.                                                               |
| 2   | Moderada                              | La calidad del aire es aceptable; sin embargo, puede haber una preocupación para un pequeño grupo de personas que son excepcionalmente sensibles a la contaminación del aire. |
| 3   | Dañina a la salud en grupos sensibles | Los miembros de grupos sensibles pueden experimentar efectos en la salud. La población en general no está en riesgo.                                                          |
| 4   | Dañina a la salud                     | Todos pueden comenzar a experimentar efectos en la salud; las personas en grupos sensibles pueden experimentar efectos más serios en la salud.                                |
| 5   | Muy dañina a la salud                 | Advertencia de salud: más efectos de salud esperados.                                                                                                                         |

### Objetivos del Proyecto:

- Proporcionar información actualizada sobre la calidad del aire en ciudades específicas.
- Analizar y comprender los factores que influyen en la calidad del aire, incluyendo datos meteorológicos y geográficos.
- Automatizar el proceso de extracción, transformación y carga de datos para garantizar la actualización continua de la información.

### Arquitectura del Proyecto

El siguiente diagrama ilustra la arquitectura de la canalización de datos de un extremo a otro:

![diagram](https://github.com/ChristianLaurean/ETL_calidad_aire/blob/main/assets/diagramETL.png)

### Componentes de la Arquitectura:

- Extracción de Datos: Utiliza las APIs de OpenWeatherMap y LocationIQ para obtener datos sobre la calidad del aire, datos meteorológicos y datos geográficos.
- Transformación de Datos: Utiliza el procesamiento de datos con Pandas para limpiar, transformar y combinar los datos obtenidos.
- Carga de Datos: Almacena los datos transformados en Amazon Redshift para su análisis y consulta posterior.
-

### Tecnologías Utilizadas

- Orquestación del flujo de trabajo: _Apache Airflow_
- Procesamiento de datos: _Pandas_
- Almacenamiento de datos: _Amazon Redshift_

## Instalación

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener tus claves de API de OpenWeatherMap y LocationIQ configuradas en un archivo .env en la raíz del proyecto.
3. Configuración del Archivo .env: Define las variables de entorno necesarias en el archivo .env con la siguiente estructura:
   ```
   AIRFLOW_UID=1000
   OPENWEATHERMAP_API_KEY=""
   LOCATIONIQ_API_KEY=""
   # Variables para Redshift
   AWS_USER=""
   AWS_PASSWORD=""
   AWS_HOST=""
   AWS_PORT=
   AWS_DB=""
   EMAIL_PASSWORD=""
   ```
   **Nota importante:** No olvides configurar tu dirección de correo electrónico (`EMAIL_PASSWORD=""`) para recibir notificaciones sobre el estado del proyecto. Asegúrate de definir las variables `EMAIL_SENDER` y `EMAIL_RECIPIENT` en el archivo `constants.py` con tus direcciones de correo electrónico.

# Ejecución del Proyecto

Inicia Apache Airflow utilizando Docker Compose con el siguiente comando:

```bash
docker-compose up airflow-init
```

```bash
docker-compose --env-file .env up --build -d
```

## Uso Continuo

Una vez configurado y ejecutado, el proyecto se ejecutará automáticamente todos los días a las 10 de la noche para extraer los datos del día y enviar alertas por correo electrónico si es necesario.
