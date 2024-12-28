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

### Archivo `A.csv` (Agresores)

```csv
location,time,precision
28.416768,-16.552114,2023-12-01 08:30:00,5
28.418540,-16.551460,2023-12-01 08:45:00,3
```

### Archivo `V.csv` (Víctimas)

```csv
location,time,precision
28.414500,-16.550950,2023-12-01 08:30:00,4
28.415200,-16.549800,2023-12-01 08:50:00,2
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
