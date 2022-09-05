"""create_tables.py."""

import os
import sys

root_dir_str = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(root_dir_str)

from scripts.functions import run_sql

sql_demo = '''
      CREATE TABLE IF NOT EXISTS demographic (
        customer_id INTEGER Not Null PRIMARY KEY,
        age INTEGER,
        monthlyincome INTEGER,
        numberofdependents INTEGER
      );
      '''

sql_debt = '''
      CREATE TABLE IF NOT EXISTS debt (
        customer_id INTEGER Not Null PRIMARY KEY,
        seriousdlqin2yrs BOOLEAN,
        numberoftime30_59dayspastduenotworse INTEGER,
        numberoftime60_89dayspastduenotworse INTEGER,
        numberoftimes90dayslate INTEGER
      );
      '''

sql_payment = '''
      CREATE TABLE IF NOT EXISTS payment (
        customer_id INTEGER Not Null PRIMARY KEY,
        debtratio DOUBLE PRECISION,
        revolvingutilizationofunsecuredlines DOUBLE PRECISION,
        numberofopencreditlinesandloans INTEGER,
        numberrealestateloansorlines INTEGER
      );
      '''

sql_list = [sql_demo, sql_debt, sql_payment]

if __name__ == '__main__':
    for sql in sql_list:
        run_sql(sql)
