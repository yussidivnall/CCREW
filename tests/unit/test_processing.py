from numpy.dtypes import DateTime64DType
import pandas as pd
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
