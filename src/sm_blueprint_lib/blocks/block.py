from dataclasses import dataclass, field

from src.sm_blueprint_lib.bases.parts.baseboundablepart import BaseBoundablePart
from src.sm_blueprint_lib.constants import SHAPEID


@dataclass
class Block(BaseBoundablePart):
    """Class that represents a Barrier Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Barrier_Block)

@dataclass
class SpaceshipFloorBlock(BaseBoundablePart):
    """Class that represents a Spaceship Floor Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Spaceship_Floor_Block)