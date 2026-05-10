"""Tick-accurate logic simulator for Scrap Mechanic blueprints.

Scrap Mechanic runs logic at 40 ticks per second. On every tick each logic
gate reads its current inputs, computes its next state, and all gates commit
simultaneously. This gives every gate a one-tick propagation delay and makes
the network synchronous (double-buffered).

Key rules enforced:
    * Two distinct ``LogicGate`` parts cannot be wired into each other (i.e.
      ``A -> B`` and ``B -> A`` simultaneously). Attempting to construct a
      :class:`Simulator` over such a blueprint raises
      :class:`MutualGateConnectionError`.
    * A logic gate may be wired into itself (``A -> A``); this is the standard
      Scrap Mechanic way to build a 1-tick toggle from a NAND/NOR with a single
      input.

The simulator does not require the optional ``preview`` dependencies
(pygame / moderngl); it operates purely on the blueprint dataclass tree.
"""
from __future__ import annotations

from collections import deque
from typing import Iterable

from ..blueprint import Blueprint
from ..parts.interactive import Button, LogicGate, Sensor, Switch, Timer

# Logic gate mode codes, matching ``LogicGateController``.
_AND, _OR, _XOR, _NAND, _NOR, _XNOR = range(6)

# Scrap Mechanic logic tick rate.
TICKS_PER_SECOND = 40


class MutualGateConnectionError(ValueError):
    """Raised when two distinct logic gates are wired into each other."""


def _resolve_id(ref) -> int:
    """Return the integer id from an ``ID`` instance or a raw int."""
    return ref.id if hasattr(ref, "id") else int(ref)


