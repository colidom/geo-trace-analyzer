import folium
import os
from utils.distance import calculate_distance, process_location


class GeoMap:
    def __init__(self, center, zoom_start=15):
        """Inicializa el mapa centrado en una ubicación específica."""
        self.map = folium.Map(location=center, zoom_start=zoom_start)

    def add_safe_zone(self, secured_area, proximity_distance):
        """Agrega un marcador y un círculo de proximidad para la zona segura con información detallada."""
        lat, lng = secured_area

        tooltip = self.add_tooltip(None, lng, lat, None, "Domicilio")

        self.add_marker(secured_area, tooltip, "blue", "home")
        circle_tooltip = f"Secured Area: {proximity_distance}m"
        self.add_proximity_circle(
            secured_area, proximity_distance, "blue", circle_tooltip
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

    def add_tooltip(self, position=None, lng=None, lat=None, row=None, name=None):
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

    def check_prox_and_add_markers(
        self, victim_data, aggressor_data, proximity_distance
    ):
        """
        Verifica la proximidad de las víctimas con los agresores y añade marcadores al mapa
        solo si hay un agresor dentro del área de proximidad de la víctima.
        También dibuja el recorrido de los agresores.
        """
        victim_position = 1
        aggressor_position = 1

        aggressor_positions = []

        for _, victim_row in victim_data.iterrows():
            victim_coordinates = process_location(
                victim_row, location_column="location"
            )

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
                            ).add_to(self.map)

                if aggressor_nearby:
                    tooltip_text = self.add_tooltip(
                        victim_position, victim_lng, victim_lat, victim_row, "Víctima"
                    )

                    self.add_marker(
                        (victim_lat, victim_lng), tooltip_text, "green", "female"
                    )

                victim_position += 1

        # Añadir marcadores y recopilar las posiciones de los agresores
        for _, aggressor_row in aggressor_data.iterrows():
            aggressor_coordinates = process_location(
                aggressor_row, location_column="location"
            )

            if aggressor_coordinates:
                aggressor_lat, aggressor_lng = aggressor_coordinates
                aggressor_positions.append((aggressor_lat, aggressor_lng))

                tooltip_text = self.add_tooltip(
                    aggressor_position,
                    aggressor_lng,
                    aggressor_lat,
                    aggressor_row,
                    "Agresor",
                )

                self.add_marker(
                    (aggressor_lat, aggressor_lng), tooltip_text, "red", "male"
                )

                aggressor_position += 1

        self.add_aggressor_route(aggressor_positions, "red")
