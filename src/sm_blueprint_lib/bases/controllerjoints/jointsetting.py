from dataclasses import dataclass

from .targetangle import *


@dataclass
class ControllerBearingJointSetting:
    """Settings from a single row of a game controller of type Bearing."""
    endAngle: int
    frames: list[TargetAngle]
    id: int
    index: int
    reverse: bool
    startAngle: int

    def __post_init__(self):
        if self.frames:
            self.frames = [TargetAngle(**ta)
                           if not isinstance(ta, TargetAngle) else
                           ta
                           for ta in self.frames]

@dataclass
class ControllerPistonControllerSetting:
    """Settings from a single row of a game controller of type Piston."""
    frames: list[Setting]
    id: int
    index: int

    def __post_init__(self):
        if self.frames:
            self.frames = [Setting(**c)
                           if not isinstance(c, Setting) else
                           c
                           for c in self.frames]