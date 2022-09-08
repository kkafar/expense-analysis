from datetime import date


def print_result_table(
    total_no_transactions: int,
    timeline: list[date],
    income_gross: list[float],
    expenses: list[float],
    income_net: list[float],
    total_net: float,
    total_gross: float,
    total_expense: float) -> None:
    
    print(f"Number of transactions: {total_no_transactions}")
    print(f"Total net: {total_net:.2f}")
    print(f"{'DATE':<12}{'GROSS':>10} {'EXPENSE':>10} {'NET':>10}")
    for (date, gross, expense, net) in zip(timeline, income_gross, expenses, income_net):
        print(f"{date}: {gross:>10.2f} {expense:>10.2f} {net:>10.2f}")
    print(f"{'TOTAL':<12}{total_gross:>10.2f} {total_expense:>10.2f} {total_net:>10.2f}")
