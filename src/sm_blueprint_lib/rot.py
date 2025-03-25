from dataclasses import dataclass
from typing import Sequence


@dataclass
class Rot:
    """Class that represents the rotation of a block (x-axis, y-axis)
    """
    x: int
    y: int

    def __add__(self, o: "Rot" | Sequence):
        if isinstance(o, Rot):
            return Rot(self.x + o.x, self.y + o.y)
        return Rot(self.x + o[0], self.y + o[1])


def check_pos(rot: Sequence | dict) -> Rot:
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
