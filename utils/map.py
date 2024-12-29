import folium
import os
from utils.distance import calculate_distance, process_location


class Map:
    def __init__(self, center, zoom_start=15):
        """Inicializa un mapa centrado en una ubicación específica."""
        self.map = folium.Map(location=center, zoom_start=zoom_start)

    def add_safe_zone(self, secured_area, proximity_distance):
        """Agrega un marcador y un círculo de proximidad para la zona segura con información detallada."""
        lat, lng = secured_area
        tooltip_text = f"<b>Lon:</b> {lng}<br><b>Lat:</b> {lat}<br>"

        folium.Marker(
            location=secured_area,
            tooltip=tooltip_text,
            icon=folium.Icon(color="blue", icon="home", prefix="fa"),
        ).add_to(self.map)

        folium.Circle(
            location=secured_area,
            radius=proximity_distance,
            color="blue",
            fill=True,
            fill_opacity=0.2,
            tooltip=f"Secured Area: {proximity_distance}m",
        ).add_to(self.map)

    def save(self, result_folder, output_file):
        """Guarda el mapa en un archivo HTML."""
        os.makedirs(result_folder, exist_ok=True)
        self.map.save(os.path.join(result_folder, output_file))
        print(f"Mapa generado exitosamente: {os.path.join(result_folder, output_file)}")

    def verify_location(self, location):
        """Verifica y procesa una ubicación en diferentes formatos."""
        if isinstance(location, str):
            lat, lng = map(float, location.split(","))
            return lat, lng
        elif isinstance(location, float):
            print(f"Valor inesperado en 'location': {location}")
        else:
            print(f"Tipo no esperado en 'location': {type(location)}")

    def check_prox_and_add_markers(
        self, victim_data, aggressor_data, proximity_distance
    ):
        """
        Verifica la proximidad de las víctimas con los agresores y añade marcadores al mapa
        solo si hay un agresor dentro del área de proximidad de la víctima.
        También dibuja el recorrido de los agresores.
        """
        victim_positions = self._process_victims(
            victim_data, aggressor_data, proximity_distance
        )
        aggressor_positions = self._process_aggressors(aggressor_data)
        self._draw_aggressor_path(aggressor_positions)

    def _process_victims(self, victim_data, aggressor_data, proximity_distance):
        victim_position = 1
        for _, victim_row in victim_data.iterrows():
            victim_coordinates = process_location(
                victim_row, location_column="location"
            )

            if victim_coordinates:
                victim_lat, victim_lng = victim_coordinates
                aggressor_nearby = self._check_prox_and_add_circle(
                    victim_lat, victim_lng, aggressor_data, proximity_distance
                )

                if aggressor_nearby:
                    self._add_marker(
                        victim_position, victim_lat, victim_lng, victim_row, "victim"
                    )

                victim_position += 1

    def _process_aggressors(self, aggressor_data):
        aggressor_positions = []
        aggressor_position = 1

        for _, aggressor_row in aggressor_data.iterrows():
            aggressor_coordinates = process_location(
                aggressor_row, location_column="location"
            )

            if aggressor_coordinates:
                aggressor_lat, aggressor_lng = aggressor_coordinates
                aggressor_positions.append((aggressor_lat, aggressor_lng))
                self._add_marker(
                    aggressor_position,
                    aggressor_lat,
                    aggressor_lng,
                    aggressor_row,
                    "aggressor",
                )

                aggressor_position += 1

        return aggressor_positions

    def _draw_aggressor_path(self, aggressor_positions):
        if len(aggressor_positions) > 1:
            folium.PolyLine(
                aggressor_positions, color="red", weight=2.5, opacity=1
            ).add_to(self.map)

    def _check_prox_and_add_circle(
        self, victim_lat, victim_lng, aggressor_data, proximity_distance
    ):
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
                    ).add_to(self.map)
                    return True

        return False

    def _add_marker(self, position, lat, lng, row, marker_type):
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
        ).add_to(self.map)