class Simulator:
    """Synchronous 40Hz logic simulator.

    Parameters
    ----------
    bp:
        The blueprint to simulate. Parts are discovered by walking
        ``bp.all_parts()``.
    validate:
        If ``True`` (default), refuse to simulate blueprints containing
        mutual gate connections (Scrap Mechanic disallows them). Set to
        ``False`` to bypass the check; the simulator will still run but the
        outputs are not what the game would produce.
    """

    def __init__(self, bp: Blueprint, *, validate: bool = True):
        self.bp = bp

        # cid -> part instance
        self._parts: dict[int, object] = {}
        # cid -> current active state
        self._state: dict[int, bool] = {}
        # cid -> next-state buffer (reused each tick to avoid allocation)
        self._next: dict[int, bool] = {}
        # cid -> list of upstream cids feeding into this part
        self._inputs: dict[int, list[int]] = {}
        # cid -> deque of length=delay holding past inputs (timers only)
        self._timer_queues: dict[int, deque[bool]] = {}
        # cids whose state is held manually via set() and not auto-evaluated
        self._pinned: set[int] = set()
        self._tick_count = 0

        self._build()
        if validate:
            self._validate_no_mutual_gate_connections()

    # ------------------------------------------------------------------ build

    def _build(self) -> None:
        for part in self.bp.all_parts():
            controller = getattr(part, "controller", None)
            if controller is None:
                continue
            cid = getattr(controller, "id", None)
            if cid is None:
                continue
            self._parts[cid] = part
            self._inputs[cid] = []
            self._state[cid] = bool(getattr(controller, "active", False))

        # Reverse adjacency: A.controller.controllers lists A's outputs.
        for cid, part in self._parts.items():
            for ref in (part.controller.controllers or ()):
                target = _resolve_id(ref)
                if target in self._inputs:
                    self._inputs[target].append(cid)

        for cid, part in self._parts.items():
            if isinstance(part, Timer):
                delay_ticks = (
                    part.controller.seconds * TICKS_PER_SECOND
                    + part.controller.ticks
                )
                # A delay of 0 still uses a length-1 buffer so the timer has
                # the same one-tick propagation behavior as a logic gate.
                length = max(1, delay_ticks)
                seed = bool(getattr(part.controller, "active", False))
                self._timer_queues[cid] = deque([seed] * length, maxlen=length)

    def _validate_no_mutual_gate_connections(self) -> None:
        for cid, part in self._parts.items():
            if not isinstance(part, LogicGate):
                continue
            outs = part.controller.controllers or ()
            for ref in outs:
                target_id = _resolve_id(ref)
                if target_id == cid:
                    continue  # self-loop is allowed
                target = self._parts.get(target_id)
                if not isinstance(target, LogicGate):
                    continue
                target_outs = target.controller.controllers or ()
                if any(_resolve_id(t) == cid for t in target_outs):
                    raise MutualGateConnectionError(
                        f"Mutual logic-gate connection between gate id={cid} "
                        f"and gate id={target_id}. Scrap Mechanic does not "
                        f"allow two distinct logic gates wired into each "
                        f"other; self-loops (gate -> itself) are fine."
                    )

    # --------------------------------------------------------------- public API

    @property
    def tick_count(self) -> int:
        """Number of ticks simulated so far."""
        return self._tick_count

    def set(self, part, value: bool) -> None:
        """Pin a part's output state to ``value`` and stop auto-evaluating it.

        Use for any part you want to drive externally — Buttons, Switches,
        Sensors, but also gates if you're hand-stepping a sub-circuit.
        """
        cid = part.controller.id
        if cid not in self._state:
            raise KeyError(f"part with controller id {cid} is not in this blueprint")
        self._state[cid] = bool(value)
        self._pinned.add(cid)

    def unpin(self, part) -> None:
        """Resume auto-evaluating ``part`` after a previous :meth:`set`."""
        self._pinned.discard(part.controller.id)

    def get(self, part) -> bool:
        """Return the current active state of ``part`` (after the last tick)."""
        return self._state[part.controller.id]

    def press(self, part, hold_ticks: int = 1) -> None:
        """Pulse ``part`` ON for ``hold_ticks`` ticks, then release to OFF.

        Convenience for Button / Switch interactions: drives the part true,
        advances the simulation, then drives it false. The part is left in
        the pinned state so it stays OFF until you :meth:`set` it again.
        """
        if hold_ticks < 1:
            raise ValueError("hold_ticks must be >= 1")
        self.set(part, True)
        self.tick(hold_ticks)
        self.set(part, False)

    def tick(self, n: int = 1) -> None:
        """Advance the simulation by ``n`` ticks (default 1)."""
        for _ in range(n):
            self._step()

    def run(self, *, ticks: int = 0, seconds: float = 0.0) -> None:
        """Advance ``ticks + seconds*40`` ticks total."""
        total = ticks + int(round(seconds * TICKS_PER_SECOND))
        self.tick(total)

    def state(self) -> dict[int, bool]:
        """Snapshot of every part's current active state, keyed by controller id."""
        return dict(self._state)

    def inputs_of(self, part) -> list[bool]:
        """Return the current active states of all parts feeding into ``part``."""
        cid = part.controller.id
        return [self._state[i] for i in self._inputs[cid]]

    # ------------------------------------------------------------------ step

    def _step(self) -> None:
        state = self._state
        nxt = self._next
        inputs_map = self._inputs
        pinned = self._pinned
        timer_queues = self._timer_queues

        # Phase 1: compute next state from CURRENT state. We never read from
        # nxt during this phase, so the update is fully synchronous.
        for cid, part in self._parts.items():
            if cid in pinned:
                nxt[cid] = state[cid]
                continue

            if isinstance(part, LogicGate):
                ins = inputs_map[cid]
                if not ins:
                    # Unconnected gate: hold its current state.
                    nxt[cid] = state[cid]
                else:
                    nxt[cid] = _eval_gate(part.controller.mode, ins, state)
                continue

            if isinstance(part, Timer):
                q = timer_queues[cid]
                input_val = any(state[i] for i in inputs_map[cid])
                # Push first so the queue holds the most recent `delay` inputs.
                # Then read the oldest of those — i.e. the input from `delay`
                # ticks ago — so total propagation delay equals the queue's
                # configured length (one tick for a length-1 queue, matching
                # a normal logic gate).
                q.append(input_val)  # maxlen evicts the front automatically
                nxt[cid] = q[0]
                continue

            if isinstance(part, (Switch, Button, Sensor)):
                # External input parts default to "hold" — the only way they
                # change is through .set(). This matches game semantics where
                # a switch's state isn't driven by other gates.
                nxt[cid] = state[cid]
                continue

            # Passive sinks (lights, engines, pistons, ...): their "active"
            # output is the OR of incoming signals, mirroring how the game
            # turns a connected light on when any wire is hot.
            ins = inputs_map[cid]
            if ins:
                nxt[cid] = any(state[i] for i in ins)
            else:
                nxt[cid] = state[cid]

        # Phase 2: commit.
        state.update(nxt)
        self._tick_count += 1


def _eval_gate(mode: int, input_cids: Iterable[int], state: dict[int, bool]) -> bool:
    """Evaluate a logic-gate mode against the given input ids' active states."""
    n = 0
    n_true = 0
    for i in input_cids:
        n += 1
        if state[i]:
            n_true += 1
    if mode == _AND:
        return n_true == n
    if mode == _OR:
        return n_true > 0
    if mode == _XOR:
        return n_true % 2 == 1
    if mode == _NAND:
        return n_true != n
    if mode == _NOR:
        return n_true == 0
    if mode == _XNOR:
        return n_true % 2 == 0
    return False
