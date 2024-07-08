import pandas as pd
from plotly.graph_objects import Scattergeo
from utils.processing import fix_datetime_columns, tracked_vessels
from utils.plotting import get_tracked_traces


def test_traces():
    tracked = [
        {"mmsi": 235118075},
        {"mmsi": 235102528},
        {"mmsi": 235098051},
        {"mmsi": 235103844},
    ]

    df = pd.read_csv("tests/data/boats.log.csv")
    df = tracked_vessels(df, tracked)
    df = fix_datetime_columns(df)

    traces = get_tracked_traces(df, tracked)
    assert len(traces) == 4
    for trace in traces:
        assert type(trace) is Scattergeo
    print(traces)
    # assert traces == []
