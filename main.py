from classes.FileSystem import FileSystem
from classes.Map import Map
from src.utils import choose_file

def main():
    fs = FileSystem()
    
    # Cargar la configuración
    proximity_distance, secured_areas, _ = FileSystem.load_configuration()
    
    # Configurar el entorno de trabajo
    _, data_dir, result_dir = fs.setup_environment()

    aggressor_file = choose_file("AGRESORES")
    victim_file = choose_file("VÍCTIMAS")

    # Leer datos desde los ficheros seleccionados
    aggressor_data = FileSystem.read_data(FileSystem.get_csv_file(aggressor_file))
    victim_data = FileSystem.read_data(FileSystem.get_csv_file(victim_file))

    # Buscar la primera área segura activa y usarla para centrar el mapa
    active_area = next((area for area in secured_areas if area['active']), None)

    if active_area:
        map_center = active_area["coordinates"]
    else:
        first_aggressor_location = aggressor_data.iloc[0]['location'].split(',')
        map_center = [float(first_aggressor_location[0]), float(first_aggressor_location[1])]

    # Crear el mapa
    map_instance = Map(map_center)

    # Procesar áreas seguras y marcar datos en el mapa
    FileSystem.process_secured_areas(map_instance, secured_areas, proximity_distance)
    map_instance.check_prox_and_add_markers(victim_data, aggressor_data, proximity_distance)

    # Guardar el mapa
    map_instance.save(result_dir, "map_points.html")


if __name__ == "__main__":
    main()
