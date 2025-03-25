from .constants import ROTATION
from .pos import Pos
from .bases.parts.basepart import BasePart


def set_rotation(part: BasePart, facing: ROTATION.FACING, rotated: ROTATION.ROTATED):
    """Sets the rotation of a Part.

    Args:
        part (BasePart): The Part that will be rotated. Note that it gets modified so don't pass the same part twice.
        facing (ROTATION.FACING): String indicating facing direction of the Part.
        rotated (ROTATION.ROTATED): String indicating rotated direction of the face.
    """
    x, y, z, x_axis, z_axis = ROTATION.ROTATION_TABLE[facing][rotated]
    part.pos.x += x
    part.pos.y += y
    part.pos.z += z
    part.xaxis = x_axis
    part.zaxis = z_axis


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
