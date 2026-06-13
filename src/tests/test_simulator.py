"""Tests for the 40-tick logic simulator.

Run from the repo root:

    python src/tests/test_simulator.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # repo/src

import sm_blueprint_lib as sm
from sm_blueprint_lib.simulator import Simulator, MutualGateConnectionError


# ---------------------------------------------------------------------- helpers

def _make(gates_spec):
    """Quick way to build a blueprint with named LogicGates.

    ``gates_spec`` is a dict ``{name: mode}``. Returns ``(bp, parts_by_name)``.
    """
    bp = sm.Blueprint()
    parts = {}
    for i, (name, mode) in enumerate(gates_spec.items()):
        parts[name] = sm.LogicGate(pos=(i, 0, 0), color="ffffff", controller=mode)
    bp.add(*parts.values())
    return bp, parts


def assert_eq(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg}: expected {expected!r}, got {actual!r}")


# ---------------------------------------------------------------------- tests

def test_propagation_delay_is_one_tick_per_gate():
    """A high signal driven into A should reach C exactly two ticks later
    when the chain is A -> B -> C."""
    bp, p = _make({"a": "or", "b": "or", "c": "or"})
    sm.connect(p["a"], p["b"])
    sm.connect(p["b"], p["c"])

    s = Simulator(bp)
    s.set(p["a"], True)

    # tick 0: a is on (just set), b and c still off (haven't read yet)
    assert_eq(s.get(p["a"]), True, "a after set")
    assert_eq(s.get(p["b"]), False, "b before any tick")
    assert_eq(s.get(p["c"]), False, "c before any tick")

    s.tick()  # tick 1
    assert_eq(s.get(p["b"]), True, "b after 1 tick")
    assert_eq(s.get(p["c"]), False, "c after 1 tick")

    s.tick()  # tick 2
    assert_eq(s.get(p["c"]), True, "c after 2 ticks")


def test_basic_gate_truth_tables():
    """All six gate modes evaluate correctly with two driven inputs."""
    cases = [
        ("and",  [(0, 0, False), (1, 0, False), (0, 1, False), (1, 1, True)]),
        ("or",   [(0, 0, False), (1, 0, True),  (0, 1, True),  (1, 1, True)]),
        ("xor",  [(0, 0, False), (1, 0, True),  (0, 1, True),  (1, 1, False)]),
        ("nand", [(0, 0, True),  (1, 0, True),  (0, 1, True),  (1, 1, False)]),
        ("nor",  [(0, 0, True),  (1, 0, False), (0, 1, False), (1, 1, False)]),
        ("xnor", [(0, 0, True),  (1, 0, False), (0, 1, False), (1, 1, True)]),
    ]
    for mode, table in cases:
        for a_val, b_val, expected in table:
            bp = sm.Blueprint()
            a = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="or")
            b = sm.LogicGate(pos=(0, 0, 1), color="ff0000", controller="or")
            g = sm.LogicGate(pos=(0, 0, 2), color="ff0000", controller=mode)
            sm.connect(a, g)
            sm.connect(b, g)
            bp.add(a, b, g)

            sim = Simulator(bp)
            sim.set(a, bool(a_val))
            sim.set(b, bool(b_val))
            sim.tick()  # one tick is enough — a/b are pinned, g reads them
            assert_eq(
                sim.get(g), expected,
                f"{mode}({a_val},{b_val})"
            )


def test_self_loop_nand_oscillates_every_tick():
    """A NAND gate fed from itself should toggle on every tick (1-tick clock).
    This is the canonical Scrap Mechanic 'NOT itself' clock pattern."""
    bp = sm.Blueprint()
    g = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="nand")
    sm.connect(g, g)
    bp.add(g)

    sim = Simulator(bp)
    # Initial state is False; NAND of a single False input is True, so the
    # gate flips True on tick 1, False on tick 2, True on tick 3, ...
    expected = [True, False, True, False, True, False]
    for i, want in enumerate(expected, start=1):
        sim.tick()
        assert_eq(sim.get(g), want, f"tick {i}")


def test_mutual_gate_connection_is_rejected():
    """A->B and B->A between two distinct LogicGates is a hard error."""
    bp, p = _make({"a": "or", "b": "or"})
    sm.connect(p["a"], p["b"])
    sm.connect(p["b"], p["a"])

    raised = False
    try:
        Simulator(bp)
    except MutualGateConnectionError:
        raised = True
    if not raised:
        raise AssertionError("expected MutualGateConnectionError but none raised")


def test_self_loop_is_allowed_even_though_mutual_gates_arent():
    """Self-loop should pass validation."""
    bp = sm.Blueprint()
    g = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="nand")
    sm.connect(g, g)
    bp.add(g)
    Simulator(bp)  # should not raise


def test_timer_delays_signal_by_configured_ticks():
    """A timer with delay (0, 5) delays its input by 5 ticks."""
    bp = sm.Blueprint()
    src = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="or")
    t = sm.Timer(pos=(0, 0, 1), color="000000", controller=(0, 5))
    sink = sm.LogicGate(pos=(0, 0, 2), color="00ff00", controller="or")
    sm.connect(src, t)
    sm.connect(t, sink)
    bp.add(src, t, sink)

    sim = Simulator(bp)
    sim.set(src, True)

    # The signal must flow: src (pinned) -> timer (5-tick delay) -> sink (1-tick gate).
    # So sink should turn on at tick 5+1 = tick 6 in our model. Verify timer
    # output first, then the sink one tick later.
    for tick_no in range(1, 6):
        sim.tick()
        # Timer output is the value pushed `delay` ticks ago — initial False.
        # On the 5th tick, the True we pushed at tick 1 reaches the front.
    # After 5 ticks the timer output should be True.
    assert_eq(
        any(sim.get(t) for _ in [0]),  # silly OR to keep linter happy
        True,
        "timer output after 5 ticks",
    )
    sim.tick()  # +1 for sink propagation
    assert_eq(sim.get(sink), True, "sink after timer + 1 gate delay")


def test_timer_one_second_delay():
    """delay=(1, 0) is exactly 40 ticks."""
    bp = sm.Blueprint()
    src = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="or")
    t = sm.Timer(pos=(0, 0, 1), color="000000", controller=(1, 0))
    sm.connect(src, t)
    bp.add(src, t)

    sim = Simulator(bp)
    sim.set(src, True)

    # 39 ticks: timer still off
    sim.tick(39)
    assert_eq(sim.get(t), False, "timer still off at tick 39")
    sim.tick()
    assert_eq(sim.get(t), True, "timer on at tick 40")


def test_synchronous_update_chain_does_not_propagate_in_one_tick():
    """In SM, a chain of N gates takes N ticks for a signal to traverse — they
    don't all evaluate in topological order in a single tick."""
    bp = sm.Blueprint()
    chain = [sm.LogicGate(pos=(i, 0, 0), color="ffffff", controller="or") for i in range(5)]
    for i in range(len(chain) - 1):
        sm.connect(chain[i], chain[i + 1])
    bp.add(*chain)

    sim = Simulator(bp)
    sim.set(chain[0], True)
    # After 1 tick only chain[1] should have flipped.
    sim.tick()
    states = [sim.get(g) for g in chain]
    assert_eq(states, [True, True, False, False, False], "after 1 tick")
    sim.tick()
    assert_eq([sim.get(g) for g in chain], [True, True, True, False, False], "after 2 ticks")
    sim.tick(2)
    assert_eq([sim.get(g) for g in chain], [True, True, True, True, True], "after 4 ticks")


