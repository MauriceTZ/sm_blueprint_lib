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


import numpy as np
from typing import Sequence
from ..utils import connect
from ..blueprint import Blueprint
from ..parts import LogicGate, Timer
from ..pos import Pos, check_pos

def cla_1tick(bp: Blueprint, 
              bit_length: int, 
              pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)
    
    red, black, blue = "FF0000", "000000", "0000FF"
    N = bit_length

    assert N > 0, "bit_length must be greater than 0"

    # 1. Input Arrays (Y = 0)
    # Bit 0 (LSB) is at X = 0.
    input_a = np.array([LogicGate(pos + (x, 0, 0), red, "or") for x in range(N)])
    input_b = np.array([LogicGate(pos + (x + N + 1, 0, 0), red, "xor") for x in range(N)])

    # 2. First Logic Layer (Y = -1)
    and_a1 = np.array([LogicGate(pos + (x, -1, 0), black, "and") for x in range(N)])
    xor_b1 = np.array([LogicGate(pos + (x + N + 1, -1, 0), black, "xor") for x in range(N)])

    # 3. Output Array (Y = -2)
    output = np.array([LogicGate(pos + (x, -2, 0), blue, "xor") for x in range(N)])

    # 4. AND Matrix Generation (Y = -2)
    and_matrix_b2 = np.full((N, N), None, dtype=object)
    for n in range(N):
        and_matrix_b2[n, :n + 1] = [
            LogicGate(pos + (N + 1 + m, -2, N - n - 1), black, "and") 
            for m in range(n + 1)
        ]

    # 5. OR / Carry / Enables Layers (Y = -3, Y = -4)
    or_b3 = np.array([LogicGate(pos + (x + N + 1, -3, 0), black if x != N - 1 else blue, "or") for x in range(N)])
    carry_inverted = LogicGate(pos + (2 * N, -4, 0), blue, "nor")
    enable_a4 = np.array([LogicGate(pos + (x, -3, 0), blue, "and") for x in range(N)])

    # 6. Global Controllers (Y = -2, Y = -3)
    add_subtract = LogicGate(pos + (2 * N + 1, -2, 0), red, "or")
    enable_out = LogicGate(pos + (2 * N + 1, -3, 0), red, "or")

    # 7. Timers (Y = -2, Y = -1)
    timer_carry_in_to_matrix = Timer(pos + (2 * N + 1, -2, 1), black, (0, 0))
    timer_output_0 = Timer(pos + (0, -2, 1), black, (0, 2))  # Bound to LSB at X=0
    
    # XOR Timers cover bits 1 through N-1
    timers_xor_b1_to_output = np.array([Timer(pos + (x + N + 1, -1, 1), black, (0, 1)) for x in range(1, N)])
    timers_and_a1_to_or_b3 = np.array([Timer(pos + (x, -1, 1), black, (0, 0)) for x in range(N)])

    # --- Connections ---
    
    # Global Controls
    connect(add_subtract, output[0])           # C_in to LSB output
    connect(add_subtract, input_b)             # Toggle subtraction inversion
    connect(enable_out, enable_a4)

    # Carry In Timer
    connect(add_subtract, timer_carry_in_to_matrix)
    connect(timer_carry_in_to_matrix, [and_matrix_b2[n, 0] for n in range(N)])

    # Output 0 (LSB) Timer
    connect(output[0], timer_output_0)
    connect(timer_output_0, enable_a4[0])

    # XOR / Output Timers (Bits 1 to N-1)
    connect(xor_b1[1:], timers_xor_b1_to_output)
    connect(timers_xor_b1_to_output, output[1:])

    # AND / OR Timers (Bits 0 to N-1)
    connect(and_a1, timers_and_a1_to_or_b3)
    connect(timers_and_a1_to_or_b3, or_b3)
    connect(timers_and_a1_to_or_b3[N - 1], carry_inverted)  # MSB generate to carry inverted

    # Initial Input Wiring
    connect(input_a, and_a1)
    connect(input_a, xor_b1)
    connect(input_b, and_a1)
    connect(input_b, xor_b1)

    connect(input_a[0], output[0])
    connect(input_b[0], output[0])

    # Output Enable Wiring
    connect(output[1:], enable_a4[1:])

    # --- Matrix Complex Wiring (LSB to MSB) ---
    
    # 1. Output of Matrix -> OR gates
    for n in range(N):
        valid_gates = [l for l in and_matrix_b2[n, :n + 1] if l is not None]
        connect(valid_gates, or_b3[n])

    # 2. Generates (G) to Matrix
    for m in range(1, N):
        g_gate = and_a1[m - 1]
        target_gates = [and_matrix_b2[n, m] for n in range(m, N)]
        connect(g_gate, target_gates)

    # 3. Propagates (P) to Matrix
    for i in range(N):
        p_gate = xor_b1[i]
        target_gates = []
        for n in range(i, N):
            for m in range(i + 1):
                target_gates.append(and_matrix_b2[n, m])
        connect(p_gate, target_gates)

    # Carry inverted NOR gets all terms of the MSB carry
    connect([and_matrix_b2[N - 1, m] for m in range(N)], carry_inverted)

    # Final OR cascade to output (C_n -> Output n+1)
    connect(or_b3[:-1], output[1:])

    # --- Blueprint Registration ---
    
    valid_matrix_gates = [gate for gate in and_matrix_b2.flatten() if gate is not None]

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
