from dataclasses import dataclass, field

from .bases.parts.basepart import BasePart
from .constants import SHAPEID


@dataclass
class Body:
    """Class that represents a Body inside a Blueprint, each Joint defines a new Body.
    """
    childs: list[BasePart] = field(default_factory=list)

    def __post_init__(self):
        self.childs = [SHAPEID.SHAPEID_TO_CLASS[child["shapeId"]](**child)
                       for child in self.childs]
