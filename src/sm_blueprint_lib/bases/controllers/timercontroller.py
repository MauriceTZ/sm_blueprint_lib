from dataclasses import dataclass, field

from .baselogiccontroller import BaseLogicController


@dataclass
class TimerController(BaseLogicController):
    """Timer's Controller
    """
    seconds: int
    ticks: int

    def __post_init__(self):
        assert 59 >= self.seconds >= 0, f"Timer seconds value invalid: {self.seconds}"
        assert 40 >= self.ticks >= 0, f"Timer ticks value invalid: {self.ticks}"
        super().__post_init__()
