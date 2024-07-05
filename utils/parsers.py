from datetime import datetime


def fix_time(time):
    # The Date format is non standard,
    # python expects 6 digits in microseconds
    # AIS gives 9
    time = time[0:26] + " " + time[-9:]
    time = time.replace(" ", "T", 1)
    ret = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f %z %Z")
    return ret


def parse_boat_state(message):
    boat = {
        "mmsi": message["MetaData"]["MMSI"],
        "name": message["MetaData"]["ShipName"],
        "lon": message["MetaData"]["longitude"],
        "lat": message["MetaData"]["latitude"],
        "time": fix_time(message["MetaData"]["time_utc"]),
        # cog, etc
    }
    return boat


def parse_aircraft_state(message):
    plane = {
        "mmsi": message["MetaData"]["MMSI"],
        "name": message["MetaData"]["ShipName"],
        "lon": message["MetaData"]["longitude"],
        "lat": message["MetaData"]["latitude"],
        "time": fix_time(message["MetaData"]["time_utc"]),
        # cog, altitude , etc
    }
    return plane


def format_position_report(record):
    ret = {
        "server_timestamp": datetime.now(),
        "time_utc": record["MetaData"][
            "time_utc"
        ],  # Should come from AIS Stream but bad format, 9 microseconds
        "mmsi": record["MetaData"]["MMSI"],
        "ship_name": record["MetaData"]["ShipName"],
        "cog": record["Message"]["PositionReport"]["Cog"],
        "lat": record["Message"]["PositionReport"]["Latitude"],
        "lon": record["Message"]["PositionReport"]["Longitude"],
        "msg_id": record["Message"]["PositionReport"]["MessageID"],
        "nav_status": record["Message"]["PositionReport"]["NavigationalStatus"],
        "pos_accuracy": record["Message"]["PositionReport"]["PositionAccuracy"],
        "raim": record["Message"]["PositionReport"]["Raim"],
        "rate_of_turn": record["Message"]["PositionReport"]["RateOfTurn"],
        "repeat_indicator": record["Message"]["PositionReport"]["RepeatIndicator"],
        "sog": record["Message"]["PositionReport"]["Sog"],
        "spare": record["Message"]["PositionReport"]["Spare"],
        "special_manoeuvre_indicator": record["Message"]["PositionReport"][
            "SpecialManoeuvreIndicator"
        ],
        "time_stamp": record["Message"]["PositionReport"]["Timestamp"],
        "true_heading": record["Message"]["PositionReport"]["TrueHeading"],
        "user_id": record["Message"]["PositionReport"]["UserID"],
        "valid": record["Message"]["PositionReport"]["Valid"],
    }
    return ret


def format_sar_aircraft_report(record):
    ret = {
        "server_timestamp": datetime.now(),
        "time_utc": record["MetaData"][
            "time_utc"
        ],  # Should come from AIS Stream but bad format
        "mmsi": record["MetaData"]["MMSI"],
        "ship_name": record["MetaData"]["ShipName"],
        "alt_from_baro": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "AltFromBaro"
        ],
        "altitude": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "Altitude"
        ],
        "assignment_mode": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "AssignedMode"
        ],
        "cog": record["Message"]["StandardSearchAndRescueAircraftReport"]["Cog"],
        "communication_state": record["Message"][
            "StandardSearchAndRescueAircraftReport"
        ]["CommunicationState"],
        "communication_stateIs_itdma": record["Message"][
            "StandardSearchAndRescueAircraftReport"
        ]["CommunicationStateIsItdma"],
        "dte": record["Message"]["StandardSearchAndRescueAircraftReport"]["Dte"],
        "lat": record["Message"]["StandardSearchAndRescueAircraftReport"]["Latitude"],
        "lon": record["Message"]["StandardSearchAndRescueAircraftReport"]["Longitude"],
        "msg_id": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "MessageID"
        ],
        "pos_accuracy": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "PositionAccuracy"
        ],
        "raim": record["Message"]["StandardSearchAndRescueAircraftReport"]["Raim"],
        "repeat_indicator": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "RepeatIndicator"
        ],
        "sog": record["Message"]["StandardSearchAndRescueAircraftReport"]["Sog"],
        "spare1": record["Message"]["StandardSearchAndRescueAircraftReport"]["Spare1"],
        "spare2": record["Message"]["StandardSearchAndRescueAircraftReport"]["Spare2"],
        "time_stamp": record["Message"]["StandardSearchAndRescueAircraftReport"][
            "Timestamp"
        ],
        "user_id": record["Message"]["StandardSearchAndRescueAircraftReport"]["UserID"],
        "valid": record["Message"]["StandardSearchAndRescueAircraftReport"]["Valid"],
    }
    return ret
