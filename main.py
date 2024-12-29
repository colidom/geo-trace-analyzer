from dotenv import load_dotenv
import os
from utils.filesystem import get_csv_file, read_data, create_directories
from utils.map import Map


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

    map_view = Map((secured_area_lat, secured_area_lng))
    map_view.add_safe_zone((secured_area_lat, secured_area_lng), prox_distance)
    map_view.check_prox_and_add_markers(victim_data, aggressor_data, prox_distance)
    map_view.save(result_folder, output_map)


if __name__ == "__main__":
    main()
