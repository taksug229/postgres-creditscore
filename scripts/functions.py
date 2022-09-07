"""functions.py."""

import os
import sys
from typing import Literal

import numpy as np
import pandas as pd
import psycopg2
import sqlalchemy

root_dir_str = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(root_dir_str)

import scripts.config as cfg


class Tables:
    """Tables Class."""
    def __init__(self, csv_path: str):
        """Init.

        Parameters
        ----------
        csv_path : str
            Path to csv file.
        """

        df = pd.read_csv(csv_path)
        df = df.rename(columns={df.columns[0]: 'Customer_ID'})
        df['SeriousDlqin2yrs'] = df['SeriousDlqin2yrs'].astype(bool)
        df['NumberOfDependents'] = df['NumberOfDependents'].astype('Int64')
        df.columns = [s.replace('-', '_') for s in df.columns.str.lower()]

        self.raw_df = df
        self.demographic_table = None
        self.debt_table = None
        self.payment_table = None

    def split_tables(self):
        """Split tables to demographic, debt, and payment."""
        demographic_mask = [
            'customer_id',
            'age',
            'monthlyincome',
            'numberofdependents'
        ]

        debt_mask = [
            'customer_id',
            'debtratio',
            'revolvingutilizationofunsecuredlines',
            'numberofopencreditlinesandloans',
            'numberrealestateloansorlines'
        ]

        payment_mask = [
            'customer_id',
            'seriousdlqin2yrs',
            'numberoftime30_59dayspastduenotworse',
            'numberoftime60_89dayspastduenotworse',
            'numberoftimes90dayslate'
        ]

        self.demographic_table = self.raw_df.loc[:, demographic_mask]
        self.debt_table = self.raw_df.loc[:, debt_mask]
        self.payment_table = self.raw_df.loc[:, payment_mask]


def run_sql(sql_query: str):
    """Runs' SQL query.

    Parameters
    ----------
    sql_query : str
        SQL query to run

    Returns
    ----------
    None:
        Runs SQL Query only
    """

    conn = psycopg2.connect(
        user=cfg.postgres["user"],
        password=cfg.postgres["password"],
        host=cfg.postgres["host"],
        dbname=cfg.postgres["dbname"]
    )
    with conn.cursor() as cur:
        cur.execute(sql_query)
    conn.commit()


def revise_table(
    df1: pd.DataFrame,
    df2: pd.DataFrame
) -> pd.DataFrame:
    """Revise new table's customer_ID (key) for uniqueness.

    Parameters
    ----------
    df1 : pd.DataFrame
        Original table.
    df2 : pd.DataFrame
        New table to add.

    Returns
    -------
    df2_: pd.DataFrame
        New table to add with unique keys
    """
    df1_ = df1.copy()
    df2_ = df2.copy()
    if len(df1_) == 0:
        return df2_
    else:
        tmp = (df1_.iloc[-1, 0] + np.arange(1, len(df2_) + 1)).astype(int)
        df2_.loc[:, 'customer_id'] = tmp
        return df2_


def add_tables_safely(
    table_name: Literal['demographic', 'debt', 'payment'],
    engine: sqlalchemy.engine.base.Engine,
    table: Tables
):
    """Function to add tables safely to SQL Database.

    Parameters
    ----------
    table_name: str
        Table name. Must be 'demographic', 'debt', or 'payment'

    engine: sqlalchemy.engine.base.Engine
        SQL connection.
        Created by sqlalchemy.create_engine

    table: Tables
        Tables class.

    Returns
    ----------
    None:
        Adds tables to SQL safely with unique customer_id.
    """
    current_table = pd.read_sql(sql=f'SELECT * FROM {table_name};', con=engine)
    if table_name == 'demographic':
        new_table = revise_table(current_table, table.demographic_table)
    elif table_name == 'debt':
        new_table = revise_table(current_table, table.debt_table)
    else:
        new_table = revise_table(current_table, table.payment_table)

    new_table.to_sql(table_name, con=engine, if_exists='append', index=False)
