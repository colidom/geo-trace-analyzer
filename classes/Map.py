import folium
import os
from utils.distance import calculate_distance, extract_coordinates


class Map:
    def __init__(self, center, zoom_start=15):
        """
        Initialize a Map object using the Folium library. The map is centered on the given coordinates with an initial zoom level.

        Args:
            center (tuple[float, float]): Latitude and longitude values representing the center of the map.
            zoom_start (int, optional): The initial zoom level for the map. Defaults to 15.
        """
        self.map = folium.Map(location=center, zoom_start=zoom_start, tiles="Cartodb Positron")

    def add_safe_zone(self, secured_area, proximity_distance):
        """
        Adds a safe zone to the map based on the given secured area details and proximity
        distance. The method places a marker on the map representing the safe zone, adds a
        descriptive tooltip, and draws a circle around the area to indicate the proximity
        radius.

        Args:
            secured_area (Dict[str, Union[str, Tuple[float, float]]]): A dictionary
                containing details of the secured area. This includes its name
                (str), coordinates (tuple of latitude and longitude), and type
                (str) of the area (used for icon representation).
            proximity_distance (float): The distance specifying the proximity radius
                around the secured area.

        Returns:
            None
        """
        name = secured_area["name"]
        lat, lng = secured_area["coordinates"]
        icon_type = secured_area["type"]

        tooltip = self.add_tooltip(None, lng, lat, None, name)

        self.add_marker(secured_area["coordinates"], tooltip, "blue", icon_type)
        self.add_proximity_circle(
            secured_area["coordinates"], proximity_distance, "blue", tooltip
        )

    def add_proximity_circle(self, location, proximity_distance, color, tooltip):
        """
        Adds a proximity circle to the folium map.

        This method creates a circle on the map at a specified location with a given
        proximity distance (radius). The circle is styled with the provided color,
        filled with a semi-transparent overlay, and includes a tooltip.

        Args:
            location (list[float]): Latitude and longitude coordinates of the circle's
                center as a [latitude, longitude] list.
            proximity_distance (float): Radius in meters for the proximity circle.
            color (str): Border color of the circle in any valid CSS color format.
            tooltip (str): Tooltip text to display on hover.

        Returns:
            None
        """
        folium.Circle(
            location=location,
            radius=proximity_distance,
            color=color,
            fill=False,
            fill_opacity=0.2,
            tooltip=tooltip,
        ).add_to(self.map)

    def add_marker(self, location, tooltip, color, icon):
        """
        Adds a marker to the map at a given location with a tooltip, icon, and color.

        Parameters:
        location: list
            The latitude and longitude coordinates for the marker.
        tooltip: str
            The text to be displayed when hovering over the marker.
        color: str
            The color of the marker icon.
        icon: str
            The icon for the marker represented by a Font Awesome icon name.
        """
        folium.Marker(
            location=location,
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon=icon, prefix="fa"),
        ).add_to(self.map)

    def add_aggressor_route(self, aggressor_positions, color):
        """
        Adds a route to the map representing the aggressor's movement. This method
        visualizes a path using a polyline if multiple positions of the aggressor
        are provided. The route is drawn with the specified color.

        Parameters:
            aggressor_positions (list): A list of positions representing the
            coordinates of the aggressor's path. Each position is expected to be a
            tuple or list of latitude and longitude values.
            color (str): The color of the polyline representing the route on the map.

        Returns:
            None
        """
        if len(aggressor_positions) > 1:
            folium.PolyLine(
                aggressor_positions, color=color, weight=2.5, opacity=1
            ).add_to(self.map)

    def save(self, result_folder, output_file):
        """
        Saves the current map instance to a specified folder and file.

        This function ensures the target directory exists. If it does not,
        the directory is created. Then the map instance linked to the 'self.map'
        attribute is saved at the specified location using the output file name.
        Finally, a success message is printed to confirm the operation.

        Parameters:
        result_folder : str
            The directory where the map file will be saved. It can be an
            absolute or relative path.
        output_file : str
            The name of the file where the map will be saved, including
            its extension.

        Raises:
        None
        """
        os.makedirs(result_folder, exist_ok=True)
        self.map.save(os.path.join(result_folder, output_file))
        print(f"Mapa generado exitosamente: {os.path.join(result_folder, output_file)}")

    @staticmethod
    def verify_location(location):
        """
        Verify the format of a location and parses it into latitude and longitude.

        This method takes a location input, validates its type, and converts it
        into a tuple containing latitude and longitude values. It supports input
        given as a comma-separated string or other formats. Non-supported types or
        unexpected values trigger specific informational messages.

        Args:
            location (str | float): The location input to be verified and parsed.

        Returns:
            tuple[float, float] | None: A tuple containing latitude and longitude
                as floats if the input is valid and parsable, otherwise None.
        """
        if isinstance(location, str):
            lat, lng = map(float, location.split(","))
            return lat, lng
        elif isinstance(location, float):
            print(f"Valor inesperado en 'location': {location}")
        else:
            print(f"Tipo no esperado en 'location': {type(location)}")

    @staticmethod
    def add_tooltip(position=None, lng=None, lat=None, row=None, name=None):
        """
            Adds a tooltip with given information to be displayed in a specific format.

            This method constructs an HTML-styled tooltip string containing details such as
            name, coordinates (longitude and latitude), a position description, and any
            additional data extracted from a provided row object. The tooltip format will
            adapt based on the inputs provided.

            Args:
                position (str or None): Description of the location or a string
                    identifier for the position. Defaults to None.
                lng (float or None): Longitude coordinate. Defaults to None.
                lat (float or None): Latitude coordinate. Defaults to None.
                row (dict or None): Additional data to include in the tooltip, such as
                    precision and time. Defaults to None.
                name (str or None): Name or title to include in the tooltip. Defaults to None.

            Returns:
                str: A string representing the HTML-styled tooltip.

            Raises:
                (No specific errors raised by this method)
        """

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
        Processes victim and aggressor data to determine proximity and add markers.

        This function iterates over victim data rows, calculates proximity to aggressors,
        and processes the coordinates of any detected victim within the specified proximity.
        It increments the victim position for each processed row. After handling victims, it
        processes the aggressor data to determine positions and adds a route marker for them.

        Arguments:
            victim_data: DataFrame containing victim information
            aggressor_data: DataFrame containing aggressor information
            proximity_distance (float): Maximum allowable distance to determine proximity

        Returns:
            None
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
        """
        Processes a victim entity by analyzing its coordinates, checking for proximity
        to an aggressor, and taking necessary actions when proximity is confirmed.
        Returns the victim's coordinates if processing is conducted.

        Args:
            victim_data_row: dict
                A dictionary containing the data row for the victim, from which
                location information can be extracted.
            aggressor_data: Any
                The data representing the aggressor, used to determine proximity.
            proximity_distance: float
                The distance threshold to determine whether an aggressor is near a victim.
            victim_position: Any
                Additional data or metadata representing a victim's position.

        Returns:
            tuple[float, float] or None:
                Returns a tuple of latitude and longitude as the victim's coordinates if
                they are processed, or None if coordinates are not available.

        Raises:
            Does not explicitly raise any exceptions.
        """
        victim_coordinates = self.get_coordinates(victim_data_row, "location")
        if not victim_coordinates:
            return None
        victim_lat, victim_lng = victim_coordinates
        if self.is_aggressor_near(victim_lat, victim_lng, aggressor_data, proximity_distance):
            self.process_entity(victim_lat, victim_lng, victim_position, victim_data_row, "Víctima", "green", "female")
        return victim_coordinates

    def process_aggressors(self, aggressor_data, aggressor_position):
        """
        Processes the aggressor data to extract coordinates, process entities, and maintain
        their positions. This function iterates through aggressor data, retrieves geographical
        coordinates, appends them to a list, and invokes additional processing methods
        for each aggressor.

        Args:
            aggressor_data (pd.DataFrame): The data containing information about aggressors.
            aggressor_position (int): The initial position index for aggressors.

        Returns:
            list: A list of tuples where each tuple represents the latitude and longitude
            coordinates of an aggressor.

        """
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
        """
        Checks if there is an aggressor near the specified victim based on their
        coordinates and a specified proximity distance. If an aggressor is found
        within the proximity range, a proximity alert is triggered and the function
        returns True.

        Args:
            victim_lat (float): Latitude of the victim's location.
            victim_lng (float): Longitude of the victim's location.
            aggressor_data (pandas.DataFrame): Data containing aggressor details.
            proximity_distance (float): Distance in meters to define proximity range.

        Returns:
            bool: True if an aggressor is within the proximity distance, otherwise False.
        """
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
        """
        Processes an entity by creating a tooltip and adding a marker to a map.

        This function generates a tooltip using the provided entity information, then
        places a marker on the map at the specified latitude and longitude. The marker
        is styled with the provided color and icon.

        Args:
            lat: Latitude of the entity's location.
            lng: Longitude of the entity's location.
            position: A string representing the general position or area of the entity.
            data_row: The dataset row containing additional information about the entity.
            entity_type: The type or category of the entity.
            color: The color to use for the marker representation.
            icon: The icon to use for the marker representation.
        """
        tooltip_text = self.add_tooltip(position, lng, lat, data_row, entity_type)
        self.add_marker((lat, lng), tooltip_text, color, icon)

    @staticmethod
    def get_coordinates(data_row, location_column):
        """
            Extracts coordinates from a data row using the specified location column.

            This static method attempts to process and extract coordinates from a given
            row of data by utilizing the location column provided. If an exception
            occurs during processing, it will print an error message and return None.

            Args:
                data_row: The data row containing relevant information for extracting
                          coordinates.
                location_column: The name or index of the column in the data row from
                                 which to extract the coordinates.

            Returns:
                A data object containing the extracted coordinates, or None if an
                exception occurred during processing.
        """
        try:
            return extract_coordinates(data_row, location_column)
        except Exception as e:
            print(f"Error al procesar coordenadas: {e}")
            return None
