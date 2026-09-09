import shlex
from dataclasses import dataclass, field
from typing import Optional, Any
from numpy import array
import numpy as np

# Assuming you are running this from outside the src directory, or adjust imports as needed
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

bp = Blueprint()
DATA_SIZE = 8
ADDRESS_SIZE = 16
nor_ram(bp, bit_length=DATA_SIZE, num_address=32)
simple_adder_subtractor(bp, bit_length=DATA_SIZE, pos=(0, 10, 0))
nor_register(bp, bit_length=DATA_SIZE, pos=(0, 15, 0))
nor_register(bp, bit_length=DATA_SIZE, pos=(0, 20, 0))
rom(bp, page_size=(DATA_SIZE, 8), data=list(range(300)), pos=(0, 25, 0))
nor_counter_register(bp, bit_length=DATA_SIZE, pos=(0, 35, 0))
counter_register(bp, bit_length=DATA_SIZE, pos=(0, 50, 0))
save_blueprint("cpu output", bp)
