import csv
import datetime as dt
from transaction import Transaction

def timediff_in_months(date_begin: dt.date, date_end: dt.date) -> int:
    diff = (date_end.year - date_begin.year) * 12 + date_end.month - date_begin.month
    assert diff >= 0, "Negative timediff. Assure that date_begin <= date_end"
    return diff


def parse_data(source: str) -> list[Transaction]:
    assert source is not None, "No source provided"
    records: list[Transaction] = []

    with open(source) as input:
        input_reader = csv.reader(input)
        
        _ = next(input_reader)
        for record in input_reader:
            records.append(Transaction(record))

    return records


def sum_netto(transactions: list[Transaction]) -> float:
    result = 0

    for transaction in transactions:
        result += transaction.amount

    return result

    
def income_net_by_month(transactions: list[Transaction], span: int = 12) -> list[float]:
    result = [0 for _ in range(span + 1)]

    for t in transactions:
        result[timediff_in_months(transactions[-1].date, t.date)] += t.amount

    return result


def income_gross_by_month(transactions: list[Transaction], span: int = 12) -> list[float]:
    result = [0 for _ in range(span + 1)]
    
    for t in transactions:
        if t.amount > 0:
            result[timediff_in_months(transactions[-1].date, t.date)] += t.amount

    return result


def expenses_by_month(transactions: list[Transaction], span: int = 12) -> list[float]:
    result = [0 for _ in range(span + 1)]
    
    for t in transactions:
        if t.amount < 0:
            result[timediff_in_months(transactions[-1].date, t.date)] += t.amount

    return result
