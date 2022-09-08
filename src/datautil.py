import csv
import datetime as dt
import numpy as np
from functools import reduce
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
    return reduce(lambda s, t: s + t.amount, transactions, 0)

    
def income_net_by_month(transactions: list[Transaction], span: int = 12) -> list[float]:
    result = np.zeros(shape=span + 1)

    for t in transactions:
        result[timediff_in_months(transactions[-1].date, t.date)] += t.amount

    return result


def income_gross_by_month(transactions: list[Transaction], span: int = 12) -> list[float]:
    result = np.zeros(shape=span + 1)
    
    for t in transactions:
        if t.amount > 0:
            result[timediff_in_months(transactions[-1].date, t.date)] += t.amount

    return result


def expenses_by_month(transactions: list[Transaction], span: int = 12) -> list[float]:
    result = np.zeros(shape=span + 1)
    
    for t in transactions:
        if t.amount < 0:
            result[timediff_in_months(transactions[-1].date, t.date)] += t.amount

    return result

def get_timeline(data: list[Transaction]) -> list[dt.date]:
    # For now we assume that thransactions are sorted - the newest at the top
    date_begin = data[-1].date
    date_end = data[0].date
    span = timediff_in_months(date_begin, date_end)

    xdata = []
    for offset in range(span + 1):
        month = date_begin.month - 1 + offset
        year_oveflow = month // 12
        month = month % 12 + 1
        year = date_begin.year + year_oveflow
        xdata.append(dt.date(year, month, 1))

    return span, xdata
