import schedule
import time
import pandas as pd

from dtypes import BoatStatus, Region, AlertsStatus
from utils import processing, logic
import config

status: AlertsStatus = {"monitor": False, "boats": {}}
boats_df: pd.DataFrame
aircrafts_df: pd.DataFrame

boats_snapshot_df: pd.DataFrame
aircrafts_snapshot_df: pd.DataFrame


def reload_dataframes():
    global boats_df
    global aircrafts_df
    global boats_snapshot_df
    global aircrafts_snapshot_df

    boats_df, aircrafts_df = processing.load_dataframes()

    # Snapshot of latest position reports
    boats_snapshot_df = processing.snapshot(boats_df)
    aircrafts_snapshot_df = processing.snapshot(aircrafts_df)


def update_regions():
    """Updates the regions in the global statuses"""
    print()
    global boats_snapshot_df, aircrafts_snapshot_df, status
    regions = config.regions

    for mmsi in status["boats"].keys():
        boat = boats_snapshot_df[boats_snapshot_df.mmsi == mmsi].iloc[0]
        # lat, lon = boat[["lat", "lon"]]
        for region_key in regions:
            r = regions[region_key]
            reg: Region = r
            in_region = logic.boat_in_region(boat, reg)
            print(boat["ship_name"])
            print(in_region)


def monitor_job():
    pass


def update_statuses():
    global boats_df
    global aircrafts_df
    print(boats_df)
    tracked_boats_df = processing.tracked_vessels(boats_df, config.tracked_boats)
    tracked_boats_snapshot_df = processing.snapshot(tracked_boats_df)
    for b in config.tracked_boats:
        mmsi = b["mmsi"]
        for region_key in config.regions.keys():
            region = config.regions[region_key]
        pass


def initilise_statuses():
    global status
    for boat in config.tracked_boats:
        mmsi = boat["mmsi"]
        name = boat["name"]

        boat_status: BoatStatus = {
            "mmsi": mmsi,
            "name": name,
            "in_regions": [],
            "online": False,
        }
        status["boats"][mmsi] = boat_status
    print(status)


def main():
    reload_dataframes()
    initilise_statuses()
    schedule.every(1).seconds.do(reload_dataframes)
    schedule.every(1).seconds.do(update_regions)
    # schedule.every(1).seconds.do(update_statuses)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
