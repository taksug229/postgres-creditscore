"""add_rows_to_tables.py."""

import os
import sys

root_dir_str = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(root_dir_str)

import argparse

from sqlalchemy import create_engine

import scripts.config as cfg
from scripts.functions import Tables, add_tables_safely

parser = argparse.ArgumentParser(description='Enter CSV File Path to add')
parser.add_argument(
    'csv_path', type=str, help='Path to CSV file to create add to tables'
    )
args = parser.parse_args()

if __name__ == '__main__':
    engine = create_engine(
        f'postgresql://{cfg.postgres["user"]}:{cfg.postgres["password"]}@{cfg.postgres["host"]}:{cfg.postgres["port"]}/{cfg.postgres["dbname"]}'
    )
    table = Tables(args.csv_path)
    table.split_tables()

    add_tables_safely(table_name='demographic', engine=engine, table=table)
    add_tables_safely(table_name='debt', engine=engine, table=table)
    add_tables_safely(table_name='payment', engine=engine, table=table)
