# Proyecto: Calidad del Aire en ciudades

Este proyecto se centra en la extracción, transformación y carga de los datos sobre la calidad del aire en diversas ciudades utilizando la API proporcionada por [AQICN](https://aqicn.org/json-api/doc/).

## Descripción del Proyecto

La calidad del aire es un factor importante que afecta la salud y el bienestar de las personas. Este proyecto utiliza datos en tiempo real de la API de AQICN para proporcionar información actualizada sobre los niveles de contaminación atmosférica en ciudades específicas.

#### Niveles de Calidad del Aire

| AQI     | Nivel de contaminación del aire       | Implicaciones para la salud                                                                                                                                                   |
| ------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0-50    | Buena                                 | La calidad del aire es satisfactoria y la contaminación del aire representa poco o ningún riesgo para la salud.                                                               |
| 51-100  | Moderada                              | La calidad del aire es aceptable; sin embargo, puede haber una preocupación para un pequeño grupo de personas que son excepcionalmente sensibles a la contaminación del aire. |
| 101-150 | Dañina a la salud de grupos sensibles | Los miembros de grupos sensibles pueden experimentar efectos en la salud. La población en general no está en riesgo.                                                          |
| 151-200 | Dañina a la salud                     | Todos pueden comenzar a experimentar efectos en la salud; las personas en grupos sensibles pueden experimentar efectos más serios en la salud.                                |
| 201-300 | Muy dañina a la salud                 | Advertencia de salud: más efectos de salud esperados.                                                                                                                         |
| 301-500 | Peligroso                             | Alerta de emergencia de salud: la población en general es más probable que se vea afectada.                                                                                   |

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

# Uso

- Asegúrate de tener tu API_KEY de [AQICN](https://aqicn.org/data-platform/token/es/) configurada en un archivo .env en la raíz del proyecto.
- Ejecuta el script principal main.py para extraer, transformar y exportar los datos de calidad del aire.
