from dataclasses import asdict, dataclass, field
import logging
from dataclasses import dataclass
import logging
from .rules import AlertRule


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
    alerts: list[AlertRule] | None = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


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
    messages: list[str] = field(default_factory=list[str])

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
