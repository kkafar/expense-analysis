from datetime import date

StrOpt = str | None

class TransactionDetails(object):
    PREFIXES = {
        "title": "Tytu³: ",
        "sender": "Nazwa nadawcy: ",
        "localization": "Lokalizacja: "
    }
    KEY_TITLE = "title"
    KEY_SENDER = "sender"
    KEY_LOCALIZATION = "localization"
    
    
    def __init__(self, raw_details: list[str]) -> None:
        self.title: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_TITLE], raw_details)
        
        self.sender: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_SENDER], raw_details)

        self.localization: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_LOCALIZATION], raw_details)

        self.other_details: list[str] = list(filter(lambda detail: not any(map(lambda prefix: detail.startswith(prefix), 
                                                                           TransactionDetails.PREFIXES.values())), raw_details))

    def __str__(self) -> str:
        return f"Title: {self.title}\nSender: {self.sender}\nOther info:\n  {self.__format_other_info()}"

    def __format_other_info(self) -> str:
        return "\n  ".join(filter(lambda info: info, self.other_details))
        
    @classmethod
    def __remove_prefix(cls, prefix: str, string: str):
        return string.removeprefix(prefix) if string is not None else None

    @classmethod
    def __find_detail_with_prefix(cls, prefix: str, raw_details: list[str]) -> StrOpt:
        for detail in raw_details: 
            if detail.startswith(prefix):
                return detail
        return None

    @classmethod
    def __find_detail_and_strip_prefix(cls, prefix: str, raw_details: list[str]) -> StrOpt:
        return TransactionDetails.__remove_prefix(prefix, TransactionDetails.__find_detail_with_prefix(prefix, raw_details))


class Transaction(object):
    KEY_DATE = 0
    KEY_TYPE = 2
    KEY_AMOUNT = 3 
    KEY_BALANCE_AFTER = 5
    KEY_DESCRIPTION_START = 6
    KEY_DESCRIPTION_END = 10

    def __init__(self, raw_record: list[str]) -> 'Transaction':
        self.date: date = date.fromisoformat(raw_record[Transaction.KEY_DATE])
        self.type: str = raw_record[Transaction.KEY_TYPE]
        self.amount: float = float(raw_record[Transaction.KEY_AMOUNT])
        self.balance_after: float = float(raw_record[Transaction.KEY_BALANCE_AFTER])
        self.details = TransactionDetails(raw_record[Transaction.KEY_DESCRIPTION_START : -1])

        
    def __str__(self) -> str:
        return f"Date: {self.date}\nAmount: {self.amount}\nBalance: {self.balance_after}\n{self.details}"

            
    @classmethod
    def print_transactions(cls, records: list['Transaction']) -> None:
        print('-' * 20)
        for record in records:
            print(record)
            print('-' * 20)
