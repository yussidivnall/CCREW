from dataclasses import dataclass
from simpleeval import simple_eval


@dataclass
class AlertRule:
    name: str
    enable: str
    disable: str
    raised: bool = False

    def parse_boat_rules(self, names):
        if simple_eval(self.enable, names=names):
            self.raised = True
        elif simple_eval(self.disable, names=names):
            self.raised = False

    def __init__(self, name, enable, disable):
        self.name = name
        self.enable = enable
        self.disable = disable
