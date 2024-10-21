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


def process_alert(alert: AlertRule, boat: BoatStatus):
    """Process a single alert, consider moving this to boat"""
    names = {"speed": boat.speed}
    alert.evaluate(names)
    return alert.raised


def monitoring_enabled_message(boat_alerts, aircraft_present):
    """Generate a monitoring message to dispatch

    Get a list of boat alerts {"alert_messages":[strings]}
    and a boolean indicating if an aircraft is present

    Returns a string with the message
    """
    # ret = boat_alerts["alert_messages"].join("\n")
    ret = "\n".join(boat_alerts["alert_messages"])
    if aircraft_present:
        ret += "\nAircraft present on scene"


def tracked_boat_alerts():
    """Iterate and evaluate all alerts in all boats in global status object

    returns a dict with "raised": True and a list of alert names if any alert rule match
    consider moving this to the status class

    return {"raised": boolean, "alert_messages": ["strings"] }
    """
    global status
    global boats_snapshot_df

    ret = {"raised": False, "alert_messages": []}
    for boat in status.boats:
        if not boat.alerts:
            continue

        for alert in boat.alerts:
            raised = process_alert(alert, boat)
            if raised:
                ret["raised"] = True
                ret["alert_messages"].append(alert.name)
    return ret


def set_monitor():
    """Perform logic to enable and disable status.monitor

    any boat that has actions defined is raised return true
    if any S&R Aircraft in the scene enable
    """
    global status
    global boats_snapshot_df
    global aircraft_snapshot_df

    boat_alerts = tracked_boat_alerts()
    aircraft_on_scene = len(aircraft_snapshot_df) > 0

    if boat_alerts["raised"] or aircraft_on_scene:
        if status.monitor == True:  # Already monitoring
            return
        else:  # Enabling
            status.monitor = True
            enable_message = monitoring_enabled_message(boat_alerts, aircraft_on_scene)

            filename = os.path.join(config.images_directory, "enabled.png")
            generate_map(filename)
            dispatch_message(enable_message, filename)
    else:
        if status.monitor == False:
            return
        else:
            dispatch_message("Disabling monitoring")
            return


def update_statuses() -> None:
    global status
    global boats_snapshot_df
    for boat in status.boats:
        mmsi = boat.mmsi
        name = boat.name
        query = f"mmsi == {mmsi} and ship_name.str.strip() == '{name}'"
        rows = boats_snapshot_df.query(query)
        if rows.empty:
            logging.debug(f"boat {mmsi}-{name} not in snapshot")
            continue
        row = rows.iloc[0]
        boat.speed = row["sog"]


def initialise_statuses() -> None:
    # Load tracked boats from config and initialise
    global status
    for boat in config.tracked_boats:
        mmsi = boat["mmsi"]
        if not isinstance(mmsi, int):
            logging.error(
                f"Boat mmsi is not an integer, fix config, not tracking {boat}"
            )
            continue

        name = str(boat["name"])
        color = str(boat["color"])
        boat_status = BoatStatus(mmsi=int(mmsi), name=name, color=color)
        if "alerts" in boat:
            alerts: list[AlertRule] = [AlertRule(**ar) for ar in boat["alerts"]]
            boat_status.alerts = alerts
        else:
            boat_status.alerts = []
        logging.info(f"adding: {boat_status}")
        status.boats.append(boat_status)


def schedule_tasks():
    schedule.every(15).seconds.do(reload_dataframes)
    schedule.every(15).seconds.do(update_statuses)
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
