import json
from pathlib import Path

from dao.abstract_datastore import AbstractDatastoreDAO
from utils.common import logger


class JsonFileDatastore(AbstractDatastoreDAO):
    data_path: Path

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self._check_path()

    def _check_path(self):
        if not self.data_path.exists():
            if self.data_path.is_dir():
                self.data_path.mkdir(parents=True, exist_ok=True)

    def data_file(self, key: str) -> Path:
        return self.data_path / f"{key}.json"

    def save_data(self, key: str, data: dict):
        try:
            self.data_file(key).write_text(json.dumps(data))
        except FileNotFoundError:
            if not self.data_file(key).parent.exists():
                self.data_file(key).parent.mkdir(parents=True, exist_ok=True)
                self.save_data(key, data)

    def get_data(self, key: str) -> dict:
        data_file = self.data_file(key)
        if data_file.exists():
            try:
                return json.loads(data_file.read_text())
            except json.decoder.JSONDecodeError as e:
                logger.error(f"Bad datafile {data_file}: {e}")
        return {}
