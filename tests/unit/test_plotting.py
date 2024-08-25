from datetime import datetime
from unittest.mock import patch
from dtypes import AlertsStatus
from utils import processing, plotting


# @patch("arena", [[[51.399, 2.2666], [50.85, 0.639]]]})
def test_monitoring_map():
    arena = [[[51.399, 2.2666], [50.85, 0.639]]]

    boats_df, aircrafts_df = processing.load_dataframes(
        "tests/data/boats.log.csv",
        "tests/data/aircrafts.log.csv",
    )
    status: AlertsStatus = {
        "monitor": False,
        "boats": {
            235118075: {
                "mmsi": 235118075,
                "name": "BF HURRICANE",
                "in_regions": [],
                "online": True,
                "home": None,
                "color": "blue",
            },
            235102528: {
                "mmsi": 235102528,
                "name": "BF VOLUNTEER",
                "in_regions": [],
                "online": True,
                "home": None,
                "color": "yellow",
            },
            235098051: {
                "mmsi": 235098051,
                "name": "BF DEFENDER",
                "in_regions": [],
                "online": True,
                "home": None,
                "color": "red",
            },
            235103844: {
                "mmsi": 235103844,
                "name": "BF RANGER",
                "in_regions": [],
                "online": True,
                "home": None,
                "color": "green",
            },
        },
        "aircrafts": {},
    }

    boats_df = processing.newer_than(boats_df, datetime(2024, 7, 8))
    aircrafts_df = processing.newer_than(aircrafts_df, datetime(2024, 8, 17))

    # boats_snapshot_df = processing.snapshot(boats_df)
    # aircrafts_snapshot_df = processing.snapshot(aircrafts_df)
    # fig = plotting.plot_map(boats_snapshot_df, arena=arena)

    fig = plotting.plot_scene(arena, boats_df, aircrafts_df, status)

    fig.show()
    print("Noooo")
    # assert False


# import pandas as pd
# from plotly.graph_objects import Scattergeo
# from utils.processing import fix_datetime_columns, tracked_vessels
# from utils.plotting import get_tracked_traces
#
# TODO
# def test_traces():
#     tracked = [
#         {"mmsi": 235118075},
#         {"mmsi": 235102528},
#         {"mmsi": 235098051},
#         {"mmsi": 235103844},
#     ]
#
#     df = pd.read_csv("tests/data/boats.log.csv")
#     df = tracked_vessels(df, tracked)
#     df = fix_datetime_columns(df)
#
#     traces = get_tracked_traces(df, tracked)
#     assert len(traces) == 4
#     for trace in traces:
#         assert type(trace) is Scattergeo
#     print(traces)
#     # assert traces == []
