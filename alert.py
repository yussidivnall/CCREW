import schedule
import time
import pandas as pd

from utils import processing
import config

status = {}
boats_df: pd.DataFrame
aircrafts_df: pd.DataFrame


def reload_dataframes():
    global boats_df
    global aircrafts_df

    boats_df, aircrafts_df = processing.load_dataframes()


def update_region_statuses():
    pass


def update_online_statuses():
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


def main():
    reload_dataframes()
    schedule.every(1).seconds.do(reload_dataframes)
    schedule.every(1).seconds.do(update_statuses)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
