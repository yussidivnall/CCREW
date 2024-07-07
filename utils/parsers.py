from datetime import datetime, timedelta
import pandas as pd

from dtypes import BoatPosition, AircraftPosition


# def fix_time(time):
#     # The Date format is non standard,
#     # python expects 6 digits in microseconds
#     # AIS gives 9
#     time = time[0:26] + " " + time[-9:]
#     time = time.replace(" ", "T", 1)
#     ret = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f %z %Z")
#     return ret
#
#
# def parse_boat_state(message):
#     boat = {
#         "mmsi": message["MetaData"]["MMSI"],
#         "name": message["MetaData"]["ShipName"],
#         "lon": message["MetaData"]["longitude"],
#         "lat": message["MetaData"]["latitude"],
#         "time": fix_time(message["MetaData"]["time_utc"]),
#         # cog, etc
#     }
#     return boat
#
#
# def parse_aircraft_state(message):
#     plane = {
#         "mmsi": message["MetaData"]["MMSI"],
#         "name": message["MetaData"]["ShipName"],
#         "lon": message["MetaData"]["longitude"],
#         "lat": message["MetaData"]["latitude"],
#         "time": fix_time(message["MetaData"]["time_utc"]),
#         # cog, altitude , etc
#     }
#     return plane


def parse_position_report(msg) -> BoatPosition:
    ret: BoatPosition = {
        "server_timestamp": datetime.now(),
        "time_utc": msg["MetaData"][
            "time_utc"
        ],  # Should come from AIS Stream but bad format, 9 microseconds
        "mmsi": msg["MetaData"]["MMSI"],
        "ship_name": msg["MetaData"]["ShipName"],
        "cog": msg["Message"]["PositionReport"]["Cog"],
        "lat": msg["Message"]["PositionReport"]["Latitude"],
        "lon": msg["Message"]["PositionReport"]["Longitude"],
        "msg_id": msg["Message"]["PositionReport"]["MessageID"],
        "nav_status": msg["Message"]["PositionReport"]["NavigationalStatus"],
        "pos_accuracy": msg["Message"]["PositionReport"]["PositionAccuracy"],
        "raim": msg["Message"]["PositionReport"]["Raim"],
        "rate_of_turn": msg["Message"]["PositionReport"]["RateOfTurn"],
        "repeat_indicator": msg["Message"]["PositionReport"]["RepeatIndicator"],
        "sog": msg["Message"]["PositionReport"]["Sog"],
        "spare": msg["Message"]["PositionReport"]["Spare"],
        "special_manoeuvre_indicator": msg["Message"]["PositionReport"][
            "SpecialManoeuvreIndicator"
        ],
        "time_stamp": msg["Message"]["PositionReport"]["Timestamp"],
        "true_heading": msg["Message"]["PositionReport"]["TrueHeading"],
        "user_id": msg["Message"]["PositionReport"]["UserID"],
        "valid": msg["Message"]["PositionReport"]["Valid"],
    }
    return ret


def parse_sar_aircraft_report(msg) -> AircraftPosition:
    ret: AircraftPosition = {
        "server_timestamp": datetime.now(),
        "time_utc": msg["MetaData"][
            "time_utc"
        ],  # Should come from AIS Stream but bad format
        "mmsi": msg["MetaData"]["MMSI"],
        "ship_name": msg["MetaData"]["ShipName"],
        "alt_from_baro": msg["Message"]["StandardSearchAndRescueAircraftReport"][
            "AltFromBaro"
        ],
        "altitude": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Altitude"],
        "assigned_mode": msg["Message"]["StandardSearchAndRescueAircraftReport"][
            "AssignedMode"
        ],
        "cog": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Cog"],
        "communication_state": msg["Message"]["StandardSearchAndRescueAircraftReport"][
            "CommunicationState"
        ],
        "communication_state_is_itdma": msg["Message"][
            "StandardSearchAndRescueAircraftReport"
        ]["CommunicationStateIsItdma"],
        "dte": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Dte"],
        "lat": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Latitude"],
        "lon": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Longitude"],
        "msg_id": msg["Message"]["StandardSearchAndRescueAircraftReport"]["MessageID"],
        "pos_accuracy": msg["Message"]["StandardSearchAndRescueAircraftReport"][
            "PositionAccuracy"
        ],
        "raim": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Raim"],
        "repeat_indicator": msg["Message"]["StandardSearchAndRescueAircraftReport"][
            "RepeatIndicator"
        ],
        "sog": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Sog"],
        "spare1": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Spare1"],
        "spare2": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Spare2"],
        "time_stamp": msg["Message"]["StandardSearchAndRescueAircraftReport"][
            "Timestamp"
        ],
        "user_id": msg["Message"]["StandardSearchAndRescueAircraftReport"]["UserID"],
        "valid": msg["Message"]["StandardSearchAndRescueAircraftReport"]["Valid"],
    }
    return ret
