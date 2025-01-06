import os
from utils.filesystem import (
    get_csv_file,
    read_data,
    create_directories,
    process_secured_areas,
    load_configuration,
    get_directories
)
from classes.Map import Map


def main():
    # Configurar entorno
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Preparar configuración y directorios
    proximity_distance, secured_areas, valid_precision = load_configuration()
    data_dir, result_dir = get_directories(script_dir)
    create_directories([data_dir, result_dir])

    # Configuración del mapa
    map_center = secured_areas[0]["coordinates"]
    map_instance = Map(map_center)

    # Carga de datos
    aggressor_data = read_data(get_csv_file(os.path.join(data_dir, "A.csv")))
    victim_data = read_data(get_csv_file(os.path.join(data_dir, "V.csv")))

    # Procesar áreas seguras y marcar datos en el mapa
    process_secured_areas(map_instance, secured_areas, proximity_distance)
    map_instance.check_prox_and_add_markers(victim_data, aggressor_data, proximity_distance)

    # Guardar el mapa
    map_instance.save(result_dir, "map_points.html")


if __name__ == "__main__":
    main()
