import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from pandas.core.api import DataFrame

from alert import alert, status, rules
from alert.rules import AlertRule
from alert.status import BoatStatus, Status


@pytest.fixture
def reset_alert():
    alert.status = Status()
    alert.status.boats = []
    yield


def test_initialised_statuses(reset_alert):
    # Empty tracked boat list
    alert.config.tracked_boats = []
    alert.initialise_statuses()
    assert alert.status.boats == []

    # tracked boat list missing keys
    alert.config.tracked_boats = [{}]
    with pytest.raises(KeyError) as kerr:
        alert.initialise_statuses()
    assert kerr.match("^'mmsi'$")
    assert alert.status.boats == []

    alert.config.tracked_boats = [{"mmsi": 1234, "name": "Shmulik", "color": "red"}]
    alert.initialise_statuses()
    assert alert.status.boats == [
        BoatStatus(
            mmsi=1234,
            name="Shmulik",
            color="red",
            online=False,
            lat=None,
            lon=None,
            speed=None,
            in_regions=None,
            home=None,
            alerts=[],
        ),
    ]


def test_initialised_statuses_with_boat_empty_alert_rules(reset_alert):
    alert.config.tracked_boats = [
        {"mmsi": 1234, "name": "Shmulik", "color": "red", "alerts": []}
    ]
    alert.initialise_statuses()
    assert alert.status.boats == [
        BoatStatus(
            mmsi=1234,
            name="Shmulik",
            color="red",
            online=False,
            lat=None,
            lon=None,
            speed=None,
            in_regions=None,
            home=None,
            alerts=[],
        ),
    ]


def test_initialised_statuses_with_boat_alert_rules(reset_alert):
    alert.config.tracked_boats = [
        {
            "mmsi": 1234,
            "name": "Shmulik",
            "color": "red",
            "alerts": [
                {"name": "test_rule", "enable": "speed>10", "disable": "speed<3"}
            ],
        }
    ]
    alert.initialise_statuses()
    assert alert.status.boats == [
        BoatStatus(
            mmsi=1234,
            name="Shmulik",
            color="red",
            online=False,
            lat=None,
            lon=None,
            speed=None,
            in_regions=None,
            home=None,
            alerts=[AlertRule(name="test_rule", enable="speed>10", disable="speed<3")],
        ),
    ]


def test_update_statuses(reset_alert):
    alert.config.tracked_boats = [
        {
            "mmsi": 1234,
            "name": "Shmulik",
            "color": "red",
            "alerts": [
                {"name": "test_rule", "enable": "speed>10", "disable": "speed<3"}
            ],
        }
    ]

    alert.boats_snapshot_df = pd.DataFrame(
        {"mmsi": [1234], "ship_name": ["Shmulik     "], "sog": [11]}
    )

    alert.initialise_statuses()
    alert.update_statuses()
    assert alert.status.boats[0].speed == 11


def test_boat_speeding_sets_monitor(reset_alert):
    alert.config.tracked_boats = [
        {
            "mmsi": 1234,
            "name": "Shmulik",
            "color": "red",
            "alerts": [
                {"name": "test_rule", "enable": "speed>10", "disable": "speed<3"}
            ],
        }
    ]

    alert.boats_df = pd.DataFrame(
        {
            "server_timestamp": datetime.datetime.now(),
            "mmsi": [1234],
            "ship_name": ["Shmulik     "],
            "sog": [11],
            "lat": 51.006948333333334,
            "lon": 1.6026500000000001,
        }
    )

    alert.boats_snapshot_df = pd.DataFrame(
        {
            "server_timestamp": datetime.datetime.now(),
            "mmsi": [1234],
            "ship_name": ["Shmulik     "],
            "sog": [11],
        }
    )

    alert.aircraft_df = pd.DataFrame({"server_timestamp": [], "mmsi": []})

    alert.initialise_statuses()
    alert.update_statuses()
    alert.set_monitor()

    assert alert.status.monitor == True


