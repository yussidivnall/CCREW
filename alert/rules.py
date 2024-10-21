from dataclasses import dataclass
import logging
from simpleeval import simple_eval


@dataclass
class AlertRule:
    name: str
    enable: str
    disable: str
    raised: bool = False

    def evaluate(self, names):
        print(f"evaluate with names:{names}")
        if "speed" not in names or names["speed"] is None:
            logging.warning("cannot evaluate missing boat speed")
            return
        if simple_eval(self.enable, names=names):
            self.raised = True
        elif simple_eval(self.disable, names=names):
            self.raised = False

    def __init__(self, name, enable, disable):
        self.name = name
        self.enable = enable
        self.disable = disable
