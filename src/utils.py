import os


def list_data_files():
    data_folder = "./data"
    files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    return files


def choose_file(file_type):
    files = list_data_files()
    print(f"\nFicheros disponibles de {file_type}:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")

    while True:
        try:
            choice = int(input(f"Por favor elige el fichero de tipo {file_type} a procesar (1-{len(files)}): "))
            if 1 <= choice <= len(files):
                return os.path.join("data", files[choice - 1])
        except ValueError:
            pass
        print("⚠️ Invalid option. Please try again.")
