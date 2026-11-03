"""XOR ROM: compile any lookup table into the fewest logic gates for a chosen speed.

    rom = xor_rom(bp, [3, 1, 4, 1, 5, 9, 2, 6])          # address -> value, answers in 2 ticks
    rom = xor_rom(bp, lambda x: (x & 15) * (x >> 4), address_bits=8, max_ticks=3)
    connect(my_switches, rom.address); connect(rom.data, my_lamps)
    xor_rom_options(data, max_ticks=6)                   # {2: 121, 3: 91, 4: ...} gates per speed

How it works. Every output bit is an XOR of product terms of the address bits, e.g.
    out0 = a0 ^ (a1 & ~a2) ^ (~a0 & ~a1 & a3)
Gates take any number of inputs, so a term is ONE gate (AND of plain bits, NOR of inverted bits)
shared by every output bit that uses it, and an output bit is ONE XOR gate. Single-bit terms and
constants need no gate. The terms are searched for (EXORCISM-style: merge and rewrite pairs of terms
without changing the function, keeping whatever needs the fewest gates).

Speed vs size (ticks from the address changing to the data being right):
  2 ticks  AND/NOR terms straight off the address, one XOR per output bit.
  3 ticks  adds a first layer of XOR/XNOR gates: inverted bits and XOR'd address combinations.
           Often far smaller (popcount of 8 bits: 103 -> 27 gates).
  4+ ticks also tries splitting the table into two chained ROMs: a small one that squeezes some
           address bits into fewer bits, feeding a second one (Curtis decomposition). Helps tables
           with structure; tables of random data hardly shrink at any speed.
"""
import itertools
import random
from typing import Callable, NamedTuple, Sequence

import numpy as np

from ..blueprint import Blueprint
from ..parts import LogicGate
from ..pos import *

__all__ = ["xor_rom", "xor_rom_options", "XorRom"]

AND, OR, XOR, NOR, XNOR = "and", "or", "xor", "nor", "xnor"
COLORS = {"address": "E8C547", "transform": "3FA7D6", "inverter": "8A8F98", "term": "222222", "data": "DF7F01"}


class XorRom(NamedTuple):
    address: list        # address input gates, least significant bit first
    data: list           # data output gates, least significant bit first
    gates: int           # gates used, not counting the address inputs
    ticks: int           # worst case from the address changing to the data being right


# ---------------------------------------------------------------------------- terms
# A term ("cube") is (plain_mask, inverted_mask). Two terms that differ at one bit i only XOR to one
# term: x ^ ~x = 1, x ^ 1 = ~x, ~x ^ 1 = x. States per bit: 1 plain, 0 inverted, 2 absent -> 3 - a - b.

def _pc(x):
    return bin(x).count("1")


def _state(c, i):
    return 1 if c[0] >> i & 1 else 0 if c[1] >> i & 1 else 2


def _with_state(c, i, s):
    p, n = c[0] & ~(1 << i), c[1] & ~(1 << i)
    return (p | 1 << i, n) if s == 1 else (p, n | 1 << i) if s == 0 else (p, n)


def _diff(a, b):
    return (a[0] ^ b[0]) | (a[1] ^ b[1])


def _xor_in(cubes, c, om):
    om ^= cubes.pop(c, 0)
    if om:
        cubes[c] = om


def _cost(cubes, out_bits, pure, penalty=10_000):
    """Gates for this set of terms. pure (2-tick) charges `penalty` per term mixing plain and inverted
    bits; the default makes them forbidden."""
    terms = inv = mixed = 0
    for p, n in cubes:
        if _pc(p | n) >= 2:
            terms += 1
            if p and n:
                inv |= n
                mixed += 1
    return terms + _pc(inv) + out_bits + (penalty * mixed if pure else 0)


def _anf(bits):
    """Moebius transform: truth table of one output bit -> Reed-Muller coefficients."""
    a = bits.astype(np.uint8).copy()
    for i in range(a.size.bit_length() - 1):
        a = a.reshape(-1, 2 << i)
        a[:, 1 << i:] ^= a[:, :1 << i]
    return a.reshape(-1)


