import numpy as np
from typing import Sequence
from numpy import ndarray, array
from ..utils import get_bits_required, connect, num_to_bit_list
from ..blueprint import Blueprint
from ..parts import LogicGate, Timer
from ..pos import *


def bitwise_alu(bp: Blueprint,
                bit_length: int,
                pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)
    arr = ndarray((bit_length, 4, 12), dtype=LogicGate)
    inputs = array([(LogicGate(pos + (x, 5, 0), "FF0000", "or"),
                     LogicGate(pos + (x, 6, 0), "FF0000", "or"))
                   for x in range(bit_length)], dtype=LogicGate)
    outputs = array([LogicGate(pos + (x, 0, 0), "0000FF", "or")
                     for x in range(bit_length)], dtype=LogicGate)
    arr[:, :, 0] = [(LogicGate(pos + (x, 1, 0), "0000FF", "and"),
                     LogicGate(pos + (x, 2, 0), "000000", "and"),
                     LogicGate(pos + (x, 3, 0), "FF0000", "and"),
                     LogicGate(pos + (x, 4, 0), "FF0000", "and"))
                    for x in range(bit_length)]
    arr[:, :, 1] = [(LogicGate(pos + (x, 1, 1), "0000FF", "and"),
                     LogicGate(pos + (x, 2, 1), "000000", "or"),
                     LogicGate(pos + (x, 3, 1), "FF0000", "and"),
                     LogicGate(pos + (x, 4, 1), "FF0000", "and"))
                    for x in range(bit_length)]
    arr[:, :, 2] = [(LogicGate(pos + (x, 1, 2), "0000FF", "and"),
                     LogicGate(pos + (x, 2, 2), "000000", "xor"),
                     LogicGate(pos + (x, 3, 2), "FF0000", "and"),
                     LogicGate(pos + (x, 4, 2), "FF0000", "and"))
                    for x in range(bit_length)]
    arr[:, :, 3] = [(LogicGate(pos + (x, 1, 3), "0000FF", "and"),
                     LogicGate(pos + (x, 2, 3), "000000", "nand"),
                     LogicGate(pos + (x, 3, 3), "FF0000", "and"),
                     LogicGate(pos + (x, 4, 3), "FF0000", "and"))
                    for x in range(bit_length)]
    arr[:, :, 4] = [(LogicGate(pos + (x, 1, 4), "0000FF", "and"),
                     LogicGate(pos + (x, 2, 4), "000000", "nor"),
                     LogicGate(pos + (x, 3, 4), "FF0000", "and"),
                     LogicGate(pos + (x, 4, 4), "FF0000", "and"))
                    for x in range(bit_length)]
    arr[:, :, 5] = [(LogicGate(pos + (x, 1, 5), "0000FF", "and"),
                     LogicGate(pos + (x, 2, 5), "000000", "xnor"),
                     LogicGate(pos + (x, 3, 5), "FF0000", "and"),
                     LogicGate(pos + (x, 4, 5), "FF0000", "and"))
                    for x in range(bit_length)]

    arr[:, [0, 1, 2], 6] = [(LogicGate(pos + (x, 1, 6), "0000FF", "and"),
                             LogicGate(pos + (x, 2, 6), "000000", "nand"),
                             LogicGate(pos + (x, 3, 6), "FF0000", "and"))
                            for x in range(bit_length)]
    arr[:, [0, 1, 2], 7] = [(LogicGate(pos + (x, 1, 7), "0000FF", "and"),
                             LogicGate(pos + (x, 2, 7), "000000", "nand"),
                             LogicGate(pos + (x, 3, 7), "FF0000", "and"))
                            for x in range(bit_length)]

    arr[:, [0, 1, 2], 8] = [(LogicGate(pos + (x, 1, 8), "0000FF", "and"),
                             LogicGate(pos + (x, 2, 8), "000000", "and"),
                             LogicGate(pos + (x, 3, 8), "FF0000", "and"))
                            for x in range(bit_length)]
    arr[:, [0, 1, 2], 9] = [(LogicGate(pos + (x, 1, 9), "0000FF", "and"),
                             LogicGate(pos + (x, 2, 9), "000000", "and"),
                             LogicGate(pos + (x, 3, 9), "FF0000", "and"))
                            for x in range(bit_length)]
    arr[:, [0, 1, 2], 10] = [(LogicGate(pos + (x, 1, 10), "0000FF", "and"),
                              LogicGate(pos + (x, 2, 10), "000000", "and"),
                              LogicGate(pos + (x, 3, 10), "FF0000", "and"))
                             for x in range(bit_length)]
    arr[:, [0, 1, 2], 11] = [(LogicGate(pos + (x, 1, 11), "0000FF", "and"),
                              LogicGate(pos + (x, 2, 11), "000000", "and"),
                              LogicGate(pos + (x, 3, 11), "FF0000", "and"))
                             for x in range(bit_length)]
    bp.add(arr[arr != np.array(None)], inputs, outputs)
