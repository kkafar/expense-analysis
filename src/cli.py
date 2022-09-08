import argparse


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small CLI driven application for keeping expenses under control.")
    parser.add_argument("--file", action='store', default="data/transactions-2020.09.07-2022.09.07.csv")
    parser.add_argument("--plot", action='store_true', help="enable plotting")
    parser.add_argument("--table", action='store_true', help="print table with monthly summary")
    parser.add_argument("--all", action="store_true", help="enable all action flags")
    return parser


def print_no_action_taken_warning():
    print("No actions were specified. Run program with --help flag to see possible actions.")
