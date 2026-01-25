from dataclasses import dataclass, field
from typing import Optional
from glm import vec3

from ...constants import ROTATION, SHAPEID, AXIS, BLOCK_COLOR
from ...pos import Pos
from ...id import ID
from .basepart import BasePart


@dataclass
class BaseNormalPart(BasePart):
    """Base class for all in-game normal parts
    """

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)
        self._offset = vec3(0, 0, 0)