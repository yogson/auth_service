from pathlib import Path

from api.settings import USER_DATA_STORE
from dao.json_file_datastore import JsonFileDatastore


datastore = JsonFileDatastore(data_path=Path(USER_DATA_STORE))


def write_user_data(username: str, data: dict):
    datastore.save_data(username, data)


def retrieve_user_data(username: str):
    return datastore.get_data(username)
