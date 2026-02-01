from dataclasses import dataclass, field


@dataclass
class BaseSteering:
    """Base class for Steering objects.
    """
    id: int
    leftAngleLimit: float
    leftAngleSpeed: float
    rightAngleLimit: float
    rightAngleSpeed: float
    unlocked: bool
