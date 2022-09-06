import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import datetime as dt
from transaction import Transaction, TransactionDetails
from util import *
from plot_util import *

    
def main():
    data = parse_data("data/transactions-2020.09.07-2022.09.06.csv")
    print(f"Number of transactions: {len(data)}")
    print(data[-1])

    fig, ax = plt.subplots(figsize=(12.7, 7))
    
    ax.set(xlabel="month", ylabel="amount", title="Income & expenses in 2022")
    
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

    print(f"Total net: {sum_netto(data):.2f}")
    print(f"Income net by month: {income_net_by_month(data, span)}")

    ax.xaxis.set_major_formatter(mdt.DateFormatter('%Y-%m-%d'))
    plot_and_scatter(ax, xdata, income_net_by_month(data, span), label="income net", linestyle="--")
    plot_and_scatter(ax, xdata, income_gross_by_month(data, span), label="income gross", linestyle="--")
    plot_and_scatter(ax, xdata, expenses_by_month(data, span), label="expenses net", linestyle="--")
    ax.legend()
    fig.autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    main()
