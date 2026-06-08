from typing import Sequence, Hashable, TypeAlias
from numpy import array
from ..blueprint import Blueprint
from ..parts import LogicGate
from ..pos import *
from ..utils import get_bits_required, connect, num_to_bit_list


State: TypeAlias = Hashable
Input: TypeAlias = Hashable
CurrentState: TypeAlias = Hashable
NextState: TypeAlias = Hashable


def finite_state_machine(bp: Blueprint,
                         input_alphabet: list[Input],
                         state_set: list[State],
                         initial_state: State,
                         state_transition_table: dict[tuple[CurrentState, Input], NextState],
                         color_per_state: dict[State, str] = dict(),
                         color_per_input: dict[State, str] = dict(),
                         pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)
    assert input_alphabet, "The set of Input Alphabet cannot be empty."
    assert state_set, "The set of States cannot be empty."
    assert initial_state in state_set, "The Initial state MUST BE an element of the set of States."

    n_bit_states = get_bits_required(len(state_set))

    state_bits = array([(LogicGate((x, 0, 0), "0000FF", 2),
                         LogicGate((x, -1, 0), "000000", 0),
                         LogicGate((x, -2, 0), "000000", 3))
                        for x in range(n_bit_states)], dtype=LogicGate)
    connect(state_bits[:, 0], state_bits[:, 0])
    connect(state_bits[:, 0], state_bits[:, 1:])

    input_signals = array([(LogicGate((-1-len(input_alphabet)+x, 0, 0), color_per_input.get(input_sym, "FF0000"), 1),
                            LogicGate(
                                (-1-len(input_alphabet)+x, -1, 0), "000000", 3),
                            LogicGate((-1-len(input_alphabet)+x, -2, 0), "000000", 0))
                           for x, input_sym in enumerate(input_alphabet)], dtype=LogicGate)
    connect(input_signals[:, 0], input_signals[:, 1:])
    connect(input_signals[:, 1], input_signals[:, 2])

    dec_state_bits = array([LogicGate((-1, -3-y, 0), color_per_state.get(state, "000000"), 0)
                            for y, state in enumerate(state_set)], dtype=LogicGate)
    initial_state_index = state_set.index(initial_state)
    transition_gates = {}
    print("State Transition table (top view):")
    for i, state in reversed(list(enumerate(state_set))):
        curr_state_index = (i-initial_state_index) % len(state_set)
        bits = num_to_bit_list(curr_state_index, n_bit_states)
        # print(bits, state)
        connect(state_bits[bits, 1], dec_state_bits[i])
        connect(state_bits[~bits, 2], dec_state_bits[i])
        for j, input_sym in reversed(list(enumerate(input_alphabet))):
            if (next_state := state_transition_table.get((state, input_sym))) is not None:
                g = LogicGate((-1-len(input_alphabet)+j, -3-i, 0), "000000", 0)
                transition_gates.setdefault((state, input_sym), []).append(g)
                connect((dec_state_bits[i], input_signals[j, 2]), g)
                next_state_index = (state_set.index(
                    next_state)-initial_state_index) % len(state_set)
                mask = curr_state_index ^ next_state_index
                connect(g, state_bits[num_to_bit_list(mask, n_bit_states), 0])
            print("(%s, %s) -> %s" % (state, input_sym, next_state), end="\t")
        print()

    # for i, ((curr_state, input_sym), next_state) in enumerate(state_transition_table.items()):
    #     print(i, (curr_state, input_sym), next_state)

    bp.add(state_bits, input_signals, dec_state_bits, transition_gates.values())
    return state_bits, input_signals, dec_state_bits, transition_gates
