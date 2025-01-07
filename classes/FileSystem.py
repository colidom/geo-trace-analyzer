import os
import pandas as pd
import json
from dotenv import load_dotenv


class FileSystem:
    def __init__(self, base_dir=None):
        """
        Initializes an instance of the class with a base directory.

        If no base directory is specified, the current working
        directory is used as the default base directory.

        Args:
            base_dir (Optional[str]): The base directory for the instance. If
            None, defaults to the current working directory.
        """
        self.base_dir = base_dir or os.getcwd()

    @staticmethod
    def get_csv_file(data_path):
        """
            Retrieves the path to a CSV file from a given directory or validates a specified file.

            If the provided path corresponds to a directory, it attempts to locate a single CSV
            file within that directory. If the path is a file, it checks if it has a ".csv"
            extension. If any of these conditions are not met or if the file/directory does not
            exist, corresponding errors are raised.

            Raises:
                ValueError: If the provided file is not a CSV or if the directory contains
                zero or multiple CSV files.
                FileNotFoundError: If the provided path does not exist.

            Args:
                data_path: Path to a file or directory to validate or locate a CSV file.

            Returns:
                str: Path to the located or validated CSV file.
        """
        if os.path.isfile(data_path):
            # Si es un archivo, verificamos que sea un CSV
            if data_path.endswith(".csv"):
                return data_path
            else:
                raise ValueError(f"El archivo especificado no es un CSV: {data_path}")
        elif os.path.isdir(data_path):
            # Si es un directorio, buscamos un único archivo CSV
            csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]
            if len(csv_files) != 1:
                raise ValueError(
                    f"Se esperaba un único archivo CSV en '{data_path}', pero se encontraron {len(csv_files)} archivos."
                )
            return os.path.join(data_path, csv_files[0])
        else:
            raise FileNotFoundError(f"No se encontró la ruta especificada: {data_path}")

    @staticmethod
    def read_data(csv_file):
        """
        Reads data from a specified CSV file, filters rows based on a precision
        threshold, and returns the filtered DataFrame.

        Parameters:
        csv_file: str
            Path to the CSV file to be read.

        Returns:
        pandas.DataFrame
            A DataFrame containing rows from the CSV file filtered based on the
            precision threshold.
        """
        _, _, valid_precision = FileSystem.load_configuration()
        df = pd.read_csv(csv_file)
        return df[df['precision'] <= valid_precision]

    @staticmethod
    def create_directories(directories):
        """
            Creates multiple directories if they do not already exist.

            This method iterates through a list of directory paths and ensures that
            each directory in the list is created. If the directory already exists,
            no error will be raised due to the use of the `exist_ok=True` parameter.

            Args:
                directories: List of paths of directories to be created as strings.
        """
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def process_secured_areas(obj, secured_areas, prox_distance):
        """
            Processes secured areas and applies them as safe zones for the given object.

            This function iterates through a list of secured areas and applies each area as
            a safe zone to the provided object using the add_safe_zone method. It does so by
            considering a specified proximity distance.

            Arguments:
                obj: The object for which the safe zones will be applied. It is expected to
                have an add_safe_zone method.
                secured_areas (list): A list of secured areas to be processed.
                prox_distance (float): The proximity distance to be used for defining
                the safe zones.
        """
        for area in secured_areas:
            obj.add_safe_zone(area, prox_distance)

    @staticmethod
    def load_configuration():
        """
        Fetches configuration values from environment variables and processes them into
        appropriate Python datatypes for later usage in the application. This includes
        loading the .env file, extracting proximity distance, secured areas, and valid
        precision, and converting them into usable forms.

        @return: A tuple containing the following in order:
                 - proximity_distance (int): The distance value used for proximity calculations.
                 - secured_areas (list): A list of secured area details.
                 - valid_precision (list): A list describing valid precision values.
        """
        load_dotenv()
        try:
            proximity_distance = int(os.getenv("PROXIMITY_DISTANCE"))
            secured_areas = json.loads(os.getenv("SECURED_AREAS"))
            valid_precision = json.loads(os.getenv("VALID_PRECISION"))
        except (TypeError, ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Error al cargar las configuraciones: {e}")
        return proximity_distance, secured_areas, valid_precision

    def get_directories(self):
        """
        Retrieves the 'data' and 'result' directories based on the base directory.

        This function constructs paths for 'data' and 'result' directories using the
        'base_dir' attribute of the class instance. These directories are assumed to
        exist within the base directory. The function returns the full paths to both
        directories as a tuple.

        Returns:
            tuple: A tuple containing two strings. The first string is the path to the
            'data' directory, and the second string is the path to the 'result'
            directory.
        """
        data_dir = os.path.join(self.base_dir, "data")
        result_dir = os.path.join(self.base_dir, "result")
        return data_dir, result_dir

    def setup_environment(self) -> tuple[str, str, str]:
        """
        Sets up the environment by changing the working directory and creating
        necessary directories. This method ensures that the base directory is
        set, and relevant subdirectories for data and results are created.

        Returns:
            tuple[str, str, str]: A tuple containing the base directory, data
            directory, and result directory paths, respectively.
        """
        os.chdir(self.base_dir)
        data_dir, result_dir = self.get_directories()
        FileSystem.create_directories([data_dir, result_dir])
        return self.base_dir, data_dir, result_dir