def _reed_muller(table, n, m, pol):
    """Fixed polarity form: bit i of pol set = address bit i inverted in every term."""
    vals = np.asarray(table, dtype=np.int64)[np.arange(1 << n) ^ pol]
    cubes = {}
    for b in range(m):
        for t in np.nonzero(_anf((vals >> b) & 1))[0].tolist():
            _xor_in(cubes, (t & ~pol, t & pol), 1 << b)
    return cubes


def _lookup(table, n):
    full = (1 << n) - 1
    return {(v, full & ~v): int(table[v]) for v in range(1 << n) if table[v]}


def _merge_all(cubes, todo):
    while todo:
        a = todo.pop()
        om = cubes.get(a)
        if om is None:
            continue
        for b, om_b in list(cubes.items()):
            if b != a and om_b == om:
                d = _diff(a, b)
                if d & (d - 1) == 0:
                    i = d.bit_length() - 1
                    merged = _with_state(a, i, 3 - _state(a, i) - _state(b, i))
                    del cubes[a], cubes[b]
                    _xor_in(cubes, merged, om)
                    if merged in cubes:
                        todo.append(merged)
                    break


SOFT_PENALTY = 2   # for 2-tick ROMs the search may pass through mixed terms at this price per term


def _minimize(start, m, steps, rng, pure):
    cubes = dict(start)
    _merge_all(cubes, list(cubes))
    cur = _cost(cubes, m, pure, SOFT_PENALTY)
    best, best_cost = dict(cubes), _cost(cubes, m, pure)
    temp, idle = 1.0, 0
    for _ in range(steps):
        if len(cubes) <= 1 or idle > 2000:
            break
        keys = list(cubes)
        a = rng.choice(keys)
        om = cubes[a]
        # partners at distance 2, counting "which outputs" as one more variable: two input bits
        # apart with the same outputs, or one input bit apart with different outputs
        partners = [b for b in keys if b != a and _pc(_diff(a, b)) == (2 if cubes[b] == om else 1)]
        if not partners:
            idle += 1
            continue
        idle = 0
        b = rng.choice(partners)
        om_b = cubes[b]
        d = _diff(a, b)
        i = d.bit_length() - 1
        ai, bi = _state(a, i), _state(b, i)
        # exorlink: a_i a_j ^ b_i b_j = (a_i ^ b_i) a_j ^ b_i (a_j ^ b_j), or its mirror image.
        # With the outputs as variable j, a_j ^ b_j is the symmetric difference of the output sets.
        if om_b == om:
            j = (d & ~(1 << i)).bit_length() - 1
            aj, bj = _state(a, j), _state(b, j)
            if rng.random() < 0.5:
                new = [(_with_state(a, i, 3 - ai - bi), om), (_with_state(b, j, 3 - aj - bj), om)]
            else:
                new = [(_with_state(a, j, 3 - aj - bj), om), (_with_state(b, i, 3 - ai - bi), om)]
        elif rng.random() < 0.5:
            new = [(_with_state(a, i, 3 - ai - bi), om), (b, om ^ om_b)]
        else:
            new = [(a, om ^ om_b), (_with_state(a, i, 3 - ai - bi), om_b)]
        trial = dict(cubes)
        del trial[a], trial[b]
        for c, o in new:
            _xor_in(trial, c, o)
        _merge_all(trial, [c for c, _ in new])
        new = _cost(trial, m, pure, SOFT_PENALTY)
        if new <= cur or rng.random() < 0.05 * temp:     # sideways moves, and rarely a worse one
            cubes, cur = trial, new
            real = _cost(cubes, m, pure)                  # only a fully valid result can be kept
            if real < best_cost:
                best, best_cost = dict(cubes), real
        temp *= 0.9995
    return best


def _purify(cubes):
    """Rewrite terms that mix plain and inverted bits into terms that don't, for 2-tick ROMs.
    ~y = 1 ^ y turns x.~y into x ^ x.y (all plain); x = 1 ^ ~x turns it into ~y ^ ~x.~y (all
    inverted). Each uses 2^k terms for k flipped bits, so flip whichever side is smaller."""
    out = {}
    for (p, n), om in cubes.items():
        if not (p and n and _pc(p | n) >= 2):
            _xor_in(out, (p, n), om)
            continue
        flip, keep_plain = (n, True) if _pc(n) <= _pc(p) else (p, False)
        bits = [i for i in range(flip.bit_length()) if flip >> i & 1]
        for k in range(1 << len(bits)):
            sub = sum(1 << b for i, b in enumerate(bits) if k >> i & 1)
            _xor_in(out, (p | sub, 0) if keep_plain else (0, n | sub), om)
    _merge_all(out, list(out))
    return out


