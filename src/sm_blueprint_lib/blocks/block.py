from dataclasses import dataclass, field

from ..bases.parts.baseboundablepart import BaseBoundablePart
from ..constants import SHAPEID, BLOCKS, BLOCK_COLOR



@dataclass
class Block(BaseBoundablePart):
    """Class that represents a Block.
    """


    shapeId: str = field(kw_only=True, default=SHAPEID.Barrier_Block)




