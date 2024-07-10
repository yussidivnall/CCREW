import pandas as pd
from datetime import datetime, timedelta


def tail_log(df, rows=-50000, oldest=1800):
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


def latest_states(vessels: pd.DataFrame) -> pd.DataFrame:
    """Returns latest entry of each vessel in dataframe groupped by mmsi"""
    vessels = vessels.loc[vessels.groupby("mmsi")["server_timestamp"].idxmax()]
    return vessels


def snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Returns latest entry of each vessel in dataframe groupped by mmsi"""
    ret = df.copy()
    df = df.loc[df.groupby("mmsi")["server_timestamp"].idxmax()]
    return df


def tracked_vessels(vessels: pd.DataFrame, tracking_vessels: list) -> pd.DataFrame:
    """Return a dataframe with only tracked vessels present in tracking_vessels

    trackiong vessels probably comes from config and looks like this
    [{"mmsi":123, "label": "Label To Apply To Boat", "name": "Anything, not really used for nothing"}, ...]
    """
    mmsis = [vessel["mmsi"] for vessel in tracking_vessels]
    mask = vessels["mmsi"].isin(mmsis)
    ret = vessels.loc[mask].copy()
    return ret