def _pure_greedy(table, n, m, passes=6):
    """2-tick terms are ANDs (plain bits) and NORs (inverted bits). NOR(S) = XOR of AND(T) over all
    T inside S, so starting from the all-AND form, toggling NOR(S) into an output flips every AND(T)
    with T inside S. Greedily toggle the NORs that save gates, counting gates shared across outputs."""
    vals = np.asarray(table, dtype=np.int64)
    pos = [set(np.nonzero(_anf((vals >> b) & 1))[0].tolist()) for b in range(m)]
    neg = [set() for _ in range(m)]
    pos_use, neg_use = {}, {}
    for b in range(m):
        for t in pos[b]:
            pos_use[t] = pos_use.get(t, 0) + 1
    subsets = {}

    def subs(S):
        if S not in subsets:
            out, t = [], S
            while True:
                out.append(t)
                if t == 0:
                    break
                t = (t - 1) & S
            subsets[S] = out
        return subsets[S]

    def delta(b, S):
        d = 0
        for t in subs(S):
            if _pc(t) >= 2:
                c = pos_use.get(t, 0)
                d += (-1 if c == 1 else 0) if t in pos[b] else (1 if c == 0 else 0)
        c = neg_use.get(S, 0)
        d += (-1 if c == 1 else 0) if S in neg[b] else (1 if c == 0 else 0)
        return d

    def toggle(b, S):
        for t in subs(S):
            if t in pos[b]:
                pos[b].remove(t); pos_use[t] -= 1
            else:
                pos[b].add(t); pos_use[t] = pos_use.get(t, 0) + 1
        if S in neg[b]:
            neg[b].remove(S); neg_use[S] -= 1
        else:
            neg[b].add(S); neg_use[S] = neg_use.get(S, 0) + 1

    candidates = sorted({t for b in range(m) for t in pos[b] if _pc(t) >= 2}, key=_pc, reverse=True)
    for _ in range(passes):
        improved = False
        for S in candidates:
            for b in range(m):
                if delta(b, S) < 0:
                    toggle(b, S)
                    improved = True
        if not improved:
            break
    cubes = {}
    for b in range(m):
        for t in pos[b]:
            _xor_in(cubes, (t, 0), 1 << b)
        for S in neg[b]:
            _xor_in(cubes, (0, S), 1 << b)
    return cubes


def _transform(table, n, rows):
    """Table re-indexed by y, where y_i = parity(x & rows[i])."""
    x = np.arange(1 << n)
    y = np.zeros_like(x)
    for i, r in enumerate(rows):
        par = x & r
        for s in (1, 2, 4, 8, 16):
            par ^= par >> s
        y |= (par & 1) << i
    out = np.empty(1 << n, dtype=np.int64)
    out[y] = np.asarray(table, dtype=np.int64)
    return out


def _rm_cost(table, n, m, pol):
    return _cost(_reed_muller(table, n, m, pol), m, False)


def _search_rows(table, n, m, steps, rng):
    """Hill-climb over invertible XOR re-codings of the address (row ops y_i ^= y_j)."""
    full = (1 << n) - 1
    cost = lambda rows: (min(_rm_cost(_transform(table, n, rows), n, m, p) for p in (0, full))
                         + sum(_pc(r) >= 2 for r in rows))
    rows = tuple(1 << i for i in range(n))
    cur = cost(rows)
    best, best_cost = rows, cur
    for _ in range(steps if n > 1 else 0):
        i, j = rng.sample(range(n), 2)
        trial = list(rows)
        trial[i] ^= rows[j]
        trial = tuple(trial)
        c = cost(trial)
        if c <= cur or rng.random() < 0.02:
            rows, cur = trial, c
            if c < best_cost:
                best, best_cost = rows, c
    return best


class _Leaf(NamedTuple):
    n: int
    m: int
    cubes: dict
    rows: tuple | None       # XOR re-coding of the address, or None

    @property
    def gates(self):
        return _cost(self.cubes, self.m, False) + (sum(_pc(r) >= 2 for r in self.rows) if self.rows else 0)

    @property
    def ticks(self):
        mixed = any(p and n and _pc(p | n) >= 2 for p, n in self.cubes)
        return 2 + (1 if mixed or (self.rows and any(_pc(r) >= 2 for r in self.rows)) else 0)


