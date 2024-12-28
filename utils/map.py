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
    """
    victim_position = 1
    aggressor_position = 1

    for _, victim_row in victim_data.iterrows():
        victim_coordinates = process_location(victim_row, location_column="location")

        if victim_coordinates:
            victim_lat, victim_lng = victim_coordinates

            aggressor_nearby = False

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
                        aggressor_nearby = True
                        folium.Circle(
                            location=(victim_lat, victim_lng),
                            radius=proximity_distance,
                            color="orange",
                            fill=True,
                            fill_opacity=0.1,
                            tooltip=f"Proximity Alert: {distance:.2f}m",
                        ).add_to(map_view)

            if aggressor_nearby:
                tooltip_text = (
                    f"<b>Posición víctima:</b> {victim_position}<br>"
                    f"<b>Lon:</b> {victim_lng}<br><b>Lat:</b> {victim_lat}<br>"
                    f"<b>Precision:</b> {victim_row.get('precision', 'N/A')}<br>"
                    f"<b>Time:</b> {victim_row.get('time', 'N/A')}"
                )
                folium.Marker(
                    location=(victim_lat, victim_lng),
                    tooltip=tooltip_text,
                    icon=folium.Icon(color="green", icon="female", prefix="fa"),
                ).add_to(map_view)

            victim_position += 1

    # Añadir marcadores de agresores
    for _, aggressor_row in aggressor_data.iterrows():
        aggressor_coordinates = process_location(
            aggressor_row, location_column="location"
        )

        if aggressor_coordinates:
            aggressor_lat, aggressor_lng = aggressor_coordinates

            tooltip_text = (
                f"<b>Posición agresor:</b> {aggressor_position}<br>"
                f"<b>Lon:</b> {aggressor_lng}<br><b>Lat:</b> {aggressor_lat}<br>"
                f"<b>Precision:</b> {aggressor_row.get('precision', 'N/A')}<br>"
                f"<b>Time:</b> {aggressor_row.get('time', 'N/A')}"
            )
            folium.Marker(
                location=(aggressor_lat, aggressor_lng),
                tooltip=tooltip_text,
                icon=folium.Icon(color="red", icon="male", prefix="fa"),
            ).add_to(map_view)

            aggressor_position += 1