def test_set_overrides_inputs():
    """Pinning a part with set() prevents auto-evaluation even with inputs."""
    bp = sm.Blueprint()
    src = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="or")
    sink = sm.LogicGate(pos=(1, 0, 0), color="ff0000", controller="or")
    sm.connect(src, sink)
    bp.add(src, sink)

    sim = Simulator(bp)
    sim.set(src, True)
    sim.set(sink, False)  # pin sink off despite incoming True signal
    sim.tick(5)
    assert_eq(sim.get(sink), False, "sink stays pinned off")

    sim.unpin(sink)
    sim.tick()
    assert_eq(sim.get(sink), True, "sink picks up input after unpin")


def test_3_input_xor():
    """XOR with three inputs: true iff odd number of inputs are true."""
    bp = sm.Blueprint()
    a = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="or")
    b = sm.LogicGate(pos=(0, 0, 1), color="ff0000", controller="or")
    c = sm.LogicGate(pos=(0, 0, 2), color="ff0000", controller="or")
    g = sm.LogicGate(pos=(1, 0, 0), color="00ff00", controller="xor")
    sm.connect(a, g); sm.connect(b, g); sm.connect(c, g)
    bp.add(a, b, c, g)

    for mask in range(8):
        sim = Simulator(bp)
        sim.set(a, bool(mask & 1))
        sim.set(b, bool(mask & 2))
        sim.set(c, bool(mask & 4))
        sim.tick()
        bits = bin(mask).count("1")
        assert_eq(sim.get(g), bits % 2 == 1, f"xor mask={mask:03b}")


# ---------------------------------------------------------------------- runner

def main():
    tests = [
        ("propagation_delay_is_one_tick_per_gate", test_propagation_delay_is_one_tick_per_gate),
        ("basic_gate_truth_tables", test_basic_gate_truth_tables),
        ("self_loop_nand_oscillates_every_tick", test_self_loop_nand_oscillates_every_tick),
        ("mutual_gate_connection_is_rejected", test_mutual_gate_connection_is_rejected),
        ("self_loop_is_allowed_even_though_mutual_gates_arent", test_self_loop_is_allowed_even_though_mutual_gates_arent),
        ("timer_delays_signal_by_configured_ticks", test_timer_delays_signal_by_configured_ticks),
        ("timer_one_second_delay", test_timer_one_second_delay),
        ("synchronous_update_chain_does_not_propagate_in_one_tick", test_synchronous_update_chain_does_not_propagate_in_one_tick),
        ("set_overrides_inputs", test_set_overrides_inputs),
        ("3_input_xor", test_3_input_xor),
    ]
    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failures.append((name, str(e)))
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
