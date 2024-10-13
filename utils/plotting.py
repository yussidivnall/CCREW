from datetime import timedelta
import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure, Scattergeo, Scattermapbox

from dtypes import Status
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
    df["ship_name"] = df["ship_name"].astype(str)
    ret = go.Scattermapbox(
        lat=df["lat"],
        lon=df["lon"],
        mode="markers+text",
        # marker=dict(symbol="circle"),
        marker=dict(
            color="#A0A0A0",
            # symbol="square",
            size=4,
            # angle="previous",
        ),
        # name=f"{group['ship_name']}",
        text=df["ship_name"],
        textposition="top right",
        showlegend=False,
        # hoverinfo="text",
    )
    return ret


def label_trace(group: pd.DataFrame, color="gray", text=None):
    """Add a trace with only the last point and a label"""

    # Sometimes we want to give a label (for planes)
    if text:
        t = [text]
    else:
        t = [group["ship_name"].iloc[-1]]

    ret = go.Scattermapbox(
        lat=[group["lat"].iloc[-1]],
        lon=[group["lon"].iloc[-1]],
        mode="markers+text",
        marker=dict(
            color=color,
            size=12,
        ),
        text=t,
        textposition="top right",
        showlegend=False,
    )
    return ret


def vessel_path_trace(group, symbol="circle", color="gray"):
    print(group["ship_name"])
    ret = go.Scattermapbox(
        lat=group["lat"],
        lon=group["lon"],
        mode="lines",
        line=dict(color=color),
        marker=dict(
            color=color,
            size=15,
        ),
        text=group["ship_name"].iloc[-1],
        textposition="top right",
        hoverinfo="text",
        showlegend=True,
    )
    return ret


def plot_scene(
    arena,
    boats: pd.DataFrame,
    aircraft: pd.DataFrame,
    status: Status,
    zoom: float = 8.2,
) -> Figure:
    """Plots the scene for alerts

    plots all boats last known position (TODO)
    plots tracked boats path
    plots aircraft path
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

    # TODO
    # arena_trace = get_region_trace()

    fig: Figure = go.Figure()
    fig.add_trace(go.Scattermapbox())
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Use OpenStreetMap as the background
            center=dict(
                lat=center["lat"],
                lon=center["lon"],
            ),
            zoom=zoom,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Snapshot of all boats
    boats_snapshot_trace = vessel_snapshot_trace(boats)
    fig.add_trace(boats_snapshot_trace)
    # Trace for tracked boats
    tracked_boats_mmsis = [m.mmsi for m in status.boats]
    tracked_boats = processing.filter_mmsis(boats, tracked_boats_mmsis)
    tracked_boats = processing.sieve_timedelta(tracked_boats, timedelta(seconds=60))
    for idx, boat in tracked_boats.groupby(["mmsi", "ship_name"]):
        print(idx)
        print()
        mmsi = int(idx[0])
        name = str(idx[1]).strip()
        boat_status = status.get_boat(mmsi, name)
        if not boat_status:
            logging.error(
                f"boat {mmsi} - {name} not found in status object, not adding trace, ensure the name is correct in config"
            )
            continue
        color = boat_status.color

        trace = vessel_path_trace(boat, color=color)
        trace.name = name
        fig.add_trace(trace)
        label = label_trace(boat, color)
        fig.add_trace(label)
    # Trace all aircraft
    for mmsi, group in aircraft.groupby("mmsi"):
        trace = vessel_path_trace(group, symbol="triangle")
        name = f"Aircraft {mmsi}"
        trace.name = name
        fig.add_trace(trace)
        label = label_trace(group, text=name)
        fig.add_trace(label)

    return fig
