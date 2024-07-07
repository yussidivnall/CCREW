import pandas as pd
from datetime import datetime, timedelta


def tail_log(df, rows=-1000, oldest=600):
    """returns N rows from end of dataframe, filter out  entries older then oldest seconds"""
    df = df.iloc[rows:]
    timeout = datetime.now() - timedelta(seconds=oldest)
    mask = df["server_timestamp"] > timeout
    df = df.loc[mask]
    return df


def fix_datetime_columns(df: pd.DataFrame, columns=["server_timestamp"]):
    """sets type of columns datetime in pandas dataframe"""
    for column_name in columns:
        col = df[column_name]
        col = pd.to_datetime(col)
        df[column_name] = col
    return df
