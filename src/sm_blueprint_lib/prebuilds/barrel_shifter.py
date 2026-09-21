from typing import Sequence
from numpy import ndarray
from ..utils import get_bits_required, connect, num_to_bit_list
from ..blueprint import Blueprint
from ..parts import LogicGate
from ..pos import *


def barrel_shifter(bp: Blueprint, bit_length: int, num_bit_shift: int, pos: Pos | Sequence = (0, 0, 0), signed=True):
    pos = check_pos(pos)
    Y_offset = num_bit_shift

    if signed:
        # Calculate maximum leftward shift to prevent negative X coordinates
        X_offset = 2 ** (num_bit_shift - 1)

        inputs = [LogicGate(pos + (x + X_offset, Y_offset, 0), "FF0000", 1)
                  for x in range(bit_length)]

        inputs_shift_binary = ndarray((num_bit_shift, 2), dtype=LogicGate)
        for x in range(num_bit_shift):
            inputs_shift_binary[x, :] = [
                LogicGate(pos + (bit_length + X_offset +
                          x + 1, Y_offset, 0), "FF0000", 4),
                LogicGate(pos + (bit_length + X_offset + x +
                          1, Y_offset + 1, 0), "FF0000", 1),
            ]

        arr = [
            [
                [LogicGate(pos + (x + X_offset, Y_offset - y - 1, 0), "000000")
                 for x in range(bit_length + (2**y - 1 if y != num_bit_shift - 1 else 0))]
                for y in range(num_bit_shift)
            ],
            [
                [LogicGate(pos + ((x - (2**y if y == num_bit_shift-1 else 0)) + X_offset, Y_offset - y - 1, 1), "000000")
                 for x in range(2**y, bit_length + 2**(y+1) - 1 - (2**y if y == num_bit_shift-1 else 0))]
                for y in range(num_bit_shift)
            ],
            [
                [LogicGate(pos + (x + X_offset, Y_offset - y - 1, 2), "000000" if y != num_bit_shift - 1 else "0000FF", 1)
                 for x in range(bit_length - 1 + (2**(y+1) if y != num_bit_shift-1 else 1))]
                for y in range(num_bit_shift)
            ],
        ]

        connect(inputs, arr[0][0])
        connect(inputs, arr[1][0])

        for y in range(num_bit_shift):
            connect(arr[0][y], arr[2][y])
        for y in range(num_bit_shift-1):
            connect(arr[2][y], arr[0][y+1])
            connect(arr[1][y], arr[2][y][2**y:])
        for y in range(num_bit_shift-2):
            connect(arr[2][y], arr[1][y+1])

        connect(arr[2][-2][2**(num_bit_shift-1):], arr[1][-1])
        connect(arr[1][-1], arr[2][-1])

        for y in range(num_bit_shift):
            connect(inputs_shift_binary[y, 0], arr[0][y])
            connect(inputs_shift_binary[y, 1], arr[1][y])

        bp.add(inputs, inputs_shift_binary, arr)
        return inputs, inputs_shift_binary, arr

    else:
        # Unsigned implementation (shifted X by +1 to fit always_off at 0)
        inputs = [LogicGate(pos + (x + 1, Y_offset, 0), "FF0000", 1)
                  for x in range(bit_length)]
        inputs_shift_binary = ndarray((num_bit_shift, 2), dtype=LogicGate)
        always_off = LogicGate(pos + (0, Y_offset, 0), "000000")

        for x in range(num_bit_shift):
            inputs_shift_binary[x, :] = [
                LogicGate(pos + (x + bit_length + 2,
                          Y_offset, 0), "FF0000", 4),
                LogicGate(pos + (x + bit_length + 2,
                          Y_offset + 1, 0), "FF0000", 1),
            ]

        arr = ndarray((bit_length, num_bit_shift, 3), dtype=LogicGate)
        for x in range(bit_length):
            for y in range(num_bit_shift):
                arr[x, y, :] = [
                    LogicGate(pos + (x + 1, Y_offset - y - 1, 0), "000000"),
                    LogicGate(pos + (x + 1, Y_offset - y - 1, 1), "000000"),
                    LogicGate(pos + (x + 1, Y_offset - y - 1, 2),
                              "000000" if y + 1 < num_bit_shift else "0000FF", 1),
                ]

        always_off.connect(always_off)

        connect(inputs, arr[:, 0, 0])
        connect(inputs, arr[1:, 0, 1])
        connect(arr[:, :, 0], arr[:, :, 2])
        connect(arr[:, :, 1], arr[:, :, 2])
        connect(arr[:, :, 2], arr[:, 1:, 0])

        for y in range(num_bit_shift):
            if y + 1 < num_bit_shift:
                connect(arr[:, y, 2], arr[2**(y+1):, y+1, 1])
            connect(always_off, arr[:2**y, y, 1])
            connect(inputs_shift_binary[y, 0], arr[:, y, 0])
            connect(inputs_shift_binary[y, 1], arr[:, y, 1])

        bp.add(inputs, inputs_shift_binary, arr, always_off)
        return inputs, inputs_shift_binary, arr, always_off
