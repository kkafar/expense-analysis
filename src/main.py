import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import datetime as dt
import numpy as np
from datautil import *
from plotutil import *
from cli import *
    

    
def main():
    args = build_cli().parse_args()

    data = parse_data(args.file)
    span, xdata = get_timeline(data)

    income_monthly_net = np.array(income_net_by_month(data, span))
    income_monthly_gross = np.array(income_gross_by_month(data, span))
    expenses_monthly = np.array(expenses_by_month(data, span))
    total_net = sum_netto(data)
    total_gross = np.sum(income_monthly_gross)
    total_expense = np.sum(expenses_monthly)
    
    if not args.quiet:
        print(f"Number of transactions: {len(data)}")
        print(f"Total net: {total_net:.2f}")
        print(f"{'DATE':<12}{'GROSS':>10} {'EXPENSE':>10} {'NET':>10}")
        for (date, income_gross, expense, income_net) in zip(xdata, income_monthly_gross, expenses_monthly, income_monthly_net):
            print(f"{date}: {income_gross:>10.2f} {expense:>10.2f} {income_net:>10.2f}")
        print(f"{'TOTAL':<12}{total_gross:>10.2f} {total_expense:>10.2f} {total_net:>10.2f}")
        
    if args.plot:
        fig, ax = plt.subplots(figsize=(12.7, 7))
        
        ax.set(xlabel="month", ylabel="amount", title="Income & expenses")

        ax.xaxis.set_major_formatter(mdt.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdt.MonthLocator(interval=1))
        plot_and_scatter(ax, xdata, income_monthly_net, label="income net", linestyle="--")
        plot_and_scatter(ax, xdata, income_monthly_gross, label="income gross", linestyle="--")
        plot_and_scatter(ax, xdata, expenses_monthly, label="expenses net", linestyle="--")
        ax.plot([xdata[0], xdata[-1]], [0, 0])
        ax.grid(True)
        ax.legend()
        fig.autofmt_xdate()
        plt.locator_params(axis='y', nbins=10)
        plt.show()


if __name__ == "__main__":
    main()
