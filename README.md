# GeoTrace Analyzer

GeoTrace Analyzer es una herramienta avanzada para visualizar y analizar datos geográficos. Está diseñada para rastrear ubicaciones, calcular distancias y determinar la proximidad entre entidades como víctimas, agresores y zonas seguras.

## Características principales

-   Representación de coordenadas geográficas en un mapa interactivo.
-   Cálculo de distancias entre diferentes puntos.
-   Detección de proximidad a zonas seguras.
-   Generación de mapas HTML fáciles de compartir.

## Requisitos previos

-   Python 3.8 o superior.
-   Librerías especificadas en `requirements.txt`.
-   Archivo `.env` con las configuraciones necesarias.

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu-usuario/geotrace-analyzer.git
    cd geotrace-analyzer
    ```

2. Crea un entorno virtual y actívalo:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura el archivo `.env` en el directorio principal:
    ```env
    SECURED_AREA_LAT=28.413966
    SECURED_AREA_LNG=-16.548123
    PROXIMITY_DISTANCE=200  # Distancia en metros
    ```

## Estructura del proyecto

```plaintext
GeoTrace Analyzer/
│
├── data/                  # Archivos CSV con datos de entrada
├── result/                # Salida de mapas generados
├── utils/                 # Módulos auxiliares
│   ├── filesystem.py      # Gestión de archivos
│   ├── map.py             # Funciones de manipulación de mapas
│   ├── distance.py        # Cálculos de distancia
├── .env                   # Configuración de variables de entorno
├── requirements.txt       # Dependencias del proyecto
├── main.py                # Script principal
└── README.md              # Documentación del proyecto
```

## Uso

1. Añade tus datos en formato CSV a la carpeta `data/`.

    - `A.csv` para datos del agresor.
    - `V.csv` para datos de la víctima.

2. Ejecuta el script principal:

    ```bash
    python main.py
    ```

3. El mapa generado se guardará en la carpeta `result/` como `map_points.html`.

## Ejemplo de entrada

### Formato requerido para los ficheros CSV:

Los archivos deben tener las siguientes columnas: `time`, `precision`, y `location` (coordenadas en formato "latitud,longitud").

#### Archivo `A.csv` (Agresores):

```csv
"time","precision","location"
"2024-12-20 22:05:20",4.5,"28.416768,-16.553500"
"2024-12-20 22:14:57",0.0,"28.417200,-16.553600"
"2024-12-20 22:14:59",4.5,"28.417800,-16.554000"
"2024-12-20 22:22:59",4.5,"28.418400,-16.554400"
"2024-12-20 22:26:44",4.5,"28.418900,-16.554800"
"2024-12-20 22:37:45",11.8,"28.419500,-16.555200"
"2024-12-20 22:37:46",11.8,"28.420000,-16.555600"
```

#### Archivo `V.csv` (Víctimas):

```csv
"time","precision","location"
"2024-12-20 22:10:20",3.0,"28.415500,-16.552900"
"2024-12-20 22:15:50",4.2,"28.416000,-16.553300"
"2024-12-20 22:20:30",5.0,"28.416500,-16.553700"
```

## Personalización

-   Cambia las coordenadas de la zona segura en el archivo `.env`.
-   Modifica el radio de proximidad (`PROXIMITY_DISTANCE`) según tus necesidades.

## Ejemplo visual

<img src="example_map.png" alt="Mapa generado" width="600">

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras errores o tienes sugerencias, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia GNU GENERAL PUBLIC LICENSE. Consulta el archivo `LICENSE` para más detalles.
