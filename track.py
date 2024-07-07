""" Logs AIStream Events to CSV files """

from datetime import timedelta
import json
import csv
import asyncio
import logging
import websockets
from pathlib import Path

import config

from dtypes import AircraftPosition, BoatPosition
from utils.parsers import parse_position_report

# Holds a state for each vessels, indexed by mmsi
# e.g state["boats"]["mmsi"] = boat: BoatPosition
# e.g state["aircrafts"]["mmsi"] = aircraft: AircraftPosition
state = {
    "boats": {},
    "aircrafts": {},
}


def add_to_log(logfile, entry):
    headers = entry.keys()
    with open(logfile, mode="a", newline="") as f:
        writer = csv.DictWriter(f, headers)
        writer.writerow(entry)


def update_check(state: dict, entry: AircraftPosition | BoatPosition) -> bool:
    """Checks if entry should be logged

    if config.record_all = True, return true
    elif entry["mmsi"] not in state, add to state and return True
    elif config.interval passed state[mmsi].server_timestamp return true
    else return false

    Arguments:
    state: a dictionary to check entry against (boats of aircrafts)
    entry: entry to check against
    """

    mmsi = entry["mmsi"]
    timestamp = entry["server_timestamp"]
    if config.record_all:
        state[mmsi] = entry
        return True

    if mmsi not in state:
        state[mmsi] = entry
        return True

    if timestamp > state[mmsi]["server_timestamp"] + timedelta(
        seconds=config.update_interval
    ):
        state[mmsi] = entry
        return True

    return False


def update(message):
    message_type = message["MessageType"]
    if message_type == "PositionReport":
        record = parse_position_report(message)
        if update_check(state["boats"], record):
            add_to_log(config.boats_log_file, record)


async def connect_ais_stream():
    api_key = config.api_key
    arena = config.arena
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {
            "APIKey": api_key,
            "BoundingBoxes": arena,
            # "FiltersShipMMSI": ["368207620", "367719770", "211476060"], # Optional!
            "FilterMessageTypes": [
                "PositionReport",
                "StandardSearchAndRescueAircraftReport",
            ],
        }

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            update(message)


def initilise():
    # Create logfiles if needed
    if not Path(config.boats_log_file).is_file():
        logging.info(f" creating csv logfile {config.boats_log_file}")
        headers = BoatPosition.__annotations__.keys()
        with open(config.boats_log_file, mode="a", newline="") as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
    if not Path(config.aircrafts_log_file).is_file():
        logging.info(f" creating csv logfile {config.aircrafts_log_file}")
        headers = AircraftPosition.__annotations__.keys()
        with open(config.aircrafts_log_file, mode="a", newline="") as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()


def main():
    initilise()
    print("Tracking...")
    asyncio.run(connect_ais_stream())


if __name__ == "__main__":
    main()