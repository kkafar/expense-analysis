from datetime import date
from typing import Any, Callable


StrOpt = str | None

class TransactionDetails(object):
    PREFIXES = {
        "title": "Tytu³: ",
        "sender": "Nazwa nadawcy: ",
        "receiver": "Nazwa odbiorcy: ",
        "localization": "Lokalizacja: "
    }
    KEY_TITLE = "title"
    KEY_SENDER = "sender"
    KEY_LOCALIZATION = "localization"
    KEY_RECEIVER = "receiver"


    def __init__(self, raw_details: list[str]) -> None:
        self.title: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_TITLE], raw_details)

        self.sender: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_SENDER], raw_details)

        self.receiver: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_RECEIVER], raw_details)

        self.localization: StrOpt = TransactionDetails.__find_detail_and_strip_prefix(
            TransactionDetails.PREFIXES[TransactionDetails.KEY_LOCALIZATION], raw_details)

        self.other_details: list[str] = list(
            filter(lambda detail: not any(map(lambda prefix: detail.startswith(prefix),
                                              TransactionDetails.PREFIXES.values())), raw_details))

    def __str__(self) -> str:
        return f"Title: {self.title}\nSender: {self.sender}\nReceiver: {self.receiver}\nLocalization: {self.localization}\nOther info:\n  {self.__format_other_info()}"

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

TransactionPredicate = Callable[['Transaction', list[str]], bool]

class SelfContainedPredicate(object):
    def __init__(self, base_pred: TransactionPredicate, *args) -> None:
        self.pred = base_pred
        self.args = args


    def __call__(self, transaction: 'Transaction') -> bool:
        return self.pred(transaction, *self.args)


class TransactionCategory(object):
    def __init__(self, name: str, preds: TransactionPredicate | list[TransactionPredicate], substrs: list[str]) -> None:
        self.name = name
        self.preds: list[SelfContainedPredicate] = [SelfContainedPredicate(preds, substrs)]


    def __repr__(self) -> str:
        return f"TransactionCategory(name={self.name})"


    def __str__(self) -> str:
        return self.name


    def accept(self, t: 'Transaction') -> bool:
        for p in self.preds:
            if p(t): return True
        return False


def _has_any_substr(string: StrOpt, substrs: list[str]) -> bool:
    if string is None: return False
    return any(map(lambda i: i != -1, map(lambda substr: string.find(substr), substrs)))


def _localization_pred(t: 'Transaction', substrs: list[str]) -> bool:
    return _has_any_substr(t.details.localization, substrs=substrs)


def _title_pred(t: 'Transaction', substrs: list[str]) -> bool:
    return _has_any_substr(t.details.title, substrs=substrs)


def _receiver_pred(t: 'Transaction', substrs: list[str]) -> bool:
    return _has_any_substr(t.details.receiver, substrs=substrs)


def _sender_pred(t: 'Transaction', substrs: list[str]) -> bool:
    return _has_any_substr(t.details.sender, substrs=substrs)


def any_category_pred(_: 'Transaction') -> True:
    return True


def groceries_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, [
        "BIEDRONKA", "CARREFOUR", "ZABKA",
        "AWITEKS", "QLT", "Nasz Chleb", "DELIKATESY",
        "AUCHAN", "MAGNUS", "Delikatesy"])


def meds_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, ["APTEKA"])


def dinners_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, ["pyszne.pl", "Hindus Food"])


def restaurants_category_pred(t: 'Transaction') -> bool:
    if _localization_pred(t, [
        "GRUZINSKIE", "KEBAB", "LODZIARNIA",
        "Dobra Paczkarnia", "MOMENTO", "MCDONALDS",
        "CUKIERNIA", "MY VIET NAM", "ZAPIEXA",
        "Good Lood", "PIZZATOPIA", "LOOD IS GOOD",
        "DOMINIUM", "Thai Cooking", "LA GRANDE MAMMA",
        "BOSCAIOLA", "RESTAURACJA", "TRATTORIA", "PORTO BELLO",
        "DOBRA PACZKARNIA", "Pizzeria", "SUSHI", "Hard Rock Cafe",
        "PAPA GELATO", "KAWIARNIA", "CIRCLE K", "JAZZ ROCK",
        "PIJALNIE", "EMALIA", "PIEC", "FABRYKA SMAKU", "ROLLS",
        "COFFEE", "CYRANO"]):
        return True

    return False


def donations_category_pred(t: 'Transaction') -> bool:
    return _sender_pred(t, ["AW KAFARA", "AW  KAFARA"])


def cosmetics_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, [
        "ROSSMANN", "SEPHORA", "STUDIO FRYZUR", "SALON FRYZJERSKI",
        "RISOR"])


