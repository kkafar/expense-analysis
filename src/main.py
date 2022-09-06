import csv
import matplotlib.pyplot as plt
import datetime as dt
from transaction import Transaction, TransactionDetails
from util import *


    
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


if __name__ == "__main__":
    main()
