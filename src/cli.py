import argparse


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small CLI driven application for keeping expenses under control.")
    parser.add_argument("--file", action='store', default="data/transactions-2020.09.07-2022.09.07.csv")
    parser.add_argument("--plot", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    return parser