class _Split(NamedTuple):
    bound: list              # address bits the first ROM squeezes
    free: list               # address bits passed straight to the second ROM
    first: object            # plan for bound bits -> code
    second: object           # plan for (code, free bits) -> data

    @property
    def gates(self):
        return self.first.gates + self.second.gates

    @property
    def ticks(self):
        return self.first.ticks + self.second.ticks


STEPS_PER_EFFORT = 1500      # term rewrites per unit of effort; the row search gets a fifth of that


def _leaf(table, n, m, ticks, effort, rng):
    """Best single-stage plan answering within `ticks` (2 or 3)."""
    full = (1 << n) - 1
    pure = ticks == 2

    def esop(tab, rows):
        # 2-tick ROMs start from the same places; the search passes through mixed terms and keeps
        # only results without them
        pols = range(1 << n) if n <= 8 else [0, full] + [rng.randrange(1 << n) for _ in range(64)]
        ranked = sorted(pols, key=lambda p: _rm_cost(tab, n, m, p))[:3]
        extra = [p for p in (0, full) if pure and p not in ranked]
        starts = [_reed_muller(tab, n, m, p) for p in ranked + extra] + [_lookup(tab, n)]
        if pure:
            starts.append(_pure_greedy(tab, n, m))
            # the same from the all-NOR side: run it on the table with every address bit flipped,
            # where ANDs and NORs trade places
            flipped = _pure_greedy(np.asarray(tab)[np.arange(1 << n) ^ full], n, m)
            starts.append({(q, p): om for (p, q), om in flipped.items()})
            # also start from the best unrestricted result, rewritten without mixed terms
            free = _minimize(min(starts, key=lambda c: _cost(c, m, False)), m,
                             int(STEPS_PER_EFFORT * effort * 0.3), rng, False)
            starts.append(_purify(free))
        steps = int(STEPS_PER_EFFORT * effort * (1.0 if pure else 0.4) / len(starts))
        found = starts + [_minimize(s, m, steps, rng, pure) for s in starts]
        return _Leaf(n, m, min(found, key=lambda c: _cost(c, m, pure)), rows)

    plain = esop(table, None)
    if pure:
        return plain
    rows = _search_rows(table, n, m, int(STEPS_PER_EFFORT * effort * 0.2), rng)
    if all(_pc(r) == 1 for r in rows):
        return plain
    return min(plain, esop(_transform(table, n, rows), rows), key=lambda p: p.gates)


def _splits(table, n, m, rng, limit):
    """Candidate decompositions f(x) = second(first(x_bound), x_free), cheapest-looking first."""
    full = (1 << n) - 1
    masks = set()
    for k in range(2, n):
        if n <= 8:
            masks.update(sum(1 << i for i in c) for c in itertools.combinations(range(n), k))
        else:
            masks.update(sum(1 << i for i in rng.sample(range(n), k)) for _ in range(12))
    out = []
    for mask in masks:
        bound = [i for i in range(n) if mask >> i & 1]
        free = [i for i in range(n) if not mask >> i & 1]
        k, f = len(bound), len(free)
        classes, code_of = {}, []
        for a in range(1 << k):
            base = sum(1 << bound[i] for i in range(k) if a >> i & 1)
            col = tuple(table[base | sum(1 << free[i] for i in range(f) if b >> i & 1)] for b in range(1 << f))
            code_of.append(classes.setdefault(col, len(classes)))
        c = max(1, (len(classes) - 1).bit_length())
        if c >= k:
            continue
        cols = list(classes)
        # second table, addressed by (code in the low bits, free bits above); unused codes repeat class 0
        second = [cols[code if code < len(cols) else 0][b] for b in range(1 << f) for code in range(1 << c)]
        first = code_of
        guess = (min(_rm_cost(first, k, c, p) for p in (0, (1 << k) - 1))
                 + min(_rm_cost(second, c + f, m, p) for p in (0, (1 << (c + f)) - 1)))
        out.append((guess, bound, free, first, c, second))
    out.sort(key=lambda t: t[0])
    return out[:limit]


