from dataclasses import dataclass
import logging
from simpleeval import simple_eval


@dataclass
class AlertRule:
    name: str
    enable: str  # condition to enable
    disable: str  # condition to disable
    raised: bool = False

    def evaluate(self, names):
        logging.debug(f"Evaluating rule {self.name} with {names}")
        if "speed" not in names or names["speed"] is None:
            logging.debug("cannot evaluate missing boat speed")
            return
        if simple_eval(self.enable, names=names):
            logging.info(f"Enabling alert for rule: {self.name}")
            self.raised = True
        elif simple_eval(self.disable, names=names):
            logging.info(f"Disabling alert for rule: {self.name}")
            self.raised = False

    def __init__(self, name, enable, disable):
        self.name = name
        self.enable = enable
        self.disable = disable
