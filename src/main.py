import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import datetime as dt
import numpy as np
from transaction import Transaction, TransactionDetails
from util import *
from plot_util import *
from pprint import pprint

    
def main():
    data = parse_data("data/transactions-2020.09.07-2022.09.06.csv")
    print(f"Number of transactions: {len(data)}")

    fig, ax = plt.subplots(figsize=(12.7, 7))
    
    ax.set(xlabel="month", ylabel="amount", title="Income & expenses")
    
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

    income_monthly_net = np.array(income_net_by_month(data, span))
    income_monthly_gross = np.array(income_gross_by_month(data, span))
    expenses_monthly = np.array(expenses_by_month(data, span))
    total_net = sum_netto(data)
    total_gross = np.sum(income_monthly_gross)
    total_expense = np.sum(expenses_monthly)
    
    print(f"Total net: {total_net:.2f}")
    print(f"{'DATE':<12}{'GROSS':>10} {'EXPENSE':>10} {'NET':>10}")
    for (date, income_gross, expense, income_net) in zip(xdata, income_monthly_gross, expenses_monthly, income_monthly_net):
        print(f"{date}: {income_gross:>10.2f} {expense:>10.2f} {income_net:>10.2f}")
    print(f"{'TOTAL':<12}{total_gross:>10.2f} {total_expense:>10.2f} {total_net:>10.2f}")
        

    ax.xaxis.set_major_formatter(mdt.DateFormatter('%Y-%m-%d'))
    plot_and_scatter(ax, xdata, income_monthly_net, label="income net", linestyle="--")
    plot_and_scatter(ax, xdata, income_monthly_gross, label="income gross", linestyle="--")
    plot_and_scatter(ax, xdata, expenses_monthly, label="expenses net", linestyle="--")
    ax.plot([xdata[0], xdata[-1]], [0, 0])
    ax.legend()
    fig.autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    main()
