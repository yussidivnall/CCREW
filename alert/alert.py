from typing import cast
import json
import logging
import os
import time
from datetime import datetime, timedelta

import pandas as pd
import schedule
from discord_webhook import DiscordWebhook

import config
from alert.rules import AlertRule
from dtypes import Status, BoatStatus, Region
from utils import logic, plotting, processing

status = Status()
boats_df: pd.DataFrame
aircraft_df: pd.DataFrame

boats_snapshot_df = pd.DataFrame()
aircraft_snapshot_df = pd.DataFrame()


def reload_dataframes():
    global boats_df
    global aircraft_df
    global boats_snapshot_df
    global aircraft_snapshot_df

    boats_df, aircraft_df = processing.load_dataframes()

    # Snapshot of latest position reports
    boats_snapshot_df = processing.snapshot(boats_df, stale=timedelta(minutes=15))
    aircraft_snapshot_df = processing.snapshot(aircraft_df, stale=timedelta(minutes=15))


def dump_status():
    global status
    print(json.dumps(status, indent=2))


def dispatch_message(message, image=None):
    # Post a message to discord
    logging.info(f"discord msg: {message}")
    webhook = DiscordWebhook(url=config.discord_webhook_url, content=message)
    if image:
        with open(image, "rb") as f:
            webhook.add_file(f.read(), filename="monitoring.png")
    webhook.execute()


def generate_map(filename):
    global boats_df
    global aircraft_df
    global status
    boats = processing.newer_than(boats_df, datetime.now() - timedelta(minutes=60))
    aircraft = processing.newer_than(
        aircraft_df, datetime.now() - timedelta(minutes=60)
    )
    fig = plotting.plot_scene(config.arena, boats, aircraft, status)
    fig.write_image(filename)


def monitor_job():
    """Check if status.monitor is set and post update"""
    global status
    if not status.monitor:
        return

    filename = os.path.join(config.images_directory, "monitoring.png")
    generate_map(filename)
    message = f"{datetime.now()} - Monitoring"
    dispatch_message(message, filename)

    # fig.show()
    # pass


def tracked_boat_alerts():
    global status
    global boats_snapshot_df
    for boat in status.boats:
        mmsi = boat.mmsi
        for alert in boat.alerts:
            pass
    #
    #    # for boat_status in status["


def set_monitor():
    """Perform logic to enable and disable status.monitor

    any boat that has actions defined is raised return true
    if aircraft active, set to True and return, otherwise False
    """
    global status
    global boats_snapshot_df
    global aircraft_snapshot_df

    tracked_boat_alerts()
    # Any aircraft enables monitoring
    if len(aircraft_snapshot_df) > 0:
        if status.monitor == True:
            # Aircraft present but already monitoring
            return
        else:
            status.monitor = True
            filename = os.path.join(config.images_directory, "enabled.png")
            generate_map(filename)
            dispatch_message("Aircraft pesent in scene, enabling monitoring", filename)
            return

    # No alerts
    if status.monitor is False:
        return
    else:
        status.monitor = False
        dispatch_message("Disabling monitoring")


def update_statuses() -> None:
    global status
    global boats_snapshot_df
    for boat in status.boats:
        mmsi = boat.mmsi
        row = boats_snapshot_df[boats_snapshot_df[mmsi] == mmsi]
        pass


def initialise_statuses() -> None:
    # Load tracked boats from config and initialise
    global status
    for boat in config.tracked_boats:
        mmsi = int(boat["mmsi"])
        name = str(boat["name"])
        color = str(boat["color"])
        boat_status = BoatStatus(mmsi=mmsi, name=name, color=color)
        if "alerts" in boat:
            alerts: list[AlertRule] = [AlertRule(**ar) for ar in boat["alerts"]]
            boat_status.alerts = alerts
        else:
            boat_status.alerts = []
        logging.info("adding: {}", boat_status)
        status.boats.append(boat_status)


def schedule_tasks():
    schedule.every(15).seconds.do(reload_dataframes)
    schedule.every(30).seconds.do(set_monitor)
    schedule.every(900).seconds.do(monitor_job)  # should be every 15 minutes


async def run():
    reload_dataframes()
    initialise_statuses()
    schedule_tasks()
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    reload_dataframes()
    initialise_statuses()
    schedule.every(15).seconds.do(reload_dataframes)
    schedule.every(30).seconds.do(set_monitor)
    schedule.every(900).seconds.do(monitor_job)  # should be every 15 minutes
    logging.info("Monitoring")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
