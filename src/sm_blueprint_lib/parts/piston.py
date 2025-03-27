from dataclasses import dataclass, field

from ..bases.joints.pistonjoint import PistonJoint
from ..constants import SHAPEID


@dataclass
class Piston5(PistonJoint):
    """Class that represents a Piston 5 part.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston_5)
