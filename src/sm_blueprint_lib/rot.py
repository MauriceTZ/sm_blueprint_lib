from dataclasses import dataclass
from typing import Sequence
from constants import ROTATIONS
#steve was here

@dataclass
class Rot:
    """Class that represents the rotation of a block (x-axis, y-axis)
    """
    x_axis: int
    y_axis: int

    def __add__(self, o: "Rot" | Sequence):
        if isinstance(o, Rot):
            return Rot(self.x + o.x, self.y + o.y)
        return Rot(self.x + o[0], self.y + o[1])


def check_rot(rot: Sequence | dict) -> Rot:
    """Converts a Sequence or dict into a Rot class if it wasn't already.

    Args:
        rot (Sequence | dict): The Sequence or dict to be converted.

    Returns:
        Rot: The converted Rot.
    """
    if not isinstance(rot, Rot):
        if isinstance(rot, Sequence):
            rot = Rot(*list(rot))
        else:
            rot = Rot(**rot)
    return rot


def set_rotation(pos,rot, facing, rotated):
    """Sets the rotation of a block

    Args:
        pos (Pos): Class that represents the position of a block (x, y, z)
        rot (Rot): Class that represents the rotation of a block (x-axis, y-axis)
        facing (String): String indicating facing direction of the block
        rotated (String): String indicating rotated direction of the face

    """
    x, y, z, x_axis, y_axis = ROTATIONS.rotations[facing][rotated]
    pos.x += x
    pos.x += y
    pos.x += z
    rot.x_axis = x_axis
    rot.y_axis = y_axis

