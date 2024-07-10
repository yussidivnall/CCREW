""" Produces a snapshot image of the arena, stores to "images/snap.png" """

import os
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import plotly.express as px
import config
from utils import processing, plotting


def main():
    if not os.path.exists(config.images_directory):
        os.mkdir(config.images_directory)

    boats_logfile = config.boats_log_file
    boats_df = pd.read_csv(boats_logfile)  # , dtype={"server_timestamp": datetime})
    boats_df = processing.fix_datetime_columns(boats_df)
    boats_df = processing.tail_log(boats_df)
    boats_df["color"] = "gray"

    # latest state of all boats
    snapshot_df = processing.snapshot(boats_df)

    # fig: Figure = plotting.plot_map(boats_df, arena=config.arena)
    # fig: Figure = plotting.plot_map(snapshot_df, arena=config.arena)
    fig: Figure = plotting.plot_map(snapshot_df, arena=config.arena)

    port = plotting.get_region_trace(config.regions["port"])
    fig.add_trace(port)
    print(fig)

    tracked_boats_df = processing.tracked_vessels(boats_df, config.tracked_boats)
    traces = plotting.get_tracked_traces(tracked_boats_df, config.tracked_boats)
    for trace in traces:
        fig.add_trace(trace)

    filename = os.path.join(config.images_directory, "snapshot.png")
    fig.write_image(filename)
    fig.show()


if __name__ == "__main__":
    main()
