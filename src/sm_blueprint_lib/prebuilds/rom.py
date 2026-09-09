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

    W, H = page_size
    num_pages = max(1, ceil(len(data) / H))

    # Calculate exactly how much space the page writers will take to offset the binary inputs
    writers_cols = ceil(num_pages / max(1, H - 1))
    bin_x = W + 1

    arr = ndarray((W, H, 2), dtype=LogicGate)
    page_read = ndarray(H, dtype=LogicGate)
    page_read2 = ndarray(H, dtype=LogicGate)
    page_read_binary = ndarray((get_bits_required(H), 2), dtype=LogicGate)
    data_out = ndarray(W, dtype=LogicGate)
    page_writers_binary = ndarray(
        (get_bits_required(num_pages), 2), dtype=LogicGate)
    page_writers = []

    # Placed directly to the right of the memory array
    enable = LogicGate(pos + (W, H, 0), "FF00FF", 1)

    for x in range(W):
        for y in range(H):
            arr[x, y, :] = [
                LogicGate(pos + (x, y, 0), "000000", 0),
                LogicGate(pos + (x, y, 1), "0000FF", 1),
            ]

    # Shifted to the right of the memory cells (x = W)
    page_read[:] = [LogicGate(pos + (W, y, 0), "000000", 0) for y in range(H)]
    page_read2[:] = [LogicGate(pos + (W, y, 1), "000000", 0) for y in range(H)]

    # Shifted further right, past the page writers (x = bin_x)
    for x in range(get_bits_required(H)):
        page_read_binary[x] = (
            LogicGate(pos + (bin_x + x, H - 1, 0), "FF0000", 4),
            LogicGate(pos + (bin_x + x, H, 0), "FF0000", 1)
        )

    data_out[:] = [LogicGate(pos + (x, H, 0), "0000FF", 1) for x in range(W)]

    # Shifted to the right of the page_read_binary block
    for x in range(get_bits_required(num_pages)):
        page_writers_binary[x] = (
            LogicGate(pos + (bin_x + get_bits_required(H) +
                      x, H - 1, 0), "FF0000", 4),
            LogicGate(pos + (bin_x + get_bits_required(H) + x, H, 0), "FF0000", 1)
        )

    for i, data_batch in enumerate(batched(data, H)):
        # OPTIMIZATION 1: Skip generating the page decoder line if the whole page is 0
        if all(d == 0 for d in data_batch):
            page_writers.append(None)
            continue

        # Grow the page writers sequentially to the right (x = W + 1 onwards)
        g0 = LogicGate(
            pos + (W + 1 + i // max(1, H - 1), i % max(1, H - 1), 0), "000000", 0)
        page_writers.append(g0)

        for j, d in enumerate(reversed(data_batch)):
            # OPTIMIZATION 2: Skip wiring individual words if they are 0
            if d == 0:
                continue
            connect(g0, arr[:, (H - len(data_batch)) + j, 1]
                    [num_to_bit_list(d, W)])

    connect(arr[:, :, 1], arr[:, :, 0])
    connect(arr[:, :, 0], data_out)
    connect(page_read, page_read2)
    connect(page_read2, arr[:, :, 0].T)

    # Internal page row selector
    decoder(bp, H, precreated_inputs_binary=page_read_binary,
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
