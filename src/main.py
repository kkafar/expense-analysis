import csv
import matplotlib.pyplot as plt
import datetime as dt
from transaction import Transaction, TransactionDetails

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

    
def main():
    data = parse_data("data/bills.csv")

    # print(Transaction.print_transactions(records=data))
    print(f"Total net: {sum_netto(data):.2f}")
    print(f"Expenses by month: {income_net_by_month(data)}")

    fig, ax = plt.subplots(figsize=(12.7, 7))
    
    ax.set(xlabel="month", ylabel="amount", title="Income net by month in 2022")
    ax.plot([i for i in range(1, 12 + 1)], income_net_by_month(data), linestyle="--")
    ax.scatter([i for i in range(1, 12 + 1)], income_net_by_month(data), label="income net", linestyle="--")
    ax.plot([i for i in range(1, 12 + 1)], income_gross_by_month(data), linestyle="--")
    ax.scatter([i for i in range(1, 12 + 1)], income_gross_by_month(data), label="income gross", linestyle="--")
    ax.plot([i for i in range(1, 12 + 1)], expenses_by_month(data), linestyle="--")
    ax.scatter([i for i in range(1, 12 + 1)], expenses_by_month(data), label="expenses net", linestyle="--")
    ax.legend()
    plt.show()


    


if __name__ == "__main__":
    main()
