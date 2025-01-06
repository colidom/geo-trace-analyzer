import os
import pandas as pd
import json
from dotenv import load_dotenv


def get_csv_file(data_path):
    """Detecta automáticamente el único archivo CSV en una carpeta o valida una ruta específica de archivo CSV."""
    if os.path.isfile(data_path):
        # Si es un archivo, verificamos que sea un CSV
        if data_path.endswith(".csv"):
            return data_path
        else:
            raise ValueError(f"El archivo especificado no es un CSV: {data_path}")
    elif os.path.isdir(data_path):
        # Si es un directorio, buscamos un único archivo CSV
        csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]
        if len(csv_files) != 1:
            raise ValueError(
                f"Se esperaba un único archivo CSV en '{data_path}', pero se encontraron {len(csv_files)} archivos."
            )
        return os.path.join(data_path, csv_files[0])
    else:
        raise FileNotFoundError(f"No se encontró la ruta especificada: {data_path}")


def read_data(csv_file):
    """
    Lee un archivo CSV y devuelve un DataFrame con coordenadas filtradas
    basándose en el valor de precisión definido en las configuraciones.
    """
    # Carga las configuraciones, incluida la precisión válida
    _, _, valid_precision = load_configuration()

    # Lee el archivo CSV
    df = pd.read_csv(csv_file)

    # Filtra las filas donde la precisión es menor o igual al valor permitido
    filtered_df = df[df['precision'] <= valid_precision]

    return filtered_df


def create_directories(directories):
    """Crea múltiples directorios si no existen."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def process_secured_areas(obj, SECURED_AREAS, prox_distance):
    """Procesa las zonas protegidas"""
    for area in SECURED_AREAS:
        obj.add_safe_zone(area, prox_distance)

def load_configuration():
    """Carga las configuraciones necesarias desde las variables de entorno."""
    load_dotenv()
    proximity_distance = int(os.getenv("PROXIMITY_DISTANCE"))
    secured_areas = json.loads(os.getenv("SECURED_AREAS"))
    valid_precision = json.loads(os.getenv("VALID_PRECISION"))
    return proximity_distance, secured_areas, valid_precision


def get_directories(base_dir):
    """Devuelve las rutas de los directorios de datos y resultados."""
    data_dir = os.path.join(base_dir, "data")
    result_dir = os.path.join(base_dir, "result")
    return data_dir, result_dir