import numpy as np
from typing import Sequence
from numpy import ndarray
from ..utils import get_bits_required, connect, num_to_bit_list
from ..blueprint import Blueprint
from ..parts import LogicGate, Timer
from ..pos import *


def simple_adder_subtractor(bp: Blueprint,
                            bit_length: int,
                            pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)
    input_a = [LogicGate(pos+(x, 0, 2), "FF0000", 1)
               for x in range(bit_length)]
    input_b = [LogicGate(pos+(x, 0, 0), "FF0000", 2)
               for x in range(bit_length)]
    and_0 = [LogicGate(pos+(x, -1, 2), "000000", 0)
             for x in range(bit_length)]
    xor_0 = [LogicGate(pos+(x, -1, 0), "000000", 2)
             for x in range(bit_length)]
    or_0 = [LogicGate(pos+((x, -2, 0) if x + 1 != bit_length else (x+1, -2, 2)), "000000" if x + 1 != bit_length else "0000FF", 1)
            for x in range(bit_length)]
    and_1 = [LogicGate(pos+(x, -2, 1), "000000", 0)
             for x in range(bit_length)]
    xor_1 = [LogicGate(pos+(x, -2, 2), "0000FF", 2)
             for x in range(bit_length)]
    carry_in = LogicGate(pos+(-1, -2, 0), "FF0000", 1)

    connect(input_a, and_0)
    connect(input_a, xor_0)
    connect(input_b, and_0)
    connect(input_b, xor_0)
    connect(and_0, or_0)
    connect(xor_0, and_1)
    connect(xor_0, xor_1)
    connect(and_1, or_0)
    connect(or_0, and_1[1:])
    connect(or_0, xor_1[1:])
    connect(carry_in, and_1[0])
    connect(carry_in, xor_1[0])
    connect(carry_in, input_b)

    bp.add(input_a, input_b, and_0, xor_0, or_0, and_1, xor_1, carry_in)
    return input_a, input_b, and_0, xor_0, or_0, and_1, xor_1, carry_in


def cla_1tick(bp: Blueprint,
              bit_length: int,
              pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)

    # Simple color constants to match the old SMTool style
    red, black, blue = "FF0000", "000000", "0000FF"

    assert bit_length > 0, "bit_length must be greater than 0"

    # 1. Input Arrays
    input_a = np.array([LogicGate(pos + (x, 0, 0), red, "or")
                       for x in range(bit_length)])
    input_b = np.array([LogicGate(
        pos + (x + bit_length + 1, 0, 0), red, "xor") for x in range(bit_length)])

    # 2. First Logic Layer
    and_a1 = np.array([LogicGate(pos + (x, 1, 0), black, "and")
                      for x in range(bit_length)])
    xor_b1 = np.array([LogicGate(pos + (x + bit_length + 1, 1, 0),
                      black, "xor") for x in range(bit_length)])

    # 3. Output Array
    output = np.array([LogicGate(pos + (x, 2, 0), blue, "xor")
                      for x in range(bit_length)])

    # 4. AND Matrix Generation
    and_matrix_b2 = np.full((bit_length, bit_length), None, dtype=object)
    for n in range(bit_length):
        and_matrix_b2[n, : n + 1] = [
            LogicGate(pos + (x + bit_length + 1, 2,
                      bit_length - n - 1), black, "and")
            for x in range(n + 1)
        ]

    # 5. OR / Carry / Enables Layers
    or_b3 = np.array([LogicGate(pos + (x + bit_length + 1, 3, 0),
                     black if x != 0 else blue, "or") for x in range(bit_length)])
    carry_inverted = LogicGate(pos + (bit_length + 1, 4, 0), blue, "nor")
    enable_a4 = np.array([LogicGate(pos + (x, 3, 0), blue, "and")
                         for x in range(bit_length)])

    # 6. Global Controllers
    add_subtract = LogicGate(pos + (bit_length * 2 + 1, 2, 0), red, "or")
    enable_out = LogicGate(pos + (bit_length * 2 + 1, 3, 0), red, "or")

    # 7. Timers (passing (seconds, ticks) as the controller argument)
    timer_carry_in_to_matrix = Timer(
        pos + (bit_length * 2 + 1, 2, 1), black, (0, 0))
    timer_output_0 = Timer(pos + (bit_length - 1, 2, 1), black, (0, 2))
    timers_xor_b1_to_output = np.array([Timer(
        pos + (bit_length + x + 1, 1, 1), black, (0, 1)) for x in range(bit_length - 1)])
    timers_and_a1_to_or_b3 = np.array(
        [Timer(pos + (x, 1, 1), black, (0, 0)) for x in range(bit_length)])

    # --- Connections ---

    # Global Controls
    connect(add_subtract, output[-1])
    connect(add_subtract, input_b)
    connect(enable_out, enable_a4)

    # Carry In Timer
    connect(add_subtract, timer_carry_in_to_matrix)
    connect(timer_carry_in_to_matrix, [
            l for l in and_matrix_b2[-1] if l is not None])

    # Output 0 Timer
    connect(output[-1], timer_output_0)
    connect(timer_output_0, enable_a4[-1])

    # XOR / Output Timers
    connect(xor_b1[:-1], timers_xor_b1_to_output)
    connect(timers_xor_b1_to_output, output[:-1])

    # AND / OR Timers
    connect(and_a1, timers_and_a1_to_or_b3)
    connect(timers_and_a1_to_or_b3, or_b3)
    connect(timers_and_a1_to_or_b3[0], carry_inverted)

    # Initial Input Wiring
    connect(input_a, and_a1)
    connect(input_a, xor_b1)
    connect(input_b, and_a1)
    connect(input_b, xor_b1)

    connect(input_a[-1], output[-1])
    connect(input_b[-1], output[-1])

    # Output Enable Wiring
    connect(output[:-1], enable_a4[:-1])

    # Matrix Complex Wiring
    for n in range(1, bit_length):
        valid_gates = [l for l in and_matrix_b2[n - 1, :n] if l is not None]
        if valid_gates:
            connect(and_a1[n], valid_gates)

    for n in range(bit_length):
        valid_gates = [l for l in and_matrix_b2[n:,
                                                :n + 1].flatten() if l is not None]
        if valid_gates:
            connect(xor_b1[n], valid_gates)

    for n in range(bit_length):
        valid_gates = [l for l in and_matrix_b2[n:, n] if l is not None]
        if valid_gates:
            connect(valid_gates, or_b3[n])

    carry_inv_gates = [l for l in and_matrix_b2[:, 0] if l is not None]
    if carry_inv_gates:
        connect(carry_inv_gates, carry_inverted)

    # Final OR cascade to output
    connect(or_b3[1:], output[:-1])

    # --- Blueprint Registration ---

    valid_matrix_gates = [
        gate for gate in and_matrix_b2.flatten() if gate is not None]

    bp.add(
        input_a, input_b, and_a1, xor_b1, output, valid_matrix_gates,
        or_b3, carry_inverted, enable_a4, add_subtract, enable_out,
        timer_carry_in_to_matrix, timer_output_0,
        timers_xor_b1_to_output, timers_and_a1_to_or_b3
    )

    return (
        input_a, input_b, and_a1, xor_b1, output, valid_matrix_gates,
        or_b3, carry_inverted, enable_a4, add_subtract, enable_out,
        timer_carry_in_to_matrix, timer_output_0,
        timers_xor_b1_to_output, timers_and_a1_to_or_b3
    )
