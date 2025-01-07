import os
from classes.FileSystem import FileSystem
from classes.Map import Map


def main():
    # Instanciar FileSystem y configurar el entorno
    fs = FileSystem()
    proximity_distance, secured_areas, valid_precision = FileSystem.load_configuration()
    script_dir, data_dir, result_dir = fs.setup_environment()

    # Configuración del mapa
    map_center = secured_areas[0]["coordinates"]
    map_instance = Map(map_center)

    # Carga de datos
    aggressor_data = FileSystem.read_data(FileSystem.get_csv_file(os.path.join(data_dir, "A.csv")))
    victim_data = FileSystem.read_data(FileSystem.get_csv_file(os.path.join(data_dir, "V.csv")))

    # Procesar áreas seguras y marcar datos en el mapa
    FileSystem.process_secured_areas(map_instance, secured_areas, proximity_distance)
    map_instance.check_prox_and_add_markers(victim_data, aggressor_data, proximity_distance)

    # Guardar el mapa
    map_instance.save(result_dir, "map_points.html")


if __name__ == "__main__":
    main()
