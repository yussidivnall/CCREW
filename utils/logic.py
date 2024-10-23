from typing import List, Tuple
from dtypes import BoatPosition
from alert.status import Region

from shapely import Point, Polygon


def lists_to_pairs(list_a, list_b) -> List[Tuple[float, float]]:
    """Converts from lat:[], lon:[] to [(lat, lon), (lat, lon),...]
    list of tuples needed for shapely
    """
    ret = [(list_a[i], list_b[i]) for i in range(0, len(list_a))]
    return ret


def point_in_region(point, region) -> bool:
    p = Point(point)
    r = Polygon(region)
    return r.contains(p)


def boat_in_region(boat: BoatPosition, region: Region) -> bool:
    """Checks if boat in region"""
    poly = Polygon(lists_to_pairs(region["lat"], region["lon"]))
    pt = Point(boat["lat"], boat["lon"])
    return poly.contains(pt)
