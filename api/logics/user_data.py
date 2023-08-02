from pathlib import Path

from dao.json_file_datastore import JsonFileDatastore


datastore = JsonFileDatastore(data_path=Path("/Users/yogson/PycharmProjects/auth_service/data/user_data"))


def write_user_data(username: str, data: dict):
    datastore.save_data(username, data)


def retrieve_user_data(username: str):
    return datastore.get_data(username)