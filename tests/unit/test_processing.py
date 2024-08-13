from datetime import datetime, timedelta
from numpy.dtypes import DateTime64DType
import pandas as pd
from utils import processing
from utils.processing import tracked_vessels, fix_datetime_columns


def test_fix_datetime_column():
    df = pd.read_csv("tests/data/boats.log.csv")
    df = fix_datetime_columns(df, ["server_timestamp"])
    assert type(df["server_timestamp"].dtype) == DateTime64DType


def test_empty_tracked_boats():
    df = pd.read_csv("tests/data/boats.log.csv")
    df = tracked_vessels(df, [])
    df = fix_datetime_columns(df)
    assert df.empty


def test_no_tracked_boats():
    tracked = [{"mmsi": 123}]
    df = pd.read_csv("tests/data/boats.log.csv")
    df = tracked_vessels(df, tracked)
    df = fix_datetime_columns(df)
    assert df.empty


def test_tracked_boat():
    tracked = [{"mmsi": 235118075}]
    df = pd.read_csv("tests/data/boats.log.csv")
    df = tracked_vessels(df, tracked)
    df = fix_datetime_columns(df)
    unique_boats = df["mmsi"].unique()
    assert unique_boats == [235118075]


def test_multiple_tracked_boats():
    tracked = [{"mmsi": 235118075}, {"mmsi": 235103844}]
    df = pd.read_csv("tests/data/boats.log.csv")
    df = tracked_vessels(df, tracked)
    df = fix_datetime_columns(df)
    unique_boats = df["mmsi"].unique()
    assert set(unique_boats) == set([235118075, 235103844])


def test_snapshot():
    tracked = [{"mmsi": 235118075}, {"mmsi": 235103844}]
    df = pd.read_csv("tests/data/boats.log.csv")
    snapshot = processing.snapshot(df)
    assert len(snapshot) == 140
    snapshot = processing.snapshot(df, tracked)
    assert len(snapshot) == 2


def test_newer_than():
    d = {
        "server_timestamp": [
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 1, 0, 29, 0),
            datetime(2024, 1, 1, 0, 31, 0),
            datetime(2024, 1, 1, 1, 0, 0),
        ]
    }
    df = pd.DataFrame(data=d)
    newer_than_datetime = datetime(2024, 1, 1, 0, 30, 0)
    df = processing.newer_than(df, newer_than_datetime)
    print(df)
    assert len(df) == 2


def test_filter_tracked():
    mmsis = [123, 456]
    d = {"mmsi": [123, 456, 678, 10, 11, 12]}
    df = pd.DataFrame(d)
    df = processing.filter_mmsis(df, mmsis)
    assert len(df) == 2
