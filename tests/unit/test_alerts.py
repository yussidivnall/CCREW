from unittest.mock import Mock, patch

import pandas as pd
from pandas.core.api import DataFrame
import pytest

from alert import alert
from dtypes import AlertsStatus, BoatStatus, Region


def mock_boats_df():
    ret = pd.DataFrame({"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]})
    return ret


def mock_boats_snapshot_df():
    boats_snapshot_df = pd.DataFrame(
        {"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]}
    )
    return boats_snapshot_df


def mock_aircraft_snapshot_df():
    aircraft_snapshot_df: pd.DataFrame = pd.DataFrame(
        {"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]}
    )
    return aircraft_snapshot_df


def mock_regions():
    regions = {
        "port": {
            "lat": [51.333369, 51.329196, 51.327212, 51.330014],
            "lon": [1.422637, 1.425542, 1.420174, 1.416394],
            "name": "Ramsgate port",
        }
    }
    return regions


def mock_dispatch(message):
    print(message)


def mock_status():
    status: AlertsStatus = {
        "monitor": False,
        "boats": {
            123: {
                "mmsi": 123,
                "name": "Boat A",
                "in_regions": [],
                "online": True,
                "home": "port",
                "color": "red",
            },
            456: {
                "mmsi": 456,
                "name": "Boat B",
                "in_regions": [],
                "online": True,
                "home": None,
                "color": "blue",
            },
        },
        "aircraft": {},
    }
    return status


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
