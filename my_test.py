from random import randint

from numpy import array
from src.sm_blueprint_lib import *


bp = Blueprint()


class Thread:
    def __init__(self, axis, initial, dir, bp=bp):
        self.axis = axis
        self.prev = initial
        self.dir = dir
        self.bp = bp
        self.bp.add(self.prev)

    def node(self, mode="and", _from=None, _to=None, chain=True, pos=None):
        if isinstance(mode, str):
            g = LogicGate(self.prev.pos + self.dir if chain else pos,
                          f"{"FF" if _from is not None else "00"}00{"FF" if _to is not None else "00"}",
                          mode,
                          **self.axis)
        else:
            g = Timer(self.prev.pos + self.dir if chain else pos,
                      f"{"FF" if _from is not None else "00"}00{"FF" if _to is not None else "00"}",
                      divmod(mode-1, TICKS_PER_SECOND),
                      **self.axis)
        if _from is not None:
            connect(_from, g)
        if _to is not None:
            connect(g, _to)
        if chain:
            connect(self.prev, g)
            self.prev = g
        self.bp.add(g)
        return g


code = Thread({"xaxis": 3, "zaxis": -1},
               LogicGate((-2, 2, 0), "FF0000", 1, xaxis=3, zaxis=-1),
               (0, 0, 1))

ADDR_SIZE = 16
START_ADDR = 0x1000
NUM_REGISTERS = 8


def mask(array, mask: int, bit_length=ADDR_SIZE):
    return array[num_to_bit_list(mask, bit_length)]


internal_bus = array([LogicGate((x, 0, 0), "FF00FF", 1)
                      for x in range(ADDR_SIZE)], dtype=LogicGate)


PC = counter_register(bp, ADDR_SIZE, with_decrement=False,
                      pos=(2+ADDR_SIZE, 2, 0))


def reg_write(reg):
    return reg[1]


def reg_read(reg):
    return reg[2]


def reg_din(reg):
    return reg[0][:, -1]


def reg_dout(reg):
    return reg[0][:, 0]


PC_write = reg_write(PC[0])
PC_read = reg_read(PC[0])

connect(internal_bus, reg_din(PC[0]))
connect(reg_dout(PC[0]), internal_bus)

registers = [
    register(bp, ADDR_SIZE, pos=(2+ADDR_SIZE, 10+5*y, 0))
    for y in range(NUM_REGISTERS)
]
for r in registers:
    connect(reg_dout(r), internal_bus)
    connect(internal_bus, reg_din(r))


adder = simple_adder_subtractor(bp, ADDR_SIZE, (-2-ADDR_SIZE, 10, 0))
reg_adder_a = register(bp, ADDR_SIZE, OE=False, pos=(-2-ADDR_SIZE, 12, 2))
reg_adder_b = register(bp, ADDR_SIZE, OE=False, pos=(-2-ADDR_SIZE, 12, 0))
adder_out = [LogicGate((-2-ADDR_SIZE+x, 7, 0), "0000FF")
             for x in range(ADDR_SIZE)]
adder_out_enable = LogicGate((-3-ADDR_SIZE, 7, 0), "FF0000", 1)
adder_mode_select = [LogicGate((-3-ADDR_SIZE, 9, 0), "0000FF", 2),
                     LogicGate((-3-ADDR_SIZE, 10, 0), "000000", 0),
                     LogicGate((-3-ADDR_SIZE, 11, 0), "FF0000", 2),
                     LogicGate((-4-ADDR_SIZE, 10, 0), "FF0000", 1)]
adder_mode_select[2].connect(adder_mode_select[1]).connect(
    adder_mode_select[0]).connect(adder_mode_select[0]).connect(adder_mode_select[2])
adder_mode_select[3].connect(adder_mode_select[1])
adder_mode_select[0].connect(adder[7])

connect(reg_dout(reg_adder_a), adder[0])
connect(reg_dout(reg_adder_b), adder[1])
connect(adder[6], adder_out)
connect(adder_out_enable, adder_out)
connect(internal_bus, reg_din(reg_adder_a))
connect(internal_bus, reg_din(reg_adder_b))
connect(adder_out, internal_bus)


reset_signal = [
    Button((-2, 3, 2), "000000"),
    LogicGate((-2, 3, 1), "000000", 3),
    LogicGate((-2, 3, 0), "000000", 0),
]
connect(reset_signal[0], reset_signal[1:])
connect(reset_signal[1], reset_signal[2])
connect(reset_signal[2], code.prev)


bp.add(internal_bus, reset_signal, adder_out,
       adder_out_enable, adder_mode_select)


def add(t, reg_a, reg_b, reg_out):
    g = t.node("or", _to=reg_read(reg_a))
    t.node(_to=reg_read(reg_b))
    t.node(_to=adder_mode_select[3])
    t.node(_to=reg_write(reg_adder_a))
    t.node(_to=reg_write(reg_adder_b))
    t.node(36, _to=adder_out_enable)
    t.node(_to=adder_mode_select[3])
    t.node()
    t.node(_to=reg_write(reg_out))
    t.node()
    return g


def sub(t, reg_a, reg_b, reg_out):
    g = t.node("or", _to=reg_read(reg_a))
    t.node(_to=reg_read(reg_b))
    t.node(_to=(adder_mode_select[3], adder_mode_select[2]))
    t.node(_to=reg_write(reg_adder_a))
    t.node(_to=reg_write(reg_adder_b))
    t.node(36, _to=adder_out_enable)
    t.node(_to=adder_mode_select[3])
    t.node()
    t.node(_to=reg_write(reg_out))
    t.node()
    return g


def move(t, reg_from, reg_to):
    g = t.node("or", _to=reg_read(reg_from))
    t.node()
    t.node()
    t.node(_to=reg_write(reg_to))
    t.node()
    return g


def set_reg(t, reg, value):
    g = t.node("or", _to=mask(internal_bus, value))
    t.node(_to=reg_write(reg))
    return g


def jump(t, g):
    return t.node("or", _to=g)


# reset
code.node(_to=mask(internal_bus, START_ADDR))
code.node(_to=PC_write)
code.node(_to=[reg_write(r) for r in registers])
code.node(_to=adder_mode_select[3])

# test program
set_reg(code, registers[0], 1)
set_reg(code, registers[1], 1)
set_reg(code, registers[2], 0)
loop = add(code, registers[0], registers[1], registers[2])
move(code, registers[1], registers[0])
move(code, registers[2], registers[1])
jump(code, loop)


print(f"Prebuild size: {len(bp.bodies[0].childs)} parts")
save_blueprint("sm lib output", bp)
