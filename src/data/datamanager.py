from pathlib import Path
from data.cache import Cache
from data.transaction import TransactionCategory
import jsonpickle as json


@json.handlers.register(TransactionCategory, base=False)
class TransactionCategoryAdapter(json.handlers.BaseHandler):
    def flatten(self, obj: TransactionCategory, data: dict):
        return {
            'name': obj.name,
            'preds': [
                {
                    'name': obj.pred.__name__,
                    'args': obj.args
                }
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
        for t in transaction_categories:
            # result = json.encode(t, unpicklable=True, indent=4)
            result = json.dumps(t, unpicklable=True, indent=4)
            print(result)
                        


    def load_categories(self) -> list[TransactionCategory]:
        return list()