def _plan(table, n, m, max_ticks, effort, rng):
    """Smallest plan whose worst-case delay is at most max_ticks. Deterministic for a given rng, and
    the searches for fewer ticks run first and unchanged, so allowing more ticks never costs gates."""
    best = _leaf(table, n, m, 2, effort * 0.5, rng)
    if max_ticks >= 3:
        best = min(best, _leaf(table, n, m, 3, effort, rng), key=lambda p: p.gates)
    if max_ticks >= 4 and n >= 3:
        candidates = _splits(table, n, m, rng, limit=4)
        each = effort * 0.5 / max(1, len(candidates))
        for _, bound, free, first, c, second in candidates:
            for t1 in (2, 3):
                if max_ticks - t1 < 2:
                    continue
                p1 = _plan(first, len(bound), c, t1, each / 2, rng)
                p2 = _plan(second, c + len(free), m, max_ticks - t1, each / 2, rng)
                split = _Split(bound, free, p1, p2)
                if split.gates < best.gates:
                    best = split
    return best


# ---------------------------------------------------------------------------- building

class _Layout:
    """Hands out non-overlapping rows of cells, one band per stage."""

    def __init__(self, pos, width):
        self.pos, self.width, self.y = pos, width, 1

    def row(self, count):
        y0 = self.y
        self.y += max(1, -(-count // self.width))
        return [self.pos + (k % self.width, y0 + k // self.width, 0) for k in range(count)]


def _build(bp, plan, sources, layout):
    """Gates for `plan` fed by `sources` (one gate per address bit). Returns the output gates."""
    if isinstance(plan, _Split):
        code = _build(bp, plan.first, [sources[i] for i in plan.bound], layout)
        return _build(bp, plan.second, code + [sources[i] for i in plan.free], layout)

    n, m, cubes = plan.n, plan.m, plan.cubes
    rows = plan.rows or tuple(1 << i for i in range(n))
    made = []

    def gate(cell, mode, color, inputs):
        g = LogicGate(cell, color, mode)
        for s in inputs:
            s.connect(g)
        made.append(g)
        return g

    srcs = lambda mask: [sources[i] for i in range(n) if mask >> i & 1]
    recoded = [r for r in rows if _pc(r) >= 2]
    cells = iter(layout.row(len(recoded)))
    y = [sources[r.bit_length() - 1] if _pc(r) == 1 else gate(next(cells), XOR, COLORS["transform"], srcs(r))
         for r in rows]

    inv_mask = 0
    for p, q in cubes:
        if p and q and _pc(p | q) >= 2:
            inv_mask |= q
    inv_bits = [i for i in range(n) if inv_mask >> i & 1]
    cells = iter(layout.row(len(inv_bits)))
    # an inverted y_i in one tick: NOR of a plain address bit, or XNOR of the bits y_i XORs
    inv = {i: gate(next(cells), NOR if _pc(rows[i]) == 1 else XNOR, COLORS["inverter"], srcs(rows[i]))
           for i in inv_bits}

    terms = sorted(c for c in cubes if _pc(c[0] | c[1]) >= 2)
    cells = iter(layout.row(len(terms)))
    term_gate = {}
    for p, q in terms:
        if p and q:
            term_gate[p, q] = gate(next(cells), AND, COLORS["term"],
                                   [y[i] for i in range(n) if p >> i & 1] + [inv[i] for i in range(n) if q >> i & 1])
        elif p:
            term_gate[p, q] = gate(next(cells), AND, COLORS["term"], [y[i] for i in range(n) if p >> i & 1])
        else:   # only inverted bits: one NOR of the plain ones
            term_gate[p, q] = gate(next(cells), NOR, COLORS["term"], [y[i] for i in range(n) if q >> i & 1])

    cells = iter(layout.row(m + 1))
    outputs, not_y0 = [], None
    for b in range(m):
        feeds, invert = [], False
        for (p, q), om in cubes.items():
            if not om >> b & 1:
                continue
            if (p, q) in term_gate:
                feeds.append(term_gate[p, q])
            elif p or q:
                feeds.append(y[(p | q).bit_length() - 1])
                invert ^= bool(q)        # a lone inverted bit: the plain bit, output flipped
            else:
                invert = not invert      # constant 1
        # a source fed twice (x and ~x both as lone bits) cancels out in an XOR; the game also
        # refuses a second wire between the same two parts
        counts = {}
        for f in feeds:
            counts[id(f)] = (counts.get(id(f), (f, 0))[0], counts.get(id(f), (f, 0))[1] + 1)
        feeds = [f for f, c in counts.values() if c % 2]
        if invert and not feeds:
            # constant 1: a gate with no inputs is off, so OR a bit with its own inverse
            if not_y0 is None:
                not_y0 = gate(next(cells), NOR, COLORS["inverter"], [sources[0]])
            outputs.append(gate(next(cells), OR, COLORS["data"], [sources[0], not_y0]))
        else:
            outputs.append(gate(next(cells), XNOR if invert else XOR, COLORS["data"], feeds))
    bp.add(made)
    return outputs


def _table(data, address_bits, data_bits):
    if callable(data):
        if address_bits is None:
            raise ValueError("give address_bits when data is a function")
        table = [int(data(x)) for x in range(1 << address_bits)]
    else:
        table = [int(v) for v in data]
        if address_bits is None:
            address_bits = max(1, (len(table) - 1).bit_length())
        if len(table) > 1 << address_bits:
            raise ValueError(f"{len(table)} values don't fit {address_bits} address bits")
        table += [0] * ((1 << address_bits) - len(table))
    if any(v < 0 for v in table):
        raise ValueError("values must be 0 or more")
    if data_bits is None:
        data_bits = max(1, max(table).bit_length())
    if address_bits > 12:
        raise ValueError(f"{address_bits} address bits is {1 << address_bits} rows; split the table or compute it")
    mask = (1 << data_bits) - 1
    return [v & mask for v in table], address_bits, data_bits


def xor_rom(bp: Blueprint,
            data: Sequence[int] | Callable[[int], int],
            address_bits: int | None = None,
            data_bits: int | None = None,
            pos: Pos | Sequence = (0, 0, 0),
            max_ticks: int = 2,
            effort: float = 1.0,
            seed: int = 0) -> XorRom:
    """Build a ROM that outputs data[address], using as few gates as it can find.

    Args:
        bp: the blueprint to add the gates to.
        data: the values, one per address (padded with 0), or a function of the address.
        address_bits: address width; defaults to what len(data) needs. Required for a function.
            Several inputs? Pack them: lambda x: (x & 15) * (x >> 4) is a 4x4-bit multiplier.
        data_bits: output width; defaults to what the largest value needs.
        pos: where the address inputs go; the ROM grows from there in +y.
        max_ticks: slowest allowed answer, from the address changing (2 or more). More ticks
            let it use fewer gates; see xor_rom_options().
        effort: how hard to search (1 takes a second or two for 8 address bits); more can find a
            smaller ROM. The same data, effort and seed always give the same ROM.
        seed: pick another seed to try a different search.

    Returns:
        XorRom(address, data, gates, ticks). Connect your inputs to rom.address and read rom.data,
        both least significant bit first.
    """
    if max_ticks < 2:
        raise ValueError("a ROM needs at least 2 ticks: one for the terms, one for the outputs")
    table, n, m = _table(data, address_bits, data_bits)
    pos = check_pos(pos)
    plan = _plan(table, n, m, max_ticks, effort, random.Random(seed))
    address = [LogicGate(pos + (i, 0, 0), COLORS["address"], OR) for i in range(n)]
    bp.add(address)
    outputs = _build(bp, plan, address, _Layout(pos, max(n, m, 1)))
    return XorRom(address, outputs, plan.gates, plan.ticks)


def xor_rom_options(data: Sequence[int] | Callable[[int], int],
                    address_bits: int | None = None,
                    data_bits: int | None = None,
                    max_ticks: int = 6,
                    effort: float = 1.0,
                    seed: int = 0) -> dict[int, int]:
    """Gate count for each speed from 2 to max_ticks, without building anything.

    Returns {ticks: gates}. A speed only shows a smaller number when it actually saves gates.
    """
    table, n, m = _table(data, address_bits, data_bits)
    options, best = {}, None
    for t in range(2, max_ticks + 1):
        plan = _plan(table, n, m, t, effort, random.Random(seed))
        best = plan.gates if best is None else min(best, plan.gates)
        options[t] = best
    return options
