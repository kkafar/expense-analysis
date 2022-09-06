import matplotlib.pyplot as plt
import datetime as dt
from transaction import Transaction, TransactionDetails
from util import *
from plot_util import *

    
def main():
    data = parse_data("data/bills.csv")

    # print(Transaction.print_transactions(records=data))
    print(f"Total net: {sum_netto(data):.2f}")
    print(f"Expenses by month: {income_net_by_month(data)}")

    fig, ax = plt.subplots(figsize=(12.7, 7))
    
    ax.set(xlabel="month", ylabel="amount", title="Income net by month in 2022")
    xdata = [i for i in range(1, 12 + 1)]
    plot_and_scatter(ax, xdata, income_net_by_month(data), label="income net", linestyle="--")
    plot_and_scatter(ax, xdata, income_gross_by_month(data), label="income gross", linestyle="--")
    plot_and_scatter(ax, xdata, expenses_by_month(data), label="expenses net", linestyle="--")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
