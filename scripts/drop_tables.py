"""drop_tables.py."""

import os
import sys

root_dir_str = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(root_dir_str)

from scripts.functions import run_sql

sql_drop_table = '''
    DROP TABLE IF EXISTS demographic, debt, payment;
    '''

if __name__ == '__main__':
    run_sql(sql_drop_table)
