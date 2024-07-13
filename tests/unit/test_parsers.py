import json
import os
import sys
from utils import parsers


def test_aircraft_parser():
    with open("tests/data/plane.json", "r") as f:
        j = json.load(f)
        resp = parsers.parse_sar_aircraft_report(j)
        assert resp["mmsi"] == 111232535
        assert resp["ship_name"] == "COASTGUARD          "
        assert resp["lat"] == 50.94049166666667
        assert resp["lon"] == 0.9656316666666667
        assert resp["altitude"] == 83
        assert resp["cog"] == 303.4
        assert resp["assigned_mode"] == False


def test_boat_parser():
    with open("tests/data/boat.json", "r") as f:
        j = json.load(f)
        resp = parsers.parse_position_report(j)
        assert resp["mmsi"] == 226044000
        assert resp["ship_name"] == "ADARA               "
        assert resp["lat"] == 51.062551666666664
        assert resp["lon"] == 1.8275516666666667
        assert resp["cog"] == 343
