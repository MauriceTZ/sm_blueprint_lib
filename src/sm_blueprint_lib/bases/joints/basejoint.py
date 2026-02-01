from dataclasses import dataclass, field

from glm import vec3

from ...constants import SHAPEID
from ...pos import *


@dataclass
class BaseJoint:
    """Base class for joint objects (bearings, pistons, suspensions, etc)
    that join two bodies together.
    """
    childA: int
    childB: int
    color: str
    id: int
    posA: Pos
    posB: Pos
    shapeId: str
    xaxisA: int
    xaxisB: int
    zaxisA: int
    zaxisB: int

    def __post_init__(self):
        self.posA = check_pos(self.posA)
        self.posB = check_pos(self.posB)
        self._box = vec3(1, 1, 1)
        self._offset = vec3(0, 0, 0)

    def __init_subclass__(cls):
        super().__init_subclass__()
        try:
            SHAPEID.JOINT_TO_CLASS[cls.shapeId.default] = cls
        except AttributeError:
            pass
