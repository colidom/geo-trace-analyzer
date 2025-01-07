import folium
import os
from utils.distance import calculate_distance, extract_coordinates


class Map:
    def __init__(self, center, zoom_start=15):
        """Inicializa el mapa centrado en una ubicación específica."""
        self.map = folium.Map(location=center, zoom_start=zoom_start)

    def add_safe_zone(self, secured_area, proximity_distance):
        """Agrega un marcador y un círculo de proximidad para la zona segura con información detallada."""
        name = secured_area["name"]
        lat, lng = secured_area["coordinates"]
        icon_type = secured_area["type"]

        tooltip = self.add_tooltip(None, lng, lat, None, name)

        self.add_marker(secured_area["coordinates"], tooltip, "blue", icon_type)
        self.add_proximity_circle(
            secured_area["coordinates"], proximity_distance, "blue", tooltip
        )

    def add_proximity_circle(self, location, proximity_distance, color, tooltip):
        """Crea un círculo de proximidad alrededor de una ubicación."""
        folium.Circle(
            location=location,
            radius=proximity_distance,
            color=color,
            fill=True,
            fill_opacity=0.2,
            tooltip=tooltip,
        ).add_to(self.map)

    def add_marker(self, location, tooltip, color, icon):
        """Agrega un marcador con información y un icono."""
        folium.Marker(
            location=location,
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon=icon, prefix="fa"),
        ).add_to(self.map)

    def add_aggressor_route(self, aggressor_positions, color):
        """Añade el recorrido de los agresores como una línea poligonal al mapa."""
        if len(aggressor_positions) > 1:
            folium.PolyLine(
                aggressor_positions, color=color, weight=2.5, opacity=1
            ).add_to(self.map)

    def save(self, result_folder, output_file):
        """Guarda el mapa en un archivo HTML."""
        os.makedirs(result_folder, exist_ok=True)
        self.map.save(os.path.join(result_folder, output_file))
        print(f"Mapa generado exitosamente: {os.path.join(result_folder, output_file)}")

    @staticmethod
    def verify_location(location):
        """Verifica y procesa una ubicación en diferentes formatos."""
        if isinstance(location, str):
            lat, lng = map(float, location.split(","))
            return lat, lng
        elif isinstance(location, float):
            print(f"Valor inesperado en 'location': {location}")
        else:
            print(f"Tipo no esperado en 'location': {type(location)}")

    @staticmethod
    def add_tooltip(position=None, lng=None, lat=None, row=None, name=None):
        """Crea un tooltip para incrustarlo en el mapa con la información requerida"""

        tooltip = f"<center>{name}</center>"

        if position is None:
            if lng is not None and lat is not None:
                tooltip += f"<b>Lon:</b> {lng}<br>" f"<b>Lat:</b> {lat}<br>"
        else:
            if lng is not None and lat is not None:
                tooltip += (
                    f"<b>Coordenada:</b> {position}<br>"
                    f"<b>Lon:</b> {lng}<br>"
                    f"<b>Lat:</b> {lat}<br>"
                )

        if row is not None:
            precision = row.get("precision", "N/A") if hasattr(row, "get") else "N/A"
            time = row.get("time", "N/A") if hasattr(row, "get") else "N/A"

            tooltip += f"<b>Precision:</b> {precision}<br>" f"<b>Time:</b> {time}"

        return tooltip

    def check_prox_and_add_markers(self, victim_data, aggressor_data, proximity_distance):
        """
        Verifica la proximidad de las víctimas con los agresores y añade marcadores al mapa.
        También dibuja el recorrido de los agresores.
        """
        victim_position = aggressor_position = 1

        for _, victim_data_row in victim_data.iterrows():
            victim_coordinates = self.process_victim(
                victim_data_row, aggressor_data, proximity_distance, victim_position
            )
            if victim_coordinates:
                victim_position += 1

        aggressor_positions = self.process_aggressors(aggressor_data, aggressor_position)
        self.add_aggressor_route(aggressor_positions, "red")

    def process_victim(self, victim_data_row, aggressor_data, proximity_distance, victim_position):
        victim_coordinates = self.get_coordinates(victim_data_row, "location")
        if not victim_coordinates:
            return None
        victim_lat, victim_lng = victim_coordinates
        if self.is_aggressor_near(victim_lat, victim_lng, aggressor_data, proximity_distance):
            self.process_entity(victim_lat, victim_lng, victim_position, victim_data_row, "Víctima", "green", "female")
        return victim_coordinates

    def process_aggressors(self, aggressor_data, aggressor_position):
        aggressor_positions = []
        for _, aggressor_row in aggressor_data.iterrows():
            aggressor_coordinates = self.get_coordinates(aggressor_row, "location")
            if aggressor_coordinates:
                aggressor_lat, aggressor_lng = aggressor_coordinates
                aggressor_positions.append((aggressor_lat, aggressor_lng))
                self.process_entity(aggressor_lat, aggressor_lng, aggressor_position, aggressor_row, "Agresor", "red",
                                    "male")
                aggressor_position += 1
        return aggressor_positions

    def is_aggressor_near(self, victim_lat, victim_lng, aggressor_data, proximity_distance):
        aggressor_nearby = False
        for _, aggressor_row in aggressor_data.iterrows():
            aggressor_coordinates = extract_coordinates(
                aggressor_row, column="location"
            )
            if aggressor_coordinates:
                aggressor_lat, aggressor_lng = aggressor_coordinates
                distance = calculate_distance(
                    (victim_lat, victim_lng), (aggressor_lat, aggressor_lng)
                )
                if distance <= proximity_distance:
                    aggressor_nearby = True
                    self.add_proximity_circle(
                        (victim_lat, victim_lng), proximity_distance, "orange", f"Proximity Alert: {distance:.2f}m"
                    )
        return aggressor_nearby

    def process_entity(self, lat, lng, position, data_row, entity_type, color, icon):
        tooltip_text = self.add_tooltip(position, lng, lat, data_row, entity_type)
        self.add_marker((lat, lng), tooltip_text, color, icon)

    @staticmethod
    def get_coordinates(data_row, location_column):
        try:
            return extract_coordinates(data_row, location_column)
        except Exception as e:
            print(f"Error al procesar coordenadas: {e}")
            return None
