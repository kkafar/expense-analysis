import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import datetime as dt
import numpy as np
from datautil import *
from cli import *
from presentation.cli import print_result_table
from presentation.plot import plot_result
    

    
def main():
    args = build_cli().parse_args()

    data = parse_data(args.file)
    span, xdata = get_timeline(data)

    income_monthly_net = income_net_by_month(data, span)
    income_monthly_gross = income_gross_by_month(data, span)
    expenses_monthly = expenses_by_month(data, span)
    total_net = sum_netto(data)
    total_gross = np.sum(income_monthly_gross)
    total_expense = np.sum(expenses_monthly)

    action_taken = False
    if args.table or args.all: 
        action_taken = True
        print_result_table(
            total_no_transactions=len(data),
            timeline=xdata,
            income_gross=income_monthly_gross,
            expenses=expenses_monthly,
            income_net=income_monthly_net,
            total_net=total_net,
            total_gross=total_gross,
            total_expense=total_expense)
        
    if args.plot or args.all:
        action_taken = True
        plot_result(
            total_no_transactions=len(data),
            timeline=xdata,
            income_gross=income_monthly_gross,
            expenses=expenses_monthly,
            income_net=income_monthly_net,
            total_net=total_net,
            total_gross=total_gross,
            total_expense=total_expense)

            
    if not action_taken:
        print_no_action_taken_warning()
        


if __name__ == "__main__":
    main()
