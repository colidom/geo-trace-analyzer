import os
from dotenv import load_dotenv
from utils.filesystem import get_csv_file, read_data, create_directories
from utils.map import (
    initialize_map,
    add_safe_zone,
    save_map,
    check_prox_and_add_markers,
)


def main():
    load_dotenv()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    data_folder = os.path.join(script_dir, "data")
    result_folder = os.path.join(script_dir, "result")
    output_map = "map_points.html"
    create_directories([data_folder, result_folder])

    prox_distance = int(os.getenv("PROXIMITY_DISTANCE"))
    secured_area_str = os.getenv("SECURED_AREA")
    secured_area_lat, secured_area_lng = map(float, secured_area_str.split(","))

    aggressor_file = get_csv_file(os.path.join(data_folder, "A.csv"))
    victim_file = get_csv_file(os.path.join(data_folder, "V.csv"))
    aggressor_data = read_data(aggressor_file)
    victim_data = read_data(victim_file)
    map_view = initialize_map((secured_area_lat, secured_area_lng))

    add_safe_zone(map_view, (secured_area_lat, secured_area_lng), prox_distance)
    check_prox_and_add_markers(map_view, victim_data, aggressor_data, prox_distance)
    save_map(map_view, result_folder, output_map)


if __name__ == "__main__":
    main()
