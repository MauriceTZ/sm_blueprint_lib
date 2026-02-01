from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *


@dataclass
class GrassContainer(BasePart):
    """Class that represents a Grass Container.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Grass_Container)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 1, 4)

@dataclass
class PottedPlant(BasePart):
    """Class that represents a Potted Plant.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Potted_Plant)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 4, 2)

@dataclass
class SmallPottedPlant(BasePart):
    """Class that represents a Small Potted Plant.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Potted_Plant)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class PottedVinePlant(BasePart):
    """Class that represents a Potted Vine Plant.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Potted_Vine_Plant)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 6, 2)

@dataclass
class BigPot(BasePart):
    """Class that represents a Big Pot.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Big_Pot)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class PottedSeedPlant(BasePart):
    """Class that represents a Potted Seed Plant.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Potted_Seed_Plant)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 2)

@dataclass
class PottedBloomingCactus(BasePart):
    """Class that represents a Potted Blooming Cactus.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Potted_Blooming_Cactus)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class PottedCactus(BasePart):
    """Class that represents a Potted Cactus.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Potted_Cactus)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 3, 1)

@dataclass
class PottedBlueFlower(BasePart):
    """Class that represents a Potted Blue Flower.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Potted_Blue_Flower)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)