"""Synchronous 40Hz logic simulator for Scrap Mechanic blueprints.

Usage:
    from sm_blueprint_lib import Blueprint, LogicGate, Timer, connect
    from sm_blueprint_lib.simulator import Simulator

    bp = Blueprint()
    a = LogicGate(pos=(0,0,0), controller="and")
    b = LogicGate(pos=(1,0,0), controller="or")
    connect(a, b)
    bp.add(a, b)

    sim = Simulator(bp)
    sim.set(a, True)
    sim.tick(2)            # advance 2 game ticks (1/20th of a second)
    print(sim.get(b))      # -> True

The simulator is independent of the optional 3D `preview` module — importing
it does not pull in pygame / moderngl.
"""
from .simulator import Simulator, MutualGateConnectionError

__all__ = ["Simulator", "MutualGateConnectionError"]
