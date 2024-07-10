# from datetime import datetime, timedelta
from dash import Dash, html, dcc
from dash import Input, Output
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from utils import processing, plotting
import config


app = Dash()
app.layout = [
    html.H1(children="Channel Crossing  Research"),
    dcc.Graph(id="map"),
    dcc.Interval(
        id="update-interval", interval=config.update_interval * 1000, n_intervals=0
    ),
]


def prepare_boats_dataframe(boats: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the boats dataframe from log to presentation
    - Remove entries older then 15 minutes
    - sorts
    - add colour column
    - ...?

    return dataframe to graph
    """
    boats = processing.tail_log(boats)
    boats["color"] = "red"
    return boats


def prepare_aircrafts_dataframe(aircrafts: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the aircrafts dataframe from log to presentation
    - Remove entries older then 15 minutes
    - sorts
    - add colour column
    - ...?

    return dataframe to graph
    """
    aircrafts = processing.tail_log(aircrafts)
    aircrafts["color"] = "blue"
    return aircrafts


def load_boats() -> pd.DataFrame:
    boats_logfile = config.boats_log_file
    # aircraft_logfile = "aircraft.log.csv"
    boats_df = pd.read_csv(boats_logfile)  # , dtype={"server_timestamp": datetime})
    boats_df = processing.fix_datetime_columns(boats_df)
    boats_df = prepare_boats_dataframe(boats_df)
    return boats_df


def load_aircrafts() -> pd.DataFrame:
    aircrafts_logfile = config.aircrafts_log_file
    # aircraft_logfile = "aircraft.log.csv"
    aircrafts_df = pd.read_csv(
        aircrafts_logfile
    )  # , dtype={"server_timestamp": datetime})
    aircrafts_df = processing.fix_datetime_columns(aircrafts_df)
    aircrafts_df = prepare_aircrafts_dataframe(aircrafts_df)
    return aircrafts_df


def draw():
    boats_df = load_boats()
    aircraft_df = load_aircrafts()

    # latest_boat_positions_df = processing.latest_states(boats_df.copy())
    tracked_boats_df = processing.tracked_vessels(boats_df, config.tracked_boats)
    traces = plotting.get_tracked_traces(tracked_boats_df, config.tracked_boats)

    df = pd.DataFrame(data={"mmsi": 0, "lat": 0, "lon": 0})

    fig: Figure = plotting.plot_map(boats_df, arena=config.arena)
    # fig: Figure = plotting.plot_map(latest_boat_positions_df, arena=config.arena)

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(uirevision=True)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(Output("map", "figure"), [Input("update-interval", "n_intervals")])
def update(value):
    print(value)
    print("Updating")
    fig = draw()
    return fig


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
