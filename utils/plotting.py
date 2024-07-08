import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure, Scattergeo


def get_tracked_traces(df: pd.DataFrame, tracked: list) -> list:
    """ """
    traces = []
    for vessel in tracked:
        mmsi = vessel["mmsi"]
        color = vessel["color"]
        vessel_df = df[df["mmsi"] == mmsi]
        trace = Scattergeo(
            lon=vessel_df["lon"],
            lat=vessel_df["lat"],
            mode="lines+markers",
            line=dict(width=2, color=color),
            marker=dict(size=6, symbol="circle", color=color),
            name=str(mmsi),
        )
        traces.append(trace)
    return traces


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
