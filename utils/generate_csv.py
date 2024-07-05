from datetime import datetime, timedelta, timezone
import asyncio
import json
from dash.dash import logging
import websockets
import config
import csv
import parsers

# from pathlib import Path

state = {
    # Dictionaries, "mmsi" is the index key
    "boats": {},
    "planes": {},
}


def clean_stale_entries():
    # current = datetime.now(datetime.timezone.utc)
    # current = datetime.now(datetime.timezone.utc)
    current = datetime.now(timezone.utc)
    state["boats"] = {
        mmsi: boat
        for mmsi, boat in state["boats"].items()
        if boat["time"] + timedelta(seconds=600) >= current
    }
    state["planes"] = {
        mmsi: plane
        for mmsi, plane in state["planes"].items()
        if plane["time"] + timedelta(seconds=600) >= current
    }


def save_state(csvfile: str, state: dict):
    clean_stale_entries()
    first_key = next(iter(state))
    headers = state[first_key].keys()
    with open(csvfile, mode="w", newline="") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(state.values())


def append_to_log(logfile: str, entry):
    print(entry.values())
    headers = entry.keys()
    with open(logfile, mode="a", newline="") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerow(entry.values())

    #    if Path(logfile).is_file():
    #        with open(logfile, mode="a", newline="") as f:
    #            writer = csv.DictWriter(f, headers)
    #            writer.writeheader()
    #            writer.writerows(entry.values())
    #    else:
    #        # Doesn't exits, create
    #        first_key = next(iter(entry))
    #        headers = state[first_key].keys()
    #        pass
    #        with open(logfile, mode="a", newline="") as f:
    #            writer = csv.DictWriter(f, headers)
    #            writer.writeheader()
    #            writer.writerows(entry.values())
    #    pass


def update_state(message):
    message_type = message["MessageType"]

    if message_type == "PositionReport":
        # Boat position report
        boat_state = parsers.parse_boat_state(message)
        mmsi = boat_state["mmsi"]
        time = boat_state["time"]
        if mmsi not in state["boats"] or time - state["boats"][mmsi][
            "time"
        ] >= timedelta(seconds=config.update_interval):
            append_to_log(
                config.boats_log_file, parsers.format_position_report(message)
            )
            state["boats"][mmsi] = boat_state
            save_state(config.boats_state_file, state["boats"])
    elif message_type == "StandardSearchAndRescueAircraftReport":
        # Aircraft position report
        aircraft_state = parsers.parse_boat_state(message)
        mmsi = aircraft_state["mmsi"]
        time = aircraft_state["time"]
        if mmsi not in state["planes"] or time - state["planes"][mmsi][
            "time"
        ] >= timedelta(seconds=config.update_interval):
            append_to_log(
                config.aircrafts_log_file, parsers.format_sar_aircraft_report(message)
            )
            state["planes"][mmsi] = aircraft_state
            save_state("planes.csv", state["planes"])
    else:
        logging.error(f"Unknown message type {message_type}")
    # print(json.dumps(message, indent=2))


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
            update_state(message)


def main():
    asyncio.run(connect_ais_stream())


if __name__ == "__main__":
    main()
