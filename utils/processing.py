from datetime import datetime, timedelta

import pandas as pd

import config
from dtypes import AircraftPosition, BoatPosition


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


def filter_mmsis(df: pd.DataFrame, mmsis: list):
    """Return only rows with 'mmsi' in mmsis"""
    mask = df["mmsi"].isin(mmsis)
    ret = df.loc[mask].copy()
    return ret


def latest_states(vessels: pd.DataFrame) -> pd.DataFrame:
    """Returns latest entry of each vessel in dataframe groupped by mmsi"""
    vessels = vessels.loc[vessels.groupby("mmsi")["server_timestamp"].idxmax()]
    return vessels


def newer_than(df: pd.DataFrame, oldest: datetime) -> pd.DataFrame:
    ret = df.copy()[df["server_timestamp"] > oldest]
    return ret


def snapshot(
    df: pd.DataFrame,
    tracked: list | None = None,
    stale: None | timedelta = None,
) -> pd.DataFrame:
    """Returns latest entry of each vessel in dataframe groupped by mmsi"""
    ret = df.copy()
    ret = ret.loc[df.groupby("mmsi")["server_timestamp"].idxmax()]
    if tracked is not None:
        ret = tracked_vessels(ret, tracked)
    if stale:
        ret = newer_than(ret, datetime.now() - stale)
    return ret


def tracked_vessels(vessels: pd.DataFrame, tracking_vessels: list) -> pd.DataFrame:
    """Return a dataframe with only tracked vessels present in tracking_vessels
    @ Probably replaced with filter_mmsis

    Args:
        vessels - dataframe
        tracking_vessels - list of boat objects

    trackiong vessels probably comes from config and looks like this
    [{"mmsi":123, "label": "Label To Apply To Boat", "name": "Anything, not really used for nothing"}, ...]
    """
    mmsis = [vessel["mmsi"] for vessel in tracking_vessels]
    print(mmsis)
    mask = vessels["mmsi"].isin(mmsis)
    ret = vessels.loc[mask].copy()
    return ret


def load_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    """A helper to load both boat and aircraft log dataframe

    Returns a tuple of both dataframes
    """
    boats = pd.read_csv(config.boats_log_file)
    aircrafts = pd.read_csv(config.aircrafts_log_file)

    boats["server_timestamp"] = pd.to_datetime(boats["server_timestamp"])
    aircrafts["server_timestamp"] = pd.to_datetime(aircrafts["server_timestamp"])

    return (boats, aircrafts)
