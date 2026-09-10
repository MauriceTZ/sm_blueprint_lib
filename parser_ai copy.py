import shlex
from dataclasses import dataclass, field
from typing import Optional, Any
from numpy import array
import numpy as np

from src.sm_blueprint_lib.prebuilds.rom import rom
from src.sm_blueprint_lib.prebuilds.decoder import decoder
from src.sm_blueprint_lib.constants import TICKS_PER_SECOND
from src.sm_blueprint_lib import Blueprint, LogicGate, Timer, Pos, check_pos
from src.sm_blueprint_lib.utils import connect, get_bits_required, num_to_bit_list, save_blueprint
from src.sm_blueprint_lib.prebuilds.adder import cla_1tick, simple_adder_subtractor
from src.sm_blueprint_lib.prebuilds.register import register, counter_register
from src.sm_blueprint_lib.prebuilds.ram import ram
from src.sm_blueprint_lib.prebuilds.timer_ram_multiclient import timer_ram_multiclient
from src.sm_blueprint_lib.prebuilds.screens.timer_character_screen import timer_character_screen
from src.sm_blueprint_lib.prebuilds.NOR_NOR_memory import nor_ram, nor_register, nor_counter_register

DATA_BUS_SIZE = 16
ADDRESS_BUS_SIZE = 16

bp = Blueprint()

pos = Pos(0, 0, 0)
data_bus = [LogicGate(pos + (x, 0, 0), "FF0000", 1, xaxis=-2, zaxis=-1)
            for x in range(DATA_BUS_SIZE)]
# Memory address register
mar = register(bp, bit_length=ADDRESS_BUS_SIZE, pos=(DATA_BUS_SIZE, 0, 0))
decoder(bp, num_address=ADDRESS_BUS_SIZE, pos=(DATA_BUS_SIZE, -5, 0))

bp.add(data_bus)
# nor_ram(bp, bit_length=DATA_BUS_SIZE, num_address=32)
# simple_adder_subtractor(bp, bit_length=DATA_BUS_SIZE, pos=(0, 10, 0))
# nor_register(bp, bit_length=DATA_BUS_SIZE, pos=(0, 15, 0))
# nor_register(bp, bit_length=DATA_BUS_SIZE, pos=(0, 20, 0))
# rom(bp, page_size=(DATA_BUS_SIZE, 8), data=list(range(300)), pos=(0, 25, 0))
# nor_counter_register(bp, bit_length=DATA_BUS_SIZE, pos=(0, 35, 0))
save_blueprint("cpu output", bp)
