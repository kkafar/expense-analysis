from pathlib import Path

from data.cache import Cache
from data.transaction import TransactionCategory

class DataManager(object):
    def __init__(self, data_dir: Path) -> None:
        if not data_dir.is_dir():
            raise FileNotFoundError(f"Provided path to data directory: \"{data_dir}\" does not point a directory.")

        self.data_dir = data_dir        
        self.cache = Cache(data_dir.parnet / ".cache")
        

    def save_categories(transaction_categories: list[TransactionCategory]) -> None:
        pass


    def load_categories() -> list[TransactionCategory]:
        return list()
