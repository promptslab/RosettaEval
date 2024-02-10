import json


def read_json_from_path(file_path):
    """
    Reads a JSON file from the specified file path and returns the data.

    Parameters
    ----------
    file_path (str): The path to the JSON file.

    Returns
    -------
    dict: The data contained in the JSON file.

    """
    try:
        with open(file_path) as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"The file at {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
