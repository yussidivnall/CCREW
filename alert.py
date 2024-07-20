import logging
import schedule
import time
import pandas as pd

from dtypes import BoatStatus, Region, AlertsStatus
from utils import processing, logic
import config

status: AlertsStatus = {"monitor": False, "boats": {}}
boats_df: pd.DataFrame
aircrafts_df: pd.DataFrame

boats_snapshot_df = pd.DataFrame()
aircrafts_snapshot_df = pd.DataFrame()


def reload_dataframes():
    global boats_df
    global aircrafts_df
    global boats_snapshot_df
    global aircrafts_snapshot_df

    boats_df, aircrafts_df = processing.load_dataframes()

    # Snapshot of latest position reports
    boats_snapshot_df = processing.snapshot(boats_df)
    aircrafts_snapshot_df = processing.snapshot(aircrafts_df)


def dump_status():
    global status
    print(json.dumps(status, indent=2))


def dispatch_message(message):
    # Post a message to discord
    print("LALALA")
    logging.info(message)
    print("Message is ", message)


def check_aircrafts():
    global status


def update_regions():
    """Updates the regions in the global statuses"""
    global boats_snapshot_df, aircrafts_snapshot_df, status
    regions = config.regions
    dispatch_message("Hello")
    dispatch_message(status)
    for mmsi in status["boats"].keys():
        dispatch_message(f"Boat {mmsi}")
        boat_status = status["boats"][mmsi]
        if "home" in boat_status.keys():
            home_key = boat_status["home"]
            home_region = regions[home_key]

        boat_snapshot = boats_snapshot_df[boats_snapshot_df.mmsi == mmsi].iloc[0]
        # lat, lon = boat[["lat", "lon"]]
        for region_key in regions:
            region: Region = regions[region_key]
            in_region = logic.boat_in_region(boat_snapshot, region)
            if in_region:
                # Boat is in region, check is it's in boat_status[region], If it is continue
                # If not, add to boat_status[regions] and dispatch message "Boat entered _region_.
                #
                # and check if it's also the home region
                # If it's the home region dispatch message "Boat has returned home"

                if region_key in boat_status["in_regions"]:
                    # Region already in status, do nothing
                    continue
                else:
                    boat_status["in_regions"].append(region_key)
                    dispatch_message(f"Boat {boat_status['name']} entered {region_key}")
                pass
            else:
                # If boat not in region
                # Check if region is in boat_status['region'], if so dispatch message "boat has left region"
                if region_key in boat_status["in_regions"]:
                    boat_status["in_regions"].remove(region_key)
                    dispatch_message(f"Boat {boat_status['name']} left {region_key}")


def monitor_job():
    """Check if status.monitor is set and post update"""
    pass


def set_monitor():
    """Perform logic to enable and disable status.monitor

    if aircraft active, or BF boats outside port set to True, otherwise False
    """
    global status
    # For all boat statuses
    # If any boat is not home, as in if boat_status["home"] not in boat_status["regions"]
    # set status_monitor to true
    # if any plane is active set status monitor to true


def check_offline():
    # Check if boat has not transmitted for a period, if not, dispatch message and se
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


def main():
    reload_dataframes()
    initilise_statuses()
    schedule.every(1).seconds.do(reload_dataframes)
    schedule.every(1).seconds.do(update_regions)
    schedule.every(1).seconds.do(set_monitor)
    schedule.every(1).seconds.do(monitor_job)  # should be every 15 minutes
    # schedule.every(10).seconds.do(dump_status)  # For development only
    logging.info("Monitoring")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
