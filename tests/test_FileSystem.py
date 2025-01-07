import os

import pandas as pd
import pytest
from classes.FileSystem import FileSystem


@pytest.fixture
def file_system():
    return FileSystem()


@pytest.fixture
def mock_base_dir(tmp_path):
    return str(tmp_path)


@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("column1,column2,precision\n1,2,0.5\n3,4,1.5\n")
    return str(csv_file)


@pytest.fixture
def sample_dir_with_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("column1,column2,precision\n1,2,0.5\n3,4,1.5\n")
    return str(tmp_path)


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("PROXIMITY_DISTANCE", "500")
    monkeypatch.setenv("SECURED_AREAS", '[{"name": "Area1", "coordinates": [0, 0]}]')
    monkeypatch.setenv("VALID_PRECISION", "1.0")


def test_get_csv_file_valid_file(sample_csv, file_system):
    csv_path = file_system.get_csv_file(sample_csv)
    assert csv_path == sample_csv


def test_get_csv_file_invalid_extension(tmp_path, file_system):
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("Some content")
    with pytest.raises(ValueError):
        file_system.get_csv_file(str(invalid_file))


def test_get_csv_file_with_directory(sample_dir_with_csv, file_system):
    csv_path = file_system.get_csv_file(sample_dir_with_csv)
    assert csv_path.endswith("test.csv")


def test_get_csv_file_no_csv_in_dir(tmp_path, file_system):
    tmp_path.mkdir(exist_ok=True)
    with pytest.raises(ValueError):
        file_system.get_csv_file(str(tmp_path))


def test_get_csv_file_not_found(tmp_path, file_system):
    non_existent_path = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        file_system.get_csv_file(str(non_existent_path))


def test_read_data_valid_csv(sample_csv, file_system, mock_env_vars):
    df = file_system.read_data(sample_csv)
    assert not df.empty
    assert all(df['precision'] <= 1.0)


def test_read_data_invalid_csv(sample_csv, file_system, monkeypatch):
    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: None)
    with pytest.raises(TypeError):  # Assuming pandas raises TypeError for broken data
        file_system.read_data(sample_csv)


def test_create_directories(file_system, mock_base_dir):
    dirs_to_create = [os.path.join(mock_base_dir, "dir1"), os.path.join(mock_base_dir, "dir2")]
    file_system.create_directories(dirs_to_create)
    for dir_path in dirs_to_create:
        assert os.path.isdir(dir_path)


def test_get_directories(file_system, mock_base_dir):
    file_system.base_dir = mock_base_dir
    data_dir, result_dir = file_system.get_directories()
    assert data_dir.endswith("data")
    assert result_dir.endswith("result")


def test_setup_environment(file_system, mock_base_dir):
    file_system.base_dir = mock_base_dir
    base_dir, data_dir, result_dir = file_system.setup_environment()
    assert base_dir == mock_base_dir
    assert os.path.isdir(data_dir)
    assert os.path.isdir(result_dir)


def test_load_configuration(file_system, mock_env_vars):
    proximity_distance, secured_areas, valid_precision = file_system.load_configuration()
    assert proximity_distance == 500
    assert secured_areas == [{"name": "Area1", "coordinates": [0, 0]}]
    assert valid_precision == 1.0
