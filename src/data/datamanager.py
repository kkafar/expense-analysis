from pathlib import Path
from data.cache import Cache
from data.transaction import SelfContainedPredicate, TransactionCategory
import jsonpickle as json


@json.handlers.register(TransactionCategory, base=False)
class TransactionCategoryAdapter(json.handlers.BaseHandler):
    def flatten(self, obj: TransactionCategory, _: dict) -> dict:
        return {
            'name': obj.name,
            'preds': [
                { 'name': pred.pred.__name__, 'args': pred.args } for pred in obj.preds
            ]
        }

    def restore(self, obj: dict):
        return TransactionCategory('x kurde d', lambda t: False)

class DataManager(object):
    def __init__(self, data_dir: Path) -> None:
        if not data_dir.is_dir():
            raise FileNotFoundError(f"Provided path to data directory: \"{data_dir}\" does not point to a directory.")

        self.data_dir = data_dir
        self.cache = Cache(data_dir.parent / ".cache")


    def save_categories(self, transaction_categories: list[TransactionCategory]) -> None:
        result = json.dumps(transaction_categories, unpicklable=True, indent=2)
        self.cache.save(result, "categories.json")


    def load_categories(self) -> list[TransactionCategory]:
        return list()
