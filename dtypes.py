from typing import TypedDict, Dict, Optional
from datetime import datetime


class BoatPosition(TypedDict):
    server_timestamp: datetime
    time_utc: str
    mmsi: int
    ship_name: str
    cog: float
    lat: float
    lon: float
    msg_id: int
    nav_status: int
    pos_accuracy: bool
    raim: bool
    rate_of_turn: int
    repeat_indicator: int
    sog: float
    spare: int
    special_manoeuvre_indicator: int
    time_stamp: int
    true_heading: int
    user_id: int
    valid: bool


class AircraftPosition(TypedDict):
    server_timestamp: datetime
    time_utc: str
    mmsi: int
    ship_name: str
    alt_from_baro: bool
    altitude: int
    assigned_mode: bool
    cog: float
    communication_state: int
    communication_state_is_itdma: bool
    dte: bool
    lat: float
    lon: float
    msg_id: int
    pos_accuracy: bool
    raim: bool
    repeat_indicator: int
    sog: int
    spare1: int
    spare2: int
    time_stamp: int
    user_id: int
    valid: bool


class BoatStatus(TypedDict):
    mmsi: int
    name: str
    color: str
    in_regions: list[str]
    online: bool
    home: Optional[str]


class AircraftStatus(TypedDict):
    mmsi: int
    name: str
    in_regions: list[str]
    online: bool


class AlertsStatus(TypedDict):
    monitor: bool
    boats: Dict[int, BoatStatus]
    aircraft: Dict[int, AircraftStatus]


class Region(TypedDict):
    lat: list[float]
    lon: list[float]
    name: str
