import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geopandas as gpd
import config

data = {"long": [], "lat": [], "text": [], "cnt": []}


def plot_map(data, arena):
    arena = {
        "east": arena[0][0][1],
        "west": arena[0][1][1],
        "south": arena[0][1][0],
        "north": arena[0][0][0],
    }

    fig = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lon",
        text=data["name"],
        zoom=3,
        # height=300,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.update_layout(mapbox_bounds={"west": 0.5, "east": 2.3, "south": 50.5, "north": 51.5})
    fig.update_layout(mapbox_bounds=arena)
    return fig


# # boats = pd.DataFrame(data=data)
# boats = pd.read_csv(config.boats_state_file)
# # planes = pd.read_csv(config.planes_state_file)
# map = go.Figure(
#     data=go.Scattergeo(
#         lon = boats['lon'],
#         lat = boats['lat'],
#         text = boats['name'],
#         mode = 'markers',
#         # marker_color = boats['cnt'],
#         )
#     )


def main():
    boats = pd.read_csv(config.boats_state_file)
    # boats = gpd.read_file(config.boats_state_file)
    map = plot_map(boats, config.arena)
    map.show()


if __name__ == "__main__":
    main()