# def mock_boats_df():
#     ret = pd.DataFrame({"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]})
#     return ret
#
#
# def mock_boats_snapshot_df():
#     boats_snapshot_df = pd.DataFrame(
#         {"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]}
#     )
#     return boats_snapshot_df
#
#
# def mock_aircraft_snapshot_df():
#     aircraft_snapshot_df: pd.DataFrame = pd.DataFrame(
#         {"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]}
#     )
#     return aircraft_snapshot_df
#
#
# def mock_regions():
#     regions = {
#         "port": {
#             "lat": [51.333369, 51.329196, 51.327212, 51.330014],
#             "lon": [1.422637, 1.425542, 1.420174, 1.416394],
#             "name": "Ramsgate port",
#         }
#     }
#     return regions
#
#
# def mock_dispatch(message):
#     print(message)
#
#
# def mock_status():
#     status: AlertsStatus = {
#         "monitor": False,
#         "boats": {
#             123: {
#                 "mmsi": 123,
#                 "name": "Boat A",
#                 "in_regions": [],
#                 "online": True,
#                 "home": "port",
#                 "color": "red",
#             },
#             456: {
#                 "mmsi": 456,
#                 "name": "Boat B",
#                 "in_regions": [],
#                 "online": True,
#                 "home": None,
#                 "color": "blue",
#             },
#         },
#         "aircraft": {},
#     }
#     return status
#
#
#
#
# Junk, superseded by
# @patch("alert.aircraft_snapshot_df", mock_aircraft_snapshot_df())
# @patch("alert.boats_snapshot_df", mock_boats_snapshot_df())
# @patch("alert.status", mock_status())
# @patch("config.regions", mock_regions())
# def test_updating_boat_region():
#     # Boat 123 not in port region, boat 456 is
#     alert.dispatch_message = Mock()
#     alert.update_regions()
#
#     # Assert boat entered port (region wasn't in "in_regions")
#     assert "port" in alert.status["boats"][456]["in_regions"]
#     assert alert.dispatch_message.called
#     alert.dispatch_message.assert_called_with("Boat Boat B entered port")
#
#     # boat 456 is in port, place outside and check it left the region
#     alert.boats_snapshot_df.loc[
#         alert.boats_snapshot_df["mmsi"] == 456, ["lat", "lon"]
#     ] = [51.0, 0.0]
#     alert.update_regions()
#     alert.dispatch_message.assert_called_with("Boat Boat B left port")
#
#     # check that when not changed it doesn't call the dispatch_message
#     alert.update_regions()
#     alert.dispatch_message.assert_not_called


@pytest.mark.skip(reason="Will send a message to discord")
def test_post_to_discord():
    alert.dispatch_message("Hi")


# @patch("alert.boats_df", mock_boats_df())
@patch("alert.aircraft_snapshot_df", pd.DataFrame())
@patch("alert.status", {"monitor": False, "boats": {}, "aircraft": {}})
@patch("alert.dispatch_message", Mock())
# @patch("alert.generate_map", Mock())
@patch("alert.dispatch_message", Mock())
@patch("alert.config.boats_log_file", "tests/data/boats.log.csv")
@pytest.mark.skip(reason="Broken as fuck")
def test_aircraft_triggers_alert_flag():

    # not monitoring
    alert.set_monitor()
    # alert.dispatch_message.assert_not_called()  # pyright: ignore[reportFunctionMemberAccess]
    assert not alert.status["monitor"]

    # aircraft present
    alert.aircraft_snapshot_df = mock_aircraft_snapshot_df()
    alert.set_monitor()
    print(alert.status)
    assert alert.status["monitor"]
    alert.dispatch_message.assert_called_with(  # pyright: ignore[reportFunctionMemberAccess]
        "Aircraft pesent in scene, enabling monitoring", "images/enabled.png"
    )

    # aircraft gone
    alert.aircraft_snapshot_df = pd.DataFrame()
    alert.set_monitor()
    assert not alert.status["monitor"]
    alert.dispatch_message.assert_called_with(  # pyright: ignore[reportFunctionMemberAccess]
        "Disabling monitoring"
    )

    # no change => no message
    alert.set_monitor()
    assert not alert.status["monitor"]
    # assert (
    #     alert.dispatch_message.call_count == 2
    # )  # pyright: ignore[reportFunctionMemberAccess]


# TODO
# def test_generate_map():
#     pass
#
# def test_boat_outside_home_triggers_alert_flag():
#     assert False


# @patch("alert.status", mock_status())
# @patch("alert.boats_snapshot_df", mock_boats_snapshot_df())
# def test_update_tracked_boats():
#     print(alert.boats_snapshot_df)
#     print(alert.status)
#     assert False
