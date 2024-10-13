from dataclasses import dataclass, field
import logging
from typing import TypedDict, Dict, Optional
from datetime import datetime
from typing_extensions import NotRequired
from alert import rules


@dataclass
class BoatPosition:
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


@dataclass
class AircraftPosition:
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


@dataclass
class BoatStatus:
    # Boats are indexed by mmsi+name,
    mmsi: int
    name: str
    color: str
    online: bool = False
    lat: float | None = None
    lon: float | None = None
    speed: float | None = None
    in_regions: list[str] | None = None
    home: str | None = None
    alerts: list[rules.AlertRule] | None = None


@dataclass
class AircraftStatus:
    mmsi: int
    name: str
    lat: float
    lon: float
    speed: float
    in_regions: list[str]
    online: bool


@dataclass
class Status:
    monitor: bool = False
    boats: list[BoatStatus] = field(default_factory=list)
    aircraft: list[AircraftStatus] = field(default_factory=list)

    def get_boat(self, mmsi, ship_name):
        """Returns a tracked boat"""
        for boat in self.boats:
            if boat.mmsi == mmsi and boat.name == ship_name:
                return boat
        logging.warning(f"No status for boat {mmsi} - {ship_name}")

    def __init__(self, monitor=False, boats=[], aircraft=[]):
        self.monitor = monitor
        self.boats = boats
        self.aircraft = aircraft


@dataclass
class Region:
    lat: list[float]
    lon: list[float]
    name: str
