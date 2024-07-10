import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure, Scattergeo, Scattermapbox


def get_tracked_traces(df: pd.DataFrame, tracked: list) -> list:
    """ """
    traces = []
    for vessel in tracked:
        mmsi = vessel["mmsi"]
        # color = vessel["color"]
        # print(color)
        vessel_df = df[df["mmsi"] == mmsi]
        trace = Scattermapbox(
            lon=vessel_df["lon"],
            lat=vessel_df["lat"],
            mode="lines+markers",
            # line=dict(width=2),
            line=dict(width=2, color="teal"),
            marker=dict(size=6, symbol="circle"),
            name=str(mmsi),
        )
        traces.append(trace)
    return traces

def get_region()


def plot_map(data, arena) -> Figure:

    arena_bounds = {
        "east": arena[0][0][1],
        "west": arena[0][1][1],
        "south": arena[0][1][0],
        "north": arena[0][0][0],
    }

    fig: Figure = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lon",
        text="ship_name",
        color="color",
        labels="ship_name",
        zoom=3,
        height=700,
        width=1400,
    )
    fig.update_layout(mapbox_style="open-street-map")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(mapbox_bounds=arena_bounds)
    fig.update_layout(uirevision=True)
    return fig
