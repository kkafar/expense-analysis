from abc import ABC, abstractmethod
from data.transaction import Transaction, TransactionCategory

class TransactionAdapter(ABC):
    @abstractmethod
    def loads(data: str) -> Transaction:
        pass


    @abstractmethod
    def dumps(t: Transaction) -> str:
        pass

    
class TransactionCategoryAdapter(ABC):
    @abstractmethod
    def loads(data: str) -> TransactionCategory:
        pass

    
    @abstractmethod
    def dumps(t: TransactionCategory) -> str:
        pass


class TransactionJsonAdapter(TransactionAdapter):
    def __init__(self) -> None:
        super().__init__()

    def loads(data: str) -> Transaction:
        pass


    def dumps(t: Transaction) -> str:
        pass


    
