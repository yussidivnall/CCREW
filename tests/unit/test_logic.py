import json
from utils import parsers
from utils.logic import lists_to_pairs, boat_in_region
from dtypes import BoatPosition
from alert.status import Region


def test_lists_to_pairs():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expected_pairs = [(1, 4), (2, 5), (3, 6)]
    recieved = lists_to_pairs(a, b)
    assert expected_pairs == recieved


def test_boat_in_region():
    region: Region = {
        "lat": [51.333369, 51.329196, 51.327212, 51.330014],
        "lon": [1.422637, 1.425542, 1.420174, 1.416394],
        "name": "Port",
    }

    with open("tests/data/boat.json", "r") as f:
        j = json.load(f)
        resp = parsers.parse_position_report(j)
        boat_pos: BoatPosition = resp
        print(boat_pos)
        assert not boat_in_region(boat_pos, region)
        boat_pos["lat"] = 51.3294
        boat_pos["lon"] = 1.42153
        assert boat_in_region(boat_pos, region)