def alcohol_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, [
        "RE OGRODEK", "KOCYK", "MADOMARKET",
        "FINE WINE", "WEZZE", "KLUB STUDIO",
        "PIWO SWIEZE", "STUDENT MARKET",
        "Klub Studio", "BAR ZEW", "Al Capone"])


def electronics_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, ["x-kom.pl", "LOGITECH"])


def salary_category_pred(t: 'Transaction') -> bool:
    sender = t.details.sender

    if sender is None or sender.find("SOFTWARE") == -1:
        return False

    return True


def rent_category_pred(t: 'Transaction') -> bool:
    return _title_pred(t, ["CZYNSZ", "OP£ATA ZA MIESZKANIE"])


def clothing_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, [
        "MARTES SPORT", "sklepbiegacza.pl",
        "LANCERTO", "KAZAR", "AMBRA", "ZEGARMISTRZ",
        "MASSIMO DUTTI", "RYLKO", "Wrangler", "Nike",
        "Timberland", "ADIDAS", "FootLocker", "TIMBERLAND",
        "Lavard", "LAVARD", "MEDICINE", "Adres: HM", "BYTOM",
        "PULL & BEAR"])


def atm_category_pred(t: 'Transaction') -> bool:
    title = t.details.title
    return title and title.find("PKO BP") != -1


def transport_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, [
        "BOLT", "rezerwacje.neobus.pl", "MPK KRAKOW", "intercity"]) or \
        _title_pred(t, ["ZAKUP BILETU KOMUNIKACYJNEGO", "barbara.net"]) or \
        _sender_pred(t, ["NEOBUS"])


def other_shopping_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, ["allegro.pl", "TESCOMA", "SMYK"])


def media_category_pred(t: 'Transaction') -> bool:
    return _title_pred(t, ["FAKTURY ZA GAZ"]) or \
        _receiver_pred(t, ["PGNIG", "TAURON"]) or \
        _sender_pred(t, ["GRZYB", "MATEUSZ", "WINIARSKI"])



def entertainment_category_pred(t: 'Transaction') -> bool:
    return _localization_pred(t, [
        "KINO KIJOW", "cinema-city", "CYBERPUB",
        "STEAM", "eventim.pl", "CINEMA CITY", "EMPIK", "RCKP",
        "MULTIKINO", "kinomikro", "Amazon", "HBO"])


def scholarship_category_pred(t: 'Transaction') -> bool:
    return _sender_pred(t, ["AKADEMIA GÓRNICZO-HUTNICZA"])

class Transaction(object):
    KEY_DATE = 0
    KEY_TYPE = 2
    KEY_AMOUNT = 3
    KEY_BALANCE_AFTER = 5
    KEY_DESCRIPTION_START = 6
    KEY_DESCRIPTION_END = 10

    CATEGORIES: set[TransactionCategory] = set([
        TransactionCategory("transport", transport_category_pred),
        TransactionCategory("groceries", groceries_category_pred),
        TransactionCategory("meds", meds_category_pred),
        TransactionCategory("dinners", dinners_category_pred),
        TransactionCategory("restaurants", restaurants_category_pred),
        TransactionCategory("alcohol", alcohol_category_pred),
        TransactionCategory("electronics", electronics_category_pred),
        TransactionCategory("salary", salary_category_pred),
        TransactionCategory("donations", donations_category_pred),
        TransactionCategory("rent", rent_category_pred),
        TransactionCategory("clothing", clothing_category_pred),
        TransactionCategory("atm", atm_category_pred),
        TransactionCategory("media", media_category_pred),
        TransactionCategory("cosmetics", cosmetics_category_pred),
        TransactionCategory("entertainment", entertainment_category_pred),
        TransactionCategory("other_shopping", other_shopping_category_pred),
        TransactionCategory("scholarship", scholarship_category_pred)
    ])

    CATEGORY_DEFAULT = TransactionCategory("Other", any_category_pred)


    def __init__(self, raw_record: list[str]) -> 'Transaction':
        self.date: date = date.fromisoformat(raw_record[Transaction.KEY_DATE])
        self.type: str = raw_record[Transaction.KEY_TYPE]
        self.amount: float = float(raw_record[Transaction.KEY_AMOUNT])
        self.balance_after: float = float(raw_record[Transaction.KEY_BALANCE_AFTER])
        self.details = TransactionDetails(raw_record[Transaction.KEY_DESCRIPTION_START : -1])
        self.category = self.resolve_category()


    def __str__(self) -> str:
        return f"Date: {self.date}\nAmount: {self.amount}\nBalance: {self.balance_after}\nCategory: {self.category}\n{self.details}"


    def resolve_category(self) -> TransactionCategory | None:
        for category in Transaction.CATEGORIES:
            if category.accept(self):
                return category

        return Transaction.CATEGORY_DEFAULT


    @classmethod
    def print_transactions(cls, records: list['Transaction']) -> None:
        print('-' * 20)
        for record in records:
            print(record)
            print('-' * 20)
