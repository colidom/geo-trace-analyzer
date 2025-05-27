from geopy.distance import geodesic
from functools import lru_cache

# Constants for error messages
INVALID_LOCATION_MSG = "Ubicación no válida en '{column}': {value}. Ignorando fila."
UNEXPECTED_TYPE_MSG = "Valor inesperado en '{column}': {value}. Ignorando fila."


@lru_cache(maxsize=1024)
def calculate_distance(coord1, coord2):
    """
    Calculates the distance in meters between two geographic coordinates using the geopy library.
    :param coord1: Tuple (latitude, longitude) of the first point.
    :param coord2: Tuple (latitude, longitude) of the second point.
    :return: Distance in meters between the two points.
    """
    return geodesic(coord1, coord2).meters


def validate_location(location, column):
    """
    Validates the location value, ensuring it is a string and not a float.
    :param location: The value of the location column.
    :param column: The name of the location column.
    :return: True if the location is valid, otherwise logs an error and returns False.
    """
    if isinstance(location, float):
        print(UNEXPECTED_TYPE_MSG.format(column=column, value=location))
        return False
    return True


def parse_coordinates(location, column):
    """
    Parses a location string into latitude and longitude.
    :param location: The location string to parse.
    :param column: The name of the location column.
    :return: Tuple (latitude, longitude) if parsing succeeds, otherwise logs an error and returns None.
    """
    try:
        return tuple(map(float, location.split(",")))
    except ValueError:
        print(INVALID_LOCATION_MSG.format(column=column, value=location))
        return None


def extract_coordinates(row, column="location"):
    """
    Extracts geographic coordinates from a data row, handling errors gracefully.
    :param row: The data row containing the location information.
    :param column: The column name where the location string is located.
    :return: Tuple (latitude, longitude) if valid, otherwise None.
    """
    location = row.get(column)
    if location is None or not validate_location(location, column):
        return None
    return parse_coordinates(location, column)
