import os
import json
from dotenv import load_dotenv
from utils.filesystem import (
    get_csv_file,
    read_data,
    create_directories,
    process_secured_areas,
)
from classes.Map import Map


def main():
    load_dotenv()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    data_folder = os.path.join(script_dir, "data")
    result_folder = os.path.join(script_dir, "result")
    output_map = "map_points.html"
    create_directories([data_folder, result_folder])

    prox_distance = int(os.getenv("PROXIMITY_DISTANCE"))
    secured_areas_str = os.getenv("SECURED_AREAS")
    SECURED_AREAS = json.loads(secured_areas_str)
    coordinates = SECURED_AREAS[0]["coordinates"]

    aggressor_file = get_csv_file(os.path.join(data_folder, "A.csv"))
    victim_file = get_csv_file(os.path.join(data_folder, "V.csv"))
    aggressor_data = read_data(aggressor_file)
    victim_data = read_data(victim_file)

    map = Map(coordinates)

    process_secured_areas(map, SECURED_AREAS, prox_distance)

    map.check_prox_and_add_markers(victim_data, aggressor_data, prox_distance)
    map.save(result_folder, output_map)


if __name__ == "__main__":
    main()
