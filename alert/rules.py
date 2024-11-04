from dataclasses import dataclass
import logging
from simpleeval import simple_eval


@dataclass
class AlertRule:
    name: str
    enable: str  # condition to enable
    disable: str  # condition to disable
    message: str
    raised: bool = False

    def evaluate(self, names):
        logging.debug(f"Evaluating rule {self.name} with {names}")
        if "speed" not in names or names["speed"] is None:
            logging.debug("cannot evaluate missing boat speed")
            return
        if simple_eval(self.enable, names=names):
            msg = self.get_message(names)
            logging.info(f"Enabling alert rule: {self.name}, - {msg}")
            self.raised = True
        elif simple_eval(self.disable, names=names):
            logging.info(f"Disabling alert for rule: {self.name}")
            self.raised = False

    def get_message(self, names):
        ret = self.message.format(**names)
        return ret

    def __init__(self, name, enable, disable, message=None):
        self.name = name
        self.enable = enable
        self.disable = disable

        if not message:
            self.message = name
        else:
            self.message = message
