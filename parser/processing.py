import pandas as pd
import numpy as np

from config import COLUMNS


def read_table(filename: str) -> pd.DataFrame:
    print(f'Чтение {filename}')
    df: pd.DataFrame = pd.read_excel(filename)

    start_index, end_index = get_table_position(df)
    df = get_raw_table(df, start_index, end_index)
    df = get_cleaned_table(df)

    df = df[df['количество договоров, шт.'].astype(int) > 0]
    return df


def get_raw_table(df, start_index, end_index):
    table = df.iloc[start_index + 3 : end_index, 1:]
    columns_line = df.iloc[start_index + 1, 1:]
    table.columns = prepare_columns(columns_line)
    table = table[COLUMNS]
    return table


def get_table_position(df: pd.DataFrame) -> tuple[int, int]:
    start_index = df[
        df.iloc[:, 1] == 'Единица измерения: Метрическая тонна'
    ].index[0]
    end_index = df.iloc[start_index:, 1][
        df.iloc[start_index:, 1] == 'Итого:'
    ].index[0]
    return start_index, end_index


def get_cleaned_table(df: pd.DataFrame) -> pd.DataFrame:
    table = df.replace('-', np.nan)
    table = table.dropna(subset=['количество договоров, шт.'])
    table = table[table['количество договоров, шт.'].astype(int) > 0]
    return table


def prepare_columns(columns):
    columns = columns.replace('\n', ' ', regex=True)
    columns = columns.str.lower()
    return columns
