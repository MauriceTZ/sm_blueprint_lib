from itertools import cycle
from typing import Sequence
from numpy import array
from ..utils import get_bits_required, _old_connect, int_to_hex, connect
from ..blueprint import Blueprint
from ..parts import LogicGate, Timer
from ..pos import *
from ..prebuilds.decoder import decoder


def nor_register(bp: Blueprint, bit_length: int, pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)

    cells = []
    for j in range(bit_length):
        cell_pos = pos + (j * 2, 0, 0)
        cell = [LogicGate(cell_pos + (0, 2, 0), "FF0000", 4, xaxis=-2, zaxis=-1),
                LogicGate(cell_pos + (1, 2, 0), "880000",
                          0, xaxis=-2, zaxis=-1),
                LogicGate(cell_pos + (0, 1, 0), "000000",
                          4, xaxis=-2, zaxis=-1),
                LogicGate(cell_pos + (1, 1, 0), "000088",
                          4, xaxis=-2, zaxis=-1),
                Timer(cell_pos + (0, 0, 0), "0000FF",
                      (0, 0), xaxis=-2, zaxis=-1),
                LogicGate(cell_pos + (1, 0, 0), "00FF00",
                          0, xaxis=-2, zaxis=-1)
                ]
        connect(cell[0], cell[2])
        connect(cell[1], cell[3])
        cell[2].connect(cell[4]).connect(cell[3]).connect(cell[2])
        connect(cell[4], cell[5])
        cells.append(cell)

    inputs = []
    for j in range(bit_length):
        input_pos = pos + (j * 2, 3, 0)
        input_gate = LogicGate(input_pos, "FFFF00", 1, xaxis=-2, zaxis=-1)
        inputs.append(input_gate)

    write_enable = [LogicGate(pos + (bit_length * 2, 3, 0), "FFFFFF", 1, xaxis=-2, zaxis=-1),
                    LogicGate(pos + (bit_length * 2, 2, 0), "888888", 4, xaxis=-2, zaxis=-1)]

    read_enable = LogicGate(pos + (bit_length * 2 + 1, 3, 0), "FFFFFF", 1, xaxis=-2, zaxis=-1)

    # Connect everything
    connect(write_enable[0], write_enable[1])
    for j in range(bit_length):
        connect(inputs[j], cells[j][0])
        connect(inputs[j], cells[j][1])
        connect(write_enable[0], cells[j][1])
        connect(write_enable[1], cells[j][0])
        connect(read_enable, cells[j][5])

    bp.add(cells)
    bp.add(inputs)
    bp.add(write_enable)
    bp.add(read_enable)
    return cells, inputs, write_enable, read_enable


def nor_ram(bp: Blueprint, bit_length: int, num_address: int, pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)

    cells = []
    for i in range(num_address):
        row = []
        for j in range(bit_length):
            cell_pos = pos + (j * 2, 0, i * 2)
            cell = [LogicGate(cell_pos + (0, 2, 0), "FF0000", 4, xaxis=-2, zaxis=-1),
                    LogicGate(cell_pos + (1, 2, 0), "880000",
                              0, xaxis=-2, zaxis=-1),
                    LogicGate(cell_pos + (0, 1, 0), "000000",
                              4, xaxis=-2, zaxis=-1),
                    LogicGate(cell_pos + (1, 1, 0), "000088",
                              4, xaxis=-2, zaxis=-1),
                    Timer(cell_pos + (0, 0, 0), "0000FF",
                          (0, 0), xaxis=-2, zaxis=-1),
                    # Read out gates
                    LogicGate(cell_pos + (1, 0, 0), "00FF00", 0, xaxis=-2, zaxis=-1)]
            connect(cell[0], cell[2])
            connect(cell[1], cell[3])
            connect(cell[4], cell[5])
            cell[2].connect(cell[4]).connect(cell[3]).connect(cell[2])
            row.append(cell)
        cells.append(row)

    inputs = []
    for j in range(bit_length):
        input_pos = pos + (j * 2, 3, 0)
        input_gate = LogicGate(input_pos, "FFFF00", 1, xaxis=-2, zaxis=-1)
        inputs.append(input_gate)

    outputs = []
    for j in range(bit_length):
        output_pos = pos + (j * 2, 3, 2)
        output_gate = LogicGate(output_pos, "00FFFF", 1, xaxis=-2, zaxis=-1)
        outputs.append(output_gate)

    write_enable = LogicGate(pos + (bit_length * 2, 3, 0),
                             "FFFFFF", 1, xaxis=-2, zaxis=-1)

    read_enable = LogicGate(pos + (bit_length * 2 + 1, 3, 0),
                            "888888", 1, xaxis=-2, zaxis=-1)

    # Write selector
    selectors_write = []
    for i in range(num_address):
        selector_pos = pos + (bit_length * 2, 2, i * 2)
        selector = [LogicGate(selector_pos, "00FF00", 0, xaxis=-2, zaxis=-1),
                    LogicGate(selector_pos + (1, 0, 0), "008800", 3, xaxis=-2, zaxis=-1)]
        selectors_write.append(selector)
        connect(selector[0], selector[1])

    selector_binary = []
    for i in range(get_bits_required(num_address)):
        selector_binary.append([LogicGate(pos + (bit_length * 2 + i + 2, 3, 0), "FFFF00", 1, xaxis=-2, zaxis=-1),
                                LogicGate(pos + (bit_length * 2 + i + 2, 2, 0), "888800", 4, xaxis=-2, zaxis=-1)])

    # Read selector
    selectors_read = []
    for i in range(num_address):
        selector_pos = pos + (bit_length * 2, 1, i * 2)
        selector = LogicGate(selector_pos, "00FF00", 0, xaxis=-2, zaxis=-1)
        selectors_read.append(selector)

    # selector_binary_read = []
    # for i in range(get_bits_required(num_address)):
    #     selector_binary_read.append([LogicGate(pos + (bit_length * 2 + i + 2, 1, 0), "FFFF00", 1, xaxis=-2, zaxis=-1),
    #                                   LogicGate(pos + (bit_length * 2 + i + 2, 0, 0), "888800", 4, xaxis=-2, zaxis=-1)])

    # Connect everything
    for i in range(num_address):
        for j in range(bit_length):
            connect(selectors_write[i][0], cells[i][j][1])
            connect(selectors_write[i][1], cells[i][j][0])
            connect(inputs[j], cells[i][j][0])
            connect(inputs[j], cells[i][j][1])

    decoder(bp, num_address, (0, 0, 0), precreated_inputs_binary=array(selector_binary),
            precreated_outputs=array(selectors_write)[::-1, 0], precreated_output_enable=write_enable)
    decoder(bp, num_address, (0, 0, 0), precreated_inputs_binary=array(selector_binary),
            precreated_outputs=array(selectors_read)[::-1], precreated_output_enable=read_enable)

    # Connect read selector to read out gates, and read out gates to outputs
    for i in range(num_address):
        for j in range(bit_length):
            connect(selectors_read[i], cells[i][j][5])
            connect(cells[i][j][5], outputs[j])

    bp.add(cells)
    bp.add(inputs)
    bp.add(outputs)
    bp.add(write_enable)
    bp.add(read_enable)
    bp.add(selectors_write)
    bp.add(selector_binary)
    bp.add(selectors_read)
    return cells, inputs, outputs, write_enable, read_enable, selectors_write, selector_binary, selectors_read
