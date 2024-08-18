from inspect import Arguments
from typing import Dict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure, Scattergeo, Scattermapbox

from dtypes import AlertsStatus
from utils import processing


def get_tracked_traces(df: pd.DataFrame, tracked: list) -> list:
    """ """
    traces = []
    for vessel in tracked:
        mmsi = vessel["mmsi"]
        name = vessel["name"]
        # color = vessel["color"]
        # print(color)
        vessel_df = df[df["mmsi"] == mmsi]
        trace = Scattermapbox(
            lon=vessel_df["lon"],
            lat=vessel_df["lat"],
            mode="lines+markers",
            line=dict(width=2),
            # line=dict(width=2, color="teal"),
            marker=dict(size=6, symbol="circle"),
            name=name,
        )
        traces.append(trace)
    return traces


def get_region_trace(region):
    """get a trace for a single enclosed region

    Arguments:
        region: a dictionary containing lat, lon points around region and a label, eg { lat:[...], lon:[...], label
        name: a name of the region
    Returns: A Scattermapbox
    """
    trace = go.Scattermapbox(
        lon=region["lon"], lat=region["lat"], fill="toself", name=region["name"]
    )
    return trace


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
        title="ship_name",
        # color="color",
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


def vessel_snapshot_trace(df, symbol="circle"):
    df = processing.snapshot(df)
    ret = go.Scattermapbox(
        lat=df["lat"],
        lon=df["lon"],
        # mode="lines+markers",
        # marker=dict(symbol="circle"),
        marker=dict(
            symbol=symbol,
            size=15,
            # angle="previous",
        ),
        # name=f"{group['ship_name']}",
        # text=df["ship_name"].iloc[-1],
        # textposition="top right",
        # hoverinfo="text",
    )
    return ret


def vessel_path_trace(group, symbol="circle"):
    print(group["ship_name"])
    ret = go.Scattermapbox(
        lat=group["lat"],
        lon=group["lon"],
        mode="lines+markers",
        # marker=dict(symbol="circle"),
        marker=dict(
            symbol=symbol,
            size=15,
            # angle="previous",
        ),
        # name=f"{group['ship_name']}",
        text=group["ship_name"].iloc[-1],
        textposition="top right",
        hoverinfo="text",
        showlegend=True,
    )
    return ret


def plot_scene(
    arena, boats: pd.DataFrame, aircrafts: pd.DataFrame, status: AlertsStatus
) -> Figure:
    """Plots the scene for alerts

    plots all boats last known position (TODO)
    plots tracked boats path
    plots aircrafts path
    """
    arena_bounds = {
        "east": arena[0][0][1],
        "west": arena[0][1][1],
        "south": arena[0][1][0],
        "north": arena[0][0][0],
    }
    center = {
        "lat": (arena_bounds["north"] + arena_bounds["south"]) / 2,
        "lon": (arena_bounds["west"] + arena_bounds["east"]) / 2,
    }

    fig: Figure = go.Figure()
    fig.add_trace(go.Scattermapbox())
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Use OpenStreetMap as the background
            center=dict(
                lat=center["lat"],
                lon=center["lon"],
            ),
            zoom=8.8,  # Adjust the zoom level
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Snapshot of all boats
    # boats_snapshot_trace = vessel_snapshot_trace(boats)
    # fig.add_trace(boats_snapshot_trace)

    # Trace for tracked boats
    tracked_boats_mmsis = [m for m in status["boats"]]
    tracked_boats = processing.filter_mmsis(boats, tracked_boats_mmsis)
    for mmsi, group in tracked_boats.groupby("mmsi"):
        trace = vessel_path_trace(group)
        m = pd.to_numeric(mmsi)
        name = status["boats"][int(m)]["name"]
        # trace.name = status["boats"][int(mmsi)]
        trace.name = name
        fig.add_trace(trace)
    # Trace all aircrafts
    for mmsi, group in aircrafts.groupby("mmsi"):
        trace = vessel_path_trace(group, symbol="2")
        fig.add_trace(trace)

    return fig
