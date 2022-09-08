import matplotlib.pyplot as plt
import matplotlib.dates as mdt
from datetime import date
from presentation.plotutil import plot_and_scatter


def plot_result(
    total_no_transactions: int,
    timeline: list[date],
    income_gross: list[float],
    expenses: list[float],
    income_net: list[float],
    total_net: float,
    total_gross: float,
    total_expense: float) -> None:
    
    fig, ax = plt.subplots(figsize=(12.7, 7))
    
    ax.set(xlabel="month", ylabel="amount", title="Income & expenses")

    ax.xaxis.set_major_formatter(mdt.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdt.MonthLocator(interval=1))
    plot_and_scatter(ax, timeline, income_net, label="income net", linestyle="--")
    plot_and_scatter(ax, timeline, income_gross, label="income gross", linestyle="--")
    plot_and_scatter(ax, timeline, expenses, label="expenses net", linestyle="--")
    ax.plot([timeline[0], timeline[-1]], [0, 0])
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate()
    plt.locator_params(axis='y', nbins=10)
    plt.show()
    