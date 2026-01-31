from dataclasses import dataclass, field

from .basepart import BasePart
from ...bounds import Bounds


@dataclass
class BaseBoundablePart(BasePart):
    """Base class for all Boundable parts (those that are draggable)
    """
    bounds: Bounds

    def __post_init__(self):
        if not isinstance(self.bounds, Bounds):
            try:
                self.bounds = Bounds(**self.bounds)
            except TypeError:
                self.bounds = Bounds(
                    self.bounds[0], self.bounds[1], self.bounds[2])
        super().__post_init__()
