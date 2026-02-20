import os
from random import randint
from math import sin
from typing import Sequence

from numpy import array
from src.sm_blueprint_lib import *
from src.sm_blueprint_lib.utils import _old_connect


bp = Blueprint()

midi_converter(bp, r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\arabesque_1_(c)oguri.mid")

# m = ndarray((7, 7, 3), dtype=BasePart)
# for x in range(7):
#     for y in range(7):
#         m[x, y, :] = [LogicGate((x, 2, y), "000000", 2, xaxis=3, zaxis=-1),
#                       LogicGate((x, 1, y), "000000", 0, xaxis=3, zaxis=-1),
#                       LogicGate((x, 0, y), "FF0000", 2, xaxis=3, zaxis=-1),
#                       ]
# _old_connect(m[:, :, 0], m[:, :, 0])
# _old_connect(m[:, :, 0], m[:, :, 2])
# _old_connect(m[:, :, 2], m[:, :, 1])
# _old_connect(m[:, :, 1], m[:, :, 0])

# for y in range(7):
#     if y % 2 == 0:
#         _old_connect(m[0:7, y, 0], m[1:7, y, 2])
#         _old_connect(m[0:7, y, 2], m[1:7, y, 2])
#         if y != 6:
#             _old_connect(m[6, y, 0], m[6, y+1, 2])
#             _old_connect(m[6, y, 2], m[6, y+1, 2])
#     else:
#         _old_connect(m[1:, y, 0], m[:, y, 2])
#         _old_connect(m[1:, y, 2], m[:, y, 2])
#         if y != 6:
#             _old_connect(m[0, y, 0], m[0, y+1, 2])
#             _old_connect(m[0, y, 2], m[0, y+1, 2])

# write = LogicGate((-2, 1, 0), "FF0000", 1)
# _old_connect(write, m[:, :, 1])
# bp.add(m, write)

# LFSR(bp, 32)

# timer_ram_cached(bp,
#                  bit_length=8,
#                  num_address_per_cache=8,
#                  num_caches=4,
#                  num_timer_banks=4,
#                  num_caches_per_bank=128)

# comparator(bp, bit_length=32)

# simple_adder_subtractor(bp, bit_length=8)

# ram(bp, 8, 8)

# counter_register(bp,
#                  bit_length=6,
#                  OE=True,
#                  with_increment=True,
#                  with_decrement=True)


# clock40hz(bp, 10)

# timer_ram_multiclient(bp, bit_length=32, num_address=16, num_clients=1)

# timer_ram_cached(bp,
#                  bit_length=32,
#                  num_address_per_cache=4,
#                  num_caches=4,
#                  num_timer_banks=4,
#                  num_caches_per_bank=1024)


# barrel_shifter(bp,
#                bit_length=32,
#                num_bit_shift=6)

# distance_sensor(bp,
#                 range(1, 9, 1))

# distance_sensor_raycast(bp,
#                         range(1, 21, 2))


# # Initial instructions rom
# micro_ins = [100,101,102,103,104,105,106,107,108]
# rom1 = rom(bp, pos=(-30, -30, 0),
#            page_size=(32, 8),
#            data=micro_ins)


# register(bp, pos=(15,-5,0), bit_length=24, OE=False)

# decoder(bp, pos=(30, 5, 0), num_address=16)

# ram(bp, pos=(20,5,0),
#     bit_length=8,
#     num_address=8)

# reg = register(bp, pos=(0, -10, 0), bit_length=32)
# c = counter(bp, pos=(0, -9, 1), bit_length=32,
#             precreated_swxors=reg[0][:, 1])

# l = LogicGate((0,0,0), "FFFF00", 0)
# bp.add(l)
print(f"Prebuild size: {len(bp.bodies[0].childs)} parts")
save_blueprint("sm lib output", bp)
# path = get_paths()[0]
# save_blueprint(bp, path)
# print(dump_string_from_blueprint(bp))
