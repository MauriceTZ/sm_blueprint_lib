from dataclasses import dataclass, field

from ..bases.parts.baseboundablepart import BaseBoundablePart
from ..constants import COLOR, SHAPEID
from ..pos import Pos

@dataclass
class Block(BaseBoundablePart):
    """Class that represents a Barrier Block.
    """
    shapeId: field(kw_only=True, default=SHAPEID.Barrier_Block)
    color: field(kw_only=True, default=COLOR.Barrier_Block)
