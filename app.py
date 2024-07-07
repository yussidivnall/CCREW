# from datetime import datetime, timedelta
from dash import Dash, html, dcc
from dash import Input, Output
import pandas as pd
import plotly.express as px
from utils import processing
import config


app = Dash()
app.layout = [
    html.H1(children="Channel Crossing  Research"),
    dcc.Graph(id="map"),
    dcc.Interval(
        id="update-interval", interval=config.update_interval * 1000, n_intervals=0
    ),
]


def plot_map(data, arena):
    arena_bounds = {
        "east": arena[0][0][1],
        "west": arena[0][1][1],
        "south": arena[0][1][0],
        "north": arena[0][0][0],
    }

    fig = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lon",
        text="ship_name",
        color="color",
        zoom=3,
        height=700,
        width=1400,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.update_layout(mapbox_bounds={"west": 0.5, "east": 2.3, "south": 50.5, "north": 51.5})
    fig.update_layout(mapbox_bounds=arena_bounds)
    fig.update_layout(uirevision=True)
    return fig


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


def latest_states(boats: pd.DataFrame) -> pd.DataFrame:
    boats = boats.loc[boats.groupby("mmsi")["server_timestamp"].idxmax()]
    return boats


def draw():
    boats_df = load_boats()
    latest_positions_df = latest_states(boats_df)
    fig = plot_map(latest_positions_df, arena=config.arena)
    return fig


@app.callback(Output("map", "figure"), [Input("update-interval", "n_intervals")])
def update(value):
    print(value)
    print("Updating")
    fig = draw()
    return fig


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
