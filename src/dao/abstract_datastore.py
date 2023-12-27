import abc


class AbstractDatastoreDAO(abc.ABC):
    @abc.abstractmethod
    def save_data(self, key: str, data: dict):
        pass

    @abc.abstractmethod
    def get_data(self, key: str) -> dict:
        pass
