# File: tests/test_Map.py

import os

import folium
import pytest
from classes.Map import Map


@pytest.fixture
def map_instance():
    """Fixture to create a Map instance with default parameters."""
    return Map(center=(0, 0), zoom_start=15)


def test_add_safe_zone(map_instance):
    secured_area = {
        "name": "Test Safe Zone",
        "coordinates": (10.0, 10.0),
        "type": "info-sign"
    }
    map_instance.add_safe_zone(secured_area, proximity_distance=500)
    # Ensure the map still has the correct object inside
    assert isinstance(map_instance.map, folium.Map)


def test_add_proximity_circle(map_instance):
    location = (5.0, 5.0)
    proximity_distance = 300
    map_instance.add_proximity_circle(location, proximity_distance, "blue", "Test Tooltip")

    # Ensure folium.Map object remains intact
    assert isinstance(map_instance.map, folium.Map)


def test_add_marker(map_instance):
    location = (20.0, 20.0)
    tooltip = "Test Marker Tooltip"
    color = "red"
    icon = "test-icon"
    map_instance.add_marker(location, tooltip, color, icon)

    # Check the map instance remains valid
    assert isinstance(map_instance.map, folium.Map)


def test_add_aggressor_route(map_instance):
    aggressor_positions = [(10.0, 10.0), (15.0, 15.0), (20.0, 20.0)]
    color = "blue"
    map_instance.add_aggressor_route(aggressor_positions, color)

    # Ensure map property is updated
    assert isinstance(map_instance.map, folium.Map)


def test_save(map_instance, tmp_path):
    result_folder = tmp_path / "test_folder"
    output_file = "test_map.html"

    map_instance.save(result_folder=str(result_folder), output_file=output_file)

    # Check if file was created
    file_path = result_folder / output_file
    assert file_path.exists()


def test_verify_location_with_string(map_instance):
    location = "25.0,30.0"
    result = map_instance.verify_location(location)
    assert result == (25.0, 30.0)


def test_verify_location_with_invalid_type(map_instance):
    location = 25.0
    result = map_instance.verify_location(location)
    assert result is None


def test_add_tooltip_with_name_only(map_instance):
    tooltip = map_instance.add_tooltip(name="Test Name")
    assert "<center>Test Name</center>" in tooltip


def test_add_tooltip_with_coordinates(map_instance):
    tooltip = map_instance.add_tooltip(lng=20.0, lat=10.0, name="Test Tooltip")
    assert "Test Tooltip" in tooltip
    assert "<b>Lon:</b> 20.0<br>" in tooltip
    assert "<b>Lat:</b> 10.0<br>" in tooltip


def test_check_prox_and_add_markers(map_instance, mocker):
    victim_data = mocker.Mock()
    aggressor_data = mocker.Mock()
    proximity_distance = 200

    victim_data.iterrows.return_value = iter([
        (0, {"location": "10.0,10.0"}),
        (1, {"location": "30.0,30.0"})
    ])
    aggressor_data.iterrows.return_value = iter([
        (0, {"location": "15.0,15.0"}),
        (1, {"location": "10.0,10.0"})
    ])

    mocker.patch("classes.Map.process_location",
                 side_effect=lambda row, **k: tuple(map(float, row["location"].split(","))))
    mocker.patch("classes.Map.calculate_distance", side_effect=lambda x, y: 100.0)

    map_instance.check_prox_and_add_markers(victim_data, aggressor_data, proximity_distance)

    # Check if the map object remains valid
    assert isinstance(map_instance.map, folium.Map)
