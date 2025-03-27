from dataclasses import dataclass, field

from .basepart import BasePart
from ...bounds import Bounds


@dataclass
class BaseBoundablePart(BasePart):
    """Base class for all Boundable parts (those that are draggable)
    """
    bounds: Bounds = field(kw_only=True, default=(1,1,1))

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.bounds, Bounds):
            try:
                self.bounds = Bounds(**self.bounds)
            except TypeError:
                self.bounds = Bounds(
                    self.bounds[0], self.bounds[1], self.bounds[2])
