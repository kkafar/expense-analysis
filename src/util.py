import csv
from transaction import Transaction


def parse_data(source: str) -> list[Transaction]:
    records: list[Transaction] = []

    with open("data/bills.csv") as input:
        input_reader = csv.reader(input)
        
        _ = next(input_reader)
        for record in input_reader:
            records.append(Transaction(record))

    return records


def sum_netto(transactions: list[Transaction]) -> float:
    total = 0
    for transaction in transactions:
        total += transaction.amount

    return total

    
def income_net_by_month(transactions: list[Transaction]) -> list[float]:
    result = [0 for _ in range(12)]

    for t in transactions:
        result[t.date.month - 1] += t.amount

    return result


def income_gross_by_month(transactions: list[Transaction]) -> list[float]:
    result = [0 for _ in range(12)]
    
    for t in transactions:
        if t.amount > 0:
            result[t.date.month - 1] += t.amount

    return result


def expenses_by_month(transactions: list[Transaction]) -> list[float]:
    result = [0 for _ in range(12)]
    
    for t in transactions:
        if t.amount < 0:
            result[t.date.month - 1] += t.amount

    return result
