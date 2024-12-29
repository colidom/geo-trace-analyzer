import folium
import os
from utils.distance import calculate_distance, process_location


def initialize_map(center, zoom_start=15):
    """Inicializa un mapa centrado en una ubicación específica."""
    return folium.Map(location=center, zoom_start=zoom_start)


def add_safe_zone(map_object, secured_area, proximity_distance):
    """Agrega un marcador y un círculo de proximidad para la zona segura con información detallada."""
    lat, lng = secured_area
    tooltip_text = f"<b>Lon:</b> {lng}<br>" f"<b>Lat:</b> {lat}<br>"

    # Agregar marcador para la zona segura
    folium.Marker(
        location=secured_area,
        tooltip=tooltip_text,
        icon=folium.Icon(color="blue", icon="home", prefix="fa"),
    ).add_to(map_object)

    # Agregar círculo para la zona de proximidad de la zona segura
    folium.Circle(
        location=secured_area,
        radius=proximity_distance,
        color="blue",
        fill=True,
        fill_opacity=0.2,
        tooltip=f"Secured Area: {proximity_distance}m",
    ).add_to(map_object)


def save_map(map_object, result_folder, output_file):
    """Guarda el mapa en un archivo HTML."""
    os.makedirs(result_folder, exist_ok=True)
    map_object.save(os.path.join(result_folder, output_file))
    print(f"Mapa generado exitosamente: {os.path.join(result_folder, output_file)}")


def verify_location(location):
    # Verificar si location es un número flotante o una cadena
    if isinstance(location, str):
        # Si es una cadena, intentamos dividirla
        lat, lng = map(float, location.split(","))
        return lat, lng
    elif isinstance(location, float):
        # Si es un flotante, lo ignoramos o realizamos algún tipo de procesamiento (si corresponde)
        print(f"Valor inesperado en 'location': {location}")
    else:
        print(f"Tipo no esperado en 'location': {type(location)}")


def check_prox_and_add_markers(
    map_view, victim_data, aggressor_data, proximity_distance
):
    """
    Verifica la proximidad de las víctimas con los agresores y añade marcadores al mapa
    solo si hay un agresor dentro del área de proximidad de la víctima.
    También dibuja el recorrido de los agresores.
    """
    # Procesar víctimas y añadir sus marcadores
    victim_positions = process_victims(
        map_view, victim_data, aggressor_data, proximity_distance
    )

    # Procesar agresores y añadir sus marcadores
    aggressor_positions = process_aggressors(map_view, aggressor_data)

    # Dibujar el recorrido de los agresores
    draw_aggressor_path(map_view, aggressor_positions)


def process_victims(map_view, victim_data, aggressor_data, proximity_distance):
    """
    Procesa las víctimas, verifica la proximidad con agresores, y añade marcadores.
    """
    victim_position = 1
    for _, victim_row in victim_data.iterrows():
        victim_coordinates = process_location(victim_row, location_column="location")

        if victim_coordinates:
            victim_lat, victim_lng = victim_coordinates
            aggressor_nearby = check_prox_and_add_circle(
                map_view, victim_lat, victim_lng, aggressor_data, proximity_distance
            )

            if aggressor_nearby:
                add_marker(
                    map_view,
                    victim_position,
                    victim_lat,
                    victim_lng,
                    victim_row,
                    "victim",
                )

            victim_position += 1


def process_aggressors(map_view, aggressor_data):
    """
    Procesa los agresores, añade marcadores, y devuelve sus posiciones.
    """
    aggressor_positions = []
    aggressor_position = 1

    for _, aggressor_row in aggressor_data.iterrows():
        aggressor_coordinates = process_location(
            aggressor_row, location_column="location"
        )

        if aggressor_coordinates:
            aggressor_lat, aggressor_lng = aggressor_coordinates
            aggressor_positions.append((aggressor_lat, aggressor_lng))
            add_marker(
                map_view,
                aggressor_position,
                aggressor_lat,
                aggressor_lng,
                aggressor_row,
                "aggressor",
            )

            aggressor_position += 1

    return aggressor_positions


def draw_aggressor_path(map_view, aggressor_positions):
    """
    Dibuja el recorrido de los agresores si hay más de una posición.
    """
    if len(aggressor_positions) > 1:
        folium.PolyLine(aggressor_positions, color="red", weight=2.5, opacity=1).add_to(
            map_view
        )


def check_prox_and_add_circle(
    map_view, victim_lat, victim_lng, aggressor_data, proximity_distance
):
    """
    Verifica si algún agresor está dentro de la proximidad de la víctima y añade un círculo.
    """
    for _, aggressor_row in aggressor_data.iterrows():
        aggressor_coordinates = process_location(
            aggressor_row, location_column="location"
        )

        if aggressor_coordinates:
            aggressor_lat, aggressor_lng = aggressor_coordinates
            distance = calculate_distance(
                (victim_lat, victim_lng), (aggressor_lat, aggressor_lng)
            )

            if distance <= proximity_distance:
                folium.Circle(
                    location=(victim_lat, victim_lng),
                    radius=proximity_distance,
                    color="orange",
                    fill=True,
                    fill_opacity=0.1,
                    tooltip=f"Proximity Alert: {distance:.2f}m",
                ).add_to(map_view)
                return True

    return False


def add_marker(map_view, position, lat, lng, row, marker_type):
    """
    Añade un marcador genérico al mapa, ya sea para una víctima o un agresor.

    :param map_view: Objeto del mapa de Folium.
    :param position: Posición del marcador (número).
    :param lat: Latitud de la ubicación.
    :param lng: Longitud de la ubicación.
    :param row: Datos de la fila correspondiente (victim_row o aggressor_row).
    :param marker_type: Tipo de marcador, "victim" o "aggressor".
    """
    if marker_type == "victim":
        tooltip_text = (
            f"<b>Posición víctima:</b> {position}<br>"
            f"<b>Lon:</b> {lng}<br><b>Lat:</b> {lat}<br>"
            f"<b>Precision:</b> {row.get('precision', 'N/A')}<br>"
            f"<b>Time:</b> {row.get('time', 'N/A')}"
        )
        icon = folium.Icon(color="green", icon="female", prefix="fa")
    elif marker_type == "aggressor":
        tooltip_text = (
            f"<b>Posición agresor:</b> {position}<br>"
            f"<b>Lon:</b> {lng}<br><b>Lat:</b> {lat}<br>"
            f"<b>Precision:</b> {row.get('precision', 'N/A')}<br>"
            f"<b>Time:</b> {row.get('time', 'N/A')}"
        )
        icon = folium.Icon(color="red", icon="male", prefix="fa")
    else:
        raise ValueError("marker_type debe ser 'victim' o 'aggressor'")

    folium.Marker(
        location=(lat, lng),
        tooltip=tooltip_text,
        icon=icon,
    ).add_to(map_view)
