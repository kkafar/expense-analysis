from pprint import pprint
from typing import Counter
import numpy as np
from data.datamanager import DataManager
from datautil import *
from cli import *
from presentation.cli import print_result_table
from presentation.plot import plot_result
from util.lazy import LazyEval
from pathlib import Path

    
def main():
    args = build_cli().parse_args()

    data = parse_data(args.file)
    span, xdata = get_timeline(data)

    
    income_monthly_net = LazyEval(income_net_by_month, data, span)
    income_monthly_gross = LazyEval(income_gross_by_month, data, span)
    expenses_monthly = LazyEval(expenses_by_month, data, span)
    total_net = LazyEval(sum_netto, data)
    total_gross = LazyEval(np.sum, income_monthly_gross.get())
    total_expense = LazyEval(np.sum, expenses_monthly.get())

    action_taken = False
    if args.table or args.all: 
        action_taken = True
        print_result_table(
            total_no_transactions=len(data),
            timeline=xdata,
            income_gross=income_monthly_gross.get(),
            expenses=expenses_monthly.get(),
            income_net=income_monthly_net.get(),
            total_net=total_net.get(),
            total_gross=total_gross.get(),
            total_expense=total_expense.get())
        
    if args.plot or args.all:
        action_taken = True
        plot_result(
            total_no_transactions=len(data),
            timeline=xdata,
            income_gross=income_monthly_gross.get(),
            expenses=expenses_monthly.get(),
            income_net=income_monthly_net.get(),
            total_net=total_net.get(),
            total_gross=total_gross.get(),
            total_expense=total_expense.get())

            
    DataManager(Path(args.file).parent).save_categories(Transaction.CATEGORIES)

            
    # data_by_localization = group_by_localization(data)
    # sorted_data_by_localization = sorted(data_by_localization, key=lambda loc: len(data_by_localization[loc]), reverse=True)

    # print(sorted_data_by_localization)

    # for loc in sorted_data_by_localization:
    #     print(loc, "count:", len(data_by_localization[loc]), "amount:", reduce(lambda s, t: s + t.amount,  data_by_localization[loc], 0))


    # for t in filter(lambda t: t.category == Transaction.CATEGORY_DEFAULT, data):
    #     print(t)

    # print(len(list(filter(lambda t: t.category == Transaction.CATEGORY_DEFAULT, data))))

    
    # counter = Counter()
    # for t in data:
    #     counter[t.category] += 1
        

    # for entry in counter:
    #     print(entry, counter[entry])
    # print(counter)

    sum_by_category = sum_net_by_category(data)

    # for cat, amount in sum_by_category.items():
    #     print(cat, amount)

    if not action_taken:
        print_no_action_taken_warning()
        


if __name__ == "__main__":
    main()
