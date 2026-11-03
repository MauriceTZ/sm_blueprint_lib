"""Tests for xor_rom, checked tick by tick with the logic simulator.

Run from the repo root:

    python src/tests/test_xor_rom.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # repo/src

import sm_blueprint_lib as sm
from sm_blueprint_lib.simulator import Simulator

PI = "3141592653589793238462643383279502884197169399375105820974944592"


def _check_every_address(data, address_bits=None, max_ticks=2, effort=0.5):
    """Build the ROM, then for every address: the data must be right `rom.ticks` ticks after the
    address changes and stay right. Returns the ROM."""
    bp = sm.Blueprint()
    rom = sm.xor_rom(bp, data, address_bits=address_bits, max_ticks=max_ticks, effort=effort)
    table = [data(x) for x in range(1 << len(rom.address))] if callable(data) else \
        list(data) + [0] * ((1 << len(rom.address)) - len(data))
    assert rom.ticks <= max_ticks, f"answers in {rom.ticks} ticks, asked for {max_ticks}"
    sim = Simulator(bp)
    read = lambda: sum(sim.get(g) << b for b, g in enumerate(rom.data))
    for x in range(len(table)):
        for i, g in enumerate(rom.address):
            sim.set(g, x >> i & 1)
        sim.tick(rom.ticks + 1)          # +1: the address gates themselves take the first tick
        for _ in range(3):
            assert read() == table[x], f"address {x}: got {read()}, want {table[x]}"
            sim.tick()
    return rom


def test_list_of_values():
    rom = _check_every_address([int(c) for c in PI[:16]])
    assert len(rom.address) == 4 and len(rom.data) == 4


def test_short_list_is_padded_with_zeros():
    rom = _check_every_address([7, 1, 7])
    assert len(rom.address) == 2


def test_function_two_ticks():
    _check_every_address(lambda x: (x & 7) * (x >> 3), address_bits=6, max_ticks=2)


def test_function_three_ticks():
    _check_every_address(lambda x: bin(x).count("1"), address_bits=7, max_ticks=3)


def test_function_four_ticks():
    _check_every_address(lambda x: round(127.5 + 127.5 * math.sin(2 * math.pi * x / 64)), address_bits=6,
                         max_ticks=4)


def test_constant_outputs():
    # bit 2 is always 1 and bit 3 always 0: both still need correct output gates
    _check_every_address(lambda x: 0b0100 | (x & 1), address_bits=3, max_ticks=2)


def test_more_ticks_never_costs_gates():
    data = lambda x: min(x & 15, x >> 4)
    options = sm.xor_rom_options(data, address_bits=8, max_ticks=4, effort=0.5)
    assert list(options) == [2, 3, 4]
    assert options[2] >= options[3] >= options[4], options


def test_same_seed_same_rom():
    a = sm.xor_rom(sm.Blueprint(), lambda x: (x * 37) % 251 & 255, address_bits=8, effort=0.5)
    b = sm.xor_rom(sm.Blueprint(), lambda x: (x * 37) % 251 & 255, address_bits=8, effort=0.5)
    assert a.gates == b.gates


def test_every_part_has_its_own_cell():
    bp = sm.Blueprint()
    sm.xor_rom(bp, lambda x: (x & 7) + (x >> 3), address_bits=6, max_ticks=3, effort=0.5)
    cells = [(p.pos.x, p.pos.y, p.pos.z) for p in bp.bodies[0].childs]
    assert len(cells) == len(set(cells))


def test_bad_input_is_rejected():
    for kwargs in ({"data": lambda x: x}, {"data": [1, 2], "max_ticks": 1}, {"data": [-1]},
                   {"data": lambda x: x, "address_bits": 13}):
        try:
            sm.xor_rom(sm.Blueprint(), **kwargs)
        except ValueError:
            continue
        raise AssertionError(f"accepted {kwargs}")


def main():
    tests = [(name[5:], fn) for name, fn in globals().items() if name.startswith("test_")]
    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failures.append(name)
            print(f"FAIL {name}: {e}")
        else:
            print(f"ok   {name}")
    print()
    if failures:
        print(f"{len(failures)} / {len(tests)} test(s) failed")
        sys.exit(1)
    print(f"all {len(tests)} tests passed")


if __name__ == "__main__":
    main()
