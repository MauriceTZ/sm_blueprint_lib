from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *


@dataclass
class Wheel(BasePart):
    """Class that represents a Wheel.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wheel)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class BigWheel(BasePart):
    """Class that represents a Big Wheel.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Big_Wheel)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 5, 2)

@dataclass
class ConcaveWedge(BasePart):
    """Class that represents a Concave Wedge.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Concave_Wedge)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LicensePlate(BasePart):
    """Class that represents a License Plate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.License_Plate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class MetallicTubeStraight(BasePart):
    """Class that represents a Metallic Tube Straight.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metallic_Tube_Straight)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class MetallicTubeBend(BasePart):
    """Class that represents a Metallic Tube Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metallic_Tube_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 2)

@dataclass
class RoundedFrameCorner(BasePart):
    """Class that represents a Rounded Frame Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Rounded_Frame_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)