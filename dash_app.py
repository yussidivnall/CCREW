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
fig = None


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


def prepare_aircraft_dataframe(aircraft: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the aircraft dataframe from log to presentation
    - Remove entries older then 15 minutes
    - sorts
    - add colour column
    - ...?

    return dataframe to graph
    """
    aircraft = processing.tail_log(aircraft)
    aircraft["color"] = "blue"
    return aircraft


def load_boats() -> pd.DataFrame:
    boats_logfile = config.boats_log_file
    # aircraft_logfile = "aircraft.log.csv"
    boats_df = pd.read_csv(boats_logfile)  # , dtype={"server_timestamp": datetime})
    boats_df = processing.fix_datetime_columns(boats_df)
    boats_df = prepare_boats_dataframe(boats_df)
    return boats_df


def load_aircraft() -> pd.DataFrame:
    aircraft_logfile = config.aircraft_log_file
    # aircraft_logfile = "aircraft.log.csv"
    aircraft_df = pd.read_csv(
        aircraft_logfile
    )  # , dtype={"server_timestamp": datetime})
    aircraft_df = processing.fix_datetime_columns(aircraft_df)
    aircraft_df = prepare_aircraft_dataframe(aircraft_df)
    return aircraft_df


def draw():
    boats_df = load_boats()
    aircraft_df = load_aircraft()

    # latest state of all boats
    boats_snapshot_df = processing.snapshot(boats_df)
    aircraft_snapshot_df = processing.snapshot(aircraft_df)

    # latest_boat_positions_df = processing.latest_states(boats_df.copy())
    tracked_boats_df = processing.tracked_vessels(boats_df, config.tracked_boats)
    traces = plotting.get_tracked_traces(tracked_boats_df, config.tracked_boats)

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(uirevision=True)
    fig.update_layout(transition_duration=500)
    return fig


def create_figure():
    boats_df = load_boats()
    aircraft_df = load_aircraft()

    # latest state of all boats
    boats_snapshot_df = processing.snapshot(boats_df)
    aircraft_snapshot_df = processing.snapshot(aircraft_df)

    # latest_boat_positions_df = processing.latest_states(boats_df.copy())
    tracked_boats_df = processing.tracked_vessels(boats_df, config.tracked_boats)
    traces = plotting.get_tracked_traces(tracked_boats_df, config.tracked_boats)

    fig: Figure = plotting.plot_map(boats_snapshot_df, arena=config.arena)
    # fig: Figure = plotting.plot_map(latest_boat_positions_df, arena=config.arena)

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(uirevision=True)
    fig.update_layout(transition_duration=500)
    return fig


def update_figure():
    boats_df = load_boats()
    aircraft_df = load_aircraft()

    # latest state of all boats
    boats_snapshot_df = processing.snapshot(boats_df)
    aircraft_snapshot_df = processing.snapshot(aircraft_df)

    # latest tracked
    tracked_boats_df = processing.tracked_vessels(boats_df, config.tracked_boats)
    pass


@app.callback(Output("map", "figure"), [Input("update-interval", "n_intervals")])
def update(value):
    print(value)
    print("Updating")
    # TODO, should update data, not recreate each time
    fig = create_figure()
    return fig


if __name__ == "__main__":
    fig = create_figure()
    app.run(debug=True, use_reloader=True)
