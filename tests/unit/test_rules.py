from simpleeval import simple_eval
from alert import rules


def test_boat_speeding():

    config_rule = {
        "name": "Test Boat Moving",
        "enable": "speed>10",
        "disable": "speed<5",
    }
    alert_rule = rules.AlertRule(**config_rule)
    assert not alert_rule.raised

    # Alert raised
    names = {"speed": 50}
    alert_rule.parse_boat_rules(names)
    assert alert_rule.raised

    # Alert unchanged
    names = {"speed": 7.5}
    alert_rule.parse_boat_rules(names)
    assert alert_rule.raised

    # Alert disabled
    names = {"speed": 4}
    alert_rule.parse_boat_rules(names)
    assert not alert_rule.raised
