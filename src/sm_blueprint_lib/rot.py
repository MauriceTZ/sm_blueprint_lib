from dataclasses import dataclass
from typing import Sequence
from .constants import ROTATIONS
from .pos import Pos
from dataclasses import dataclass
from typing import Sequence

@dataclass
class Xaxis:
    """Class that represents the xaxis of a block (y-axis)
    """

    xaxis: int

    def __add__(self, o: "Xaxis" | Sequence):
        if isinstance(o, Xaxis):
            return Xaxis(self.xaxis + o.xaxis)
        return Xaxis(self.xaxis + o[0])


def check_xaxis(xaxis: Sequence | dict) -> Xaxis:
    """Converts a Sequence or dict into a xaxis class if it wasn't already.

    Args:
        xaxis (Sequence | dict): The Sequence or dict to be converted.

    Returns:
        Xaxis: The converted Xaxis.
    """
    if not isinstance(xaxis, Xaxis):
        if isinstance(xaxis, Sequence):
            xaxis = Xaxis(*list(xaxis))
        else:
            xaxis = Xaxis(**xaxis)
    return xaxis


@dataclass
class Zaxis:
    """Class that represents the zaxis of a block (y-axis)
    """

    zaxis: int

    def __add__(self, o: "Zaxis" | Sequence):
        if isinstance(o, Zaxis):
            return Zaxis(self.zaxis + o.zaxis)
        return Zaxis(self.zaxis + o[0])


def check_zaxis(zaxis: Sequence | dict) -> Zaxis:
    """Converts a Sequence or dict into a zaxis class if it wasn't already.

    Args:
        zaxis (Sequence | dict): The Sequence or dict to be converted.

    Returns:
        Zaxis: The converted Zaxis.
    """
    if not isinstance(zaxis, Zaxis):
        if isinstance(zaxis, Sequence):
            zaxis = Zaxis(*list(zaxis))
        else:
            zaxis = Zaxis(**zaxis)
    return zaxis


def set_rotation(pos, xaxis, zaxis, facing, rotated):
    """Sets the rotation of a block.

    Args:
        pos (Pos): Class that represents the position of a block (x, y, z).
        rot (Rot): Class that represents the rotation of a block (x-axis, y-axis).
        facing (String): String indicating facing direction of the block.
        rotated (String): String indicating rotated direction of the face.

    """
    x, y, z, x_axis, z_axis = ROTATIONS.rotations[facing][rotated]
    pos.x += x
    pos.y += y
    pos.z += z
    xaxis.xaxis = x_axis
    zaxis.zaxis = z_axis


def rotate(gates: list, center: Pos):
    """Rotates a list of gate

    Args:
        gates (list): list of gates to rotate.
        center (Pos): Center point to rotate gates.

    """
    for gate in gates:
        temp = gate.pos
        # todo everything :)
    pass

