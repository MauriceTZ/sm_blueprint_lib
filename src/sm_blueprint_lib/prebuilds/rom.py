from itertools import batched, cycle
from math import ceil
from typing import Sequence
from numpy import ndarray
from ..utils import get_bits_required, connect, num_to_bit_list
from ..blueprint import Blueprint
from ..parts import LogicGate
from ..prebuilds.decoder import decoder
from ..parts import Timer
from ..pos import *


def rom(
        bp: Blueprint,
        page_size: tuple[int, int],
        data: Sequence[int],
        pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)
    data = list(data)

    # Pre-calculate number of pages to avoid repetition
    num_pages = max(1, ceil(len(data) / page_size[1]))

    arr = ndarray((*page_size, 2), dtype=LogicGate)
    page_read = ndarray(page_size[1], dtype=LogicGate)
    page_read2 = ndarray(page_size[1], dtype=LogicGate)
    page_read_binary = ndarray(
        (get_bits_required(page_size[1]), 2), dtype=LogicGate)
    data_out = ndarray(page_size[0], dtype=LogicGate)

    page_writers_binary = ndarray(
        (get_bits_required(num_pages), 2), dtype=LogicGate)
    page_writers = []
    enable = LogicGate(pos + (-1, page_size[1], 0), "FF00FF", 1)

    for x in range(page_size[0]):
        for y in range(page_size[1]):
            arr[x, y, :] = [
                LogicGate(pos + (x, y, 0), "000000", 0),
                LogicGate(pos + (x, y, 1), "0000FF", 1),
            ]

    page_read[:] = [LogicGate(pos + (-1, y, 0), "000000", 0)
                    for y in range(page_size[1])]
    page_read2[:] = [LogicGate(pos + (-1, y, 1), "000000", 0)
                     for y in range(page_size[1])]

    offset0 = (-get_bits_required(page_size[1]) -
               get_bits_required(num_pages) - 1)

    for x in range(get_bits_required(page_size[1])):
        page_read_binary[x] = (
            LogicGate(pos + (x+offset0, page_size[1]-1, 0), "FF0000", 4),
            LogicGate(pos + (x+offset0, page_size[1], 0), "FF0000", 1)
        )

    data_out[:] = [LogicGate(pos + (x, page_size[1], 0), "0000FF", 1)
                   for x in range(page_size[0])]

    for x in range(get_bits_required(num_pages)):
        page_writers_binary[x] = (
            LogicGate(
                pos + (x+offset0+get_bits_required(page_size[1]), page_size[1]-1, 0), "FF0000", 4),
            LogicGate(
                pos + (x+offset0+get_bits_required(page_size[1]), page_size[1], 0), "FF0000", 1)
        )

    for i, data_batch in enumerate(batched(data, page_size[1])):
        # OPTIMIZATION 1: Skip generating the page decoder line if the whole page is 0
        if all(d == 0 for d in data_batch):
            page_writers.append(None)
            continue

        g0 = LogicGate(
            pos + (-2-i//(page_size[1]-1), i % (page_size[1]-1), 0), "000000", 0)
        page_writers.append(g0)

        for j, d in enumerate(reversed(data_batch)):
            # OPTIMIZATION 2: Skip wiring individual words if they are 0
            if d == 0:
                continue
            connect(g0, arr[:, (page_size[1] - len(data_batch)
                                ) + j, 1][num_to_bit_list(d, page_size[0])])

    connect(arr[:, :, 1], arr[:, :, 0])
    connect(arr[:, :, 0], data_out)
    connect(page_read, page_read2)
    connect(page_read2, arr[:, :, 0].T)

    # Internal page row selector
    decoder(bp, page_size[1], precreated_inputs_binary=page_read_binary,
            precreated_outputs=list(reversed(page_read)), precreated_output_enable=enable)

    # Manually wire the outer page selector to skip None elements safely
    for i, page_gate in enumerate(page_writers):
        if page_gate is None:
            continue
        bit_mask = num_to_bit_list(i, get_bits_required(num_pages))
        connect(page_writers_binary[~bit_mask, 0], page_gate)
        connect(page_writers_binary[bit_mask, 1], page_gate)

    # Filter out None values before adding to Blueprint
    valid_page_writers = [g for g in page_writers if g is not None]

    bp.add(arr, page_read, page_read2, page_read_binary, data_out,
           page_writers_binary, valid_page_writers, enable)

    return arr, page_read, page_read_binary, data_out, page_writers_binary, valid_page_writers, enable
