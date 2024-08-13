import pytest
import alert
from unittest.mock import patch, Mock
import pandas as pd
from dtypes import Region, AlertsStatus, BoatStatus


def mock_boats_snapshot_df():
    boats_snapshot_df = pd.DataFrame(
        {"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]}
    )
    return boats_snapshot_df


def mock_aircrafts_snapshot_df():
    aircrafts_snapshot_df: pd.DataFrame = pd.DataFrame(
        {"mmsi": [123, 456], "lat": [51.5, 51.328], "lon": [0.0, 1.421]}
    )
    return aircrafts_snapshot_df


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
            },
            456: {
                "mmsi": 456,
                "name": "Boat B",
                "in_regions": [],
                "online": True,
                "home": None,
            },
        },
        "aircrafts": {},
    }
    return status


# @patch("alert.aircrafts_snapshot_df", mock_aircrafts_snapshot_df())
@patch("alert.boats_snapshot_df", mock_boats_snapshot_df())
@patch("alert.status", mock_status())
@patch("config.regions", mock_regions())
def test_updating_boat_region():
    # Boat 123 not in port region, boat 456 is
    alert.dispatch_message = Mock()
    alert.update_regions()

    # Assert boat entered port (region wasn't in "in_regions")
    assert "port" in alert.status["boats"][456]["in_regions"]
    assert alert.dispatch_message.called
    alert.dispatch_message.assert_called_with("Boat Boat B entered port")

    # boat 456 is in port, place outside and check it left the region
    alert.boats_snapshot_df.loc[
        alert.boats_snapshot_df["mmsi"] == 456, ["lat", "lon"]
    ] = [51.0, 0.0]
    alert.update_regions()
    alert.dispatch_message.assert_called_with("Boat Boat B left port")

    # check that when not changed it doesn't call the dispatch_message
    alert.update_regions()
    alert.dispatch_message.assert_not_called


@pytest.mark.skip(reason="Will send a message to discord")
def test_post_to_discord():
    alert.dispatch_message("Hi")


@patch("alert.aircrafts_snapshot_df", pd.DataFrame())
@patch("alert.status", {"monitor": False, "boats": {}, "aircrafts": {}})
@patch("alert.dispatch_message", Mock())
def test_aircraft_triggers_alert_flag():

    # not monitoring
    alert.set_monitor()
    alert.dispatch_message.assert_not_called()  # pyright: ignore[reportFunctionMemberAccess]
    assert not alert.status["monitor"]

    # aircrafts present
    alert.aircrafts_snapshot_df = mock_aircrafts_snapshot_df()
    alert.set_monitor()
    print(alert.status)
    assert alert.status["monitor"]
    alert.dispatch_message.assert_called_with(  # pyright: ignore[reportFunctionMemberAccess]
        "Aircraft pesent in secene, enabling monitoring"
    )

    # aircrafts gone
    alert.aircrafts_snapshot_df = pd.DataFrame()
    alert.set_monitor()
    assert not alert.status["monitor"]
    alert.dispatch_message.assert_called_with(  # pyright: ignore[reportFunctionMemberAccess]
        "Disabling monitoring"
    )

    # no change => no message
    alert.set_monitor()
    assert not alert.status["monitor"]
    assert (
        alert.dispatch_message.call_count == 2
    )  # pyright: ignore[reportFunctionMemberAccess]


def test_boat_outside_home_triggers_alert_flag():
    assert False
