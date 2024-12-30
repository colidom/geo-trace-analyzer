import os
import pandas as pd


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
    """Lee un archivo CSV y lo devuelve como un DataFrame."""
    return pd.read_csv(csv_file)


def create_directories(directories):
    """Crea múltiples directorios si no existen."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def process_secured_areas(obj, SECURED_AREAS, prox_distance):
    """Procesa las zonas protegidas"""
    for area in SECURED_AREAS:
        obj.add_safe_zone(area, prox_distance)
