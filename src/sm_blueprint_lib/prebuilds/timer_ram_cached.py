from itertools import cycle
from typing import Sequence
from numpy import append, array, clip, ndarray

from ..blocks import BarrierBlock
from ..utils import get_bits_required, _old_connect, num_to_bit_list
from ..bases.parts.baseinteractablepart import BaseInteractablePart
from ..bases.parts.baselogicpart import BaseLogicPart
from ..blueprint import Blueprint
from ..constants import TICKS_PER_SECOND
from ..parts import LogicGate
from ..parts import Timer
from ..pos import *
from ..prebuilds.clock40hz import clock40hz
from ..prebuilds.counter import counter
from ..prebuilds.decoder import decoder
from ..prebuilds.ram import ram
from ..prebuilds.register import register


def timer_ram_cached(
        bp: Blueprint,
        bit_length: int,
        num_address_per_cache: int,
        num_caches: int,
        num_timer_banks: int,
        num_caches_per_bank: int,
        pos: Pos | Sequence = (0, 0, 0)):
    total_bits = bit_length*num_address_per_cache*num_timer_banks*num_caches_per_bank
    cached_bits = bit_length*num_address_per_cache*num_caches
    cached_addresses = num_address_per_cache*num_caches
    banked_addresses = num_address_per_cache*num_timer_banks
    total_pages = num_timer_banks*num_caches_per_bank
    total_addresses = num_address_per_cache*num_timer_banks*num_caches_per_bank

    pos = check_pos(pos)

    clock = clock40hz(
        bp, get_bits_required(num_caches_per_bank), pos + (-get_bits_required(total_pages) - 4, 7, num_caches))

    cache = ram(bp,
                bit_length,
                cached_addresses,
                pos + (0, 5, 0))
    cache_arr = ndarray((bit_length, cached_addresses, 4), dtype=LogicGate)
    cache_full_page_in = ndarray(
        (bit_length, num_address_per_cache), dtype=LogicGate)
    cache_full_page_out = ndarray(
        (bit_length, num_address_per_cache), dtype=LogicGate)

    timer_bank = ndarray(
        (bit_length, banked_addresses, 5), dtype=BaseLogicPart)

    timer_bank_decoder_read = [LogicGate(
        pos + (bit_length*3, 8, z), "000000", xaxis=1, zaxis=3) for z in range(banked_addresses)]
    timer_bank_decoder_read_in = ndarray(
        (get_bits_required(num_timer_banks), 2), dtype=LogicGate)
    timer_bank_decoder_read_enable = LogicGate(
        pos + (bit_length*3, 8, -1), "FF0000", 1, xaxis=1, zaxis=3)

    timer_bank_decoder_write_keep = ndarray(
        (banked_addresses, 2), dtype=LogicGate)
    timer_bank_decoder_write_keep_in = ndarray(
        (get_bits_required(num_timer_banks), 4), dtype=LogicGate)
    timer_bank_decoder_write_keep_enable = (LogicGate(pos + (bit_length*3, 6, -1), "FF0000", 1, xaxis=1, zaxis=3),
                                            LogicGate(pos + (bit_length*3, 6, -2), "FF0000", 1, xaxis=1, zaxis=3))

    cache_pointer = counter(bp, get_bits_required(num_caches),
                            pos + (-get_bits_required(total_pages) - 4, 5, num_caches))

    # cache_table_offset_x = int(
    #     clip(get_bits_required(total_pages) - bit_length + 2, 0, None))
    cache_table = ram(bp,
                      bit_length=get_bits_required(total_pages) + 1,  # XD
                      num_address=num_caches,
                      #   pos=pos + (-cache_table_offset_x, 5, cached_addresses+2))
                      pos=pos + (-get_bits_required(total_pages) - 4, 5, 0))

    cache_table_lookup = ndarray(
        (get_bits_required(total_pages), num_caches), dtype=LogicGate)
    cache_table_lookup_in = [LogicGate(pos + (x-get_bits_required(total_pages) - 4, 4, -1),
                                       "ff0000", 1, xaxis=1, zaxis=3) for x in range(get_bits_required(total_pages))]
    cache_table_lookup_out = array([LogicGate(pos + (x-get_bits_required(total_pages) - 4, 4, -2),
                                   "0000ff", 1, xaxis=1, zaxis=3) for x in range(get_bits_required(num_caches)+1)], dtype=LogicGate)
    cache_table_lookup_dec = [LogicGate(pos + (-get_bits_required(
        total_pages) - 5, 4, z), "000000", xaxis=1, zaxis=3) for z in range(num_caches)]
    cache_table_lookup_dec_enable = LogicGate(
        pos+(-get_bits_required(total_pages) - 5, 4, -1), "ff0000", xaxis=1, zaxis=3, controller=1)
    cache_table_set_flag = ndarray((num_caches, 2), dtype=LogicGate)

    for x in range(bit_length):
        for y in range(cached_addresses):
            cache_arr[x, y, :] = [
                LogicGate(pos + (x, 3, y), "000000"),
                LogicGate(pos + (x, 4, y), "FF0000", 2),
                LogicGate(pos + (x, 5, y), "000000"),
                cache[0][x, y, 3]
            ]
        for y in range(num_address_per_cache):
            cache_full_page_in[x, y] = LogicGate(
                pos + (x, 2, y+1), "FF0000", 1, xaxis=1, zaxis=-3)
            cache_full_page_out[x, y] = LogicGate(
                pos + (x, 2, y+num_address_per_cache+1), "0000FF", 1, xaxis=1, zaxis=-3)
    for x in range(bit_length):
        for y in range(banked_addresses):
            timer_bank[x, y, :] = [
                LogicGate(pos + (x*2 + bit_length, 7, y), "FF0000"),
                LogicGate(pos + (x*2 + bit_length+1, 7, y), "0000FF"),
                LogicGate(pos + (x*2 + bit_length, 8, y), "000000"),
                LogicGate(pos + (x*2 + bit_length+1, 8, y), "000000", 1),
                Timer(pos + (x*2 + bit_length, 9, y+1), "0000FF",
                      divmod(num_caches_per_bank-3, TICKS_PER_SECOND), xaxis=-3, zaxis=-2)
            ]
    for x in range(get_bits_required(num_timer_banks)):
        timer_bank_decoder_read_in[x, :] = [
            LogicGate(pos + (bit_length*3+1, 8, x),
                      "FF0000", 4, xaxis=1, zaxis=3),
            LogicGate(pos + (bit_length*3+2, 8, x),
                      "FF0000", 1, xaxis=1, zaxis=3),
        ]
        timer_bank_decoder_write_keep_in[x, :] = [
            LogicGate(pos + (bit_length*3+2, 6, x),
                      "FF0000", 4, xaxis=1, zaxis=3),
            LogicGate(pos + (bit_length*3+3, 6, x),
                      "FF0000", 1, xaxis=1, zaxis=3),
            LogicGate(pos + (bit_length*3+4, 6, x),
                      "FF0000", 4, xaxis=1, zaxis=3),
            LogicGate(pos + (bit_length*3+5, 6, x),
                      "FF0000", 1, xaxis=1, zaxis=3),
        ]
    for z in range(banked_addresses):
        timer_bank_decoder_write_keep[z, :] = [
            LogicGate(pos + (bit_length*3, 6, z), "000000", xaxis=1, zaxis=3),
            LogicGate(pos + (bit_length*3+1, 6, z),
                      "000000", 3, xaxis=1, zaxis=3),
        ]
    for x in range(get_bits_required(total_pages)):
        for z in range(num_caches):
            cache_table_lookup[x, z] = LogicGate(
                pos + (x-get_bits_required(total_pages) - 4, 5, z+1), "000000", 5, xaxis=1, zaxis=-3)
    for y in range(num_caches):
        cache_table_set_flag[y] = [
            LogicGate(
                pos + (0-get_bits_required(total_pages) - 4, 4, y+1), "000000", 3, xaxis=1, zaxis=-3),
            LogicGate(
                pos + (1-get_bits_required(total_pages) - 4, 4, y+1), "000000", 0, xaxis=1, zaxis=-3)]

    _old_connect(timer_bank[:, :, 4], timer_bank[:, :, 2])
    _old_connect(timer_bank[:, :, 2], timer_bank[:, :, 3])
    _old_connect(timer_bank[:, :, 3], timer_bank[:, :, 4])
    _old_connect(timer_bank[:, :, 4], timer_bank[:, :, 1])
    _old_connect(timer_bank[:, :, 0], timer_bank[:, :, 3])

    decoder(bp, banked_addresses,
            precreated_outputs=timer_bank_decoder_read,
            precreated_inputs_binary=timer_bank_decoder_read_in,
            precreated_output_enable=timer_bank_decoder_read_enable,
            address_divisor=num_address_per_cache)

    decoder(bp, banked_addresses,
            precreated_outputs=timer_bank_decoder_write_keep[:, 0],
            precreated_inputs_binary=timer_bank_decoder_write_keep_in[:, :2],
            precreated_output_enable=timer_bank_decoder_write_keep_enable[0],
            address_divisor=num_address_per_cache)

    decoder(bp, banked_addresses,
            precreated_outputs=timer_bank_decoder_write_keep[:, 1],
            precreated_inputs_binary=timer_bank_decoder_write_keep_in[:, 2:],
            precreated_output_enable=timer_bank_decoder_write_keep_enable[1],
            address_divisor=num_address_per_cache)

    _old_connect(timer_bank_decoder_read, timer_bank[:, :, 1].T)
    _old_connect(timer_bank_decoder_write_keep[:, 0], timer_bank[:, :, 0].T)
    _old_connect(timer_bank_decoder_write_keep[:, 1], timer_bank[:, :, 2].T)

    for t, c in zip(timer_bank[:, :, 1].T, cycle(cache_full_page_in.T)):
        _old_connect(t, c)

    for c, t in zip(cycle(cache_full_page_out.T), timer_bank[:, :, 0].T):
        _old_connect(c, t)

    _old_connect(cache_table[0][:, :, -1], cache_table_lookup)
    # _old_connect(cache_table[0][-2, :, -1], cache_table_lookup_dec)
    _old_connect(cache_table_lookup_dec_enable, cache_table_lookup_dec)
    _old_connect(cache_table[0][-1, :, -1], cache_table_set_flag[:, 0])
    _old_connect(cache_table_set_flag[:, 1], cache_table[0][-1, :, -1])
    _old_connect(cache_table_set_flag[:, 0], cache_table_set_flag[:, 1])
    _old_connect(cache_table_lookup_dec, cache_table_set_flag[:, 1])
    # _old_connect(cache_table_lookup_dec, cache_table[0][-1, :, -1])
    _old_connect(cache_table_lookup_in, cache_table_lookup)
    _old_connect(cache_table_lookup.T, cache_table_lookup_dec)
    _old_connect(cache_table_lookup_dec, cache_table_lookup_out[-1])
    for x in range(num_caches):
        bit_mask = num_to_bit_list(
            x, get_bits_required(num_caches)+1)
        _old_connect(cache_table_lookup_dec[x], cache_table_lookup_out[bit_mask])

    cache_full_page = ram(bp,
                          bit_length=bit_length*num_address_per_cache,
                          num_address=cached_addresses,
                          pos=pos + (0, 1, 0),
                          address_divisor=num_address_per_cache,
                          pre_arr=cache_arr,
                          pre_inputs=cache_full_page_in.T.flat,
                          pre_outputs=cache_full_page_out.T.flat)

    control_pos = pos+(0, 10, -2)
    data_register = register(bp, bit_length=bit_length, pos=control_pos)
    address_register = register(
        bp, bit_length=get_bits_required(total_bits//bit_length), pos=control_pos+(bit_length+1, 0, 0))
    read_write_register = register(
        bp, bit_length=1, pos=control_pos+(bit_length+get_bits_required(total_bits//bit_length)+2, 0, 0))
    execute = LogicGate(pos=control_pos+(bit_length+get_bits_required(total_bits//bit_length)+3, 3, 0),
                        color="FF0000",
                        controller=1)
    execution_done = LogicGate(pos=control_pos+(bit_length+get_bits_required(total_bits//bit_length)+4, 3, 0),
                               color="0000FF",
                               controller=1)

    address_comparator = [
        # cache_table
        [LogicGate(pos + (-get_bits_required(total_pages) - 4 + x, 8, num_caches),
                   "000000", 5, xaxis=1, zaxis=3)
         for x in range(get_bits_required(num_caches_per_bank))],
        LogicGate(pos + (-get_bits_required(total_pages) - 4, 8, num_caches+1),
                  "000000", 0, xaxis=1, zaxis=3),
        LogicGate(pos + (-get_bits_required(total_pages) - 3, 8, num_caches+1),
                  "000000", 0, xaxis=1, zaxis=3),
    ]
    _old_connect(address_comparator[0], address_comparator[1])
    _old_connect(address_comparator[0], address_comparator[2])
    _old_connect(clock[:, 0], address_comparator[0])

    rpos = control_pos + (-get_bits_required(total_pages) - 4, 6, 0)
    routing0 = [
        [LogicGate(rpos + (x, 0, 0), "000000")  # 0
         for x in range(get_bits_required(num_caches))],

        [Timer(rpos + (x, 1, 0), "000000", (0, 0))  # 1
         for x in range(get_bits_required(total_pages))],

        [LogicGate(rpos + (x, 1, 2), "000000")  # 2
         for x in range(get_bits_required(total_pages))],

        [LogicGate(rpos + (x, 2, 0), "000000")  # 3
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos + (x, 3, 0), "000000")  # 4
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos + (x, 4, 0), "000000")  # 5
         for x in range(get_bits_required(num_caches_per_bank))],

        [LogicGate(rpos + (x, 5, 0), "000000")  # 6
         for x in range(get_bits_required(num_timer_banks))],

        [LogicGate(rpos + (x, 6, 0), "000000")  # 7
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos + (x, 7, 0), "000000")  # 8
         for x in range(get_bits_required(num_caches_per_bank))],

        [LogicGate(rpos + (x, 8, 0), "000000")  # 9
         for x in range(get_bits_required(num_timer_banks))],

        [LogicGate(rpos + (x, 9, 0), "000000")  # 10
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos + (x, 10, 0), "000000")  # 11
         for x in range(get_bits_required(total_pages))],

        [LogicGate(rpos + (x, 11, 0), "000000")  # 12
         for x in range(get_bits_required(num_caches))],
    ]
    rpos1 = rpos + (max(map(lambda p: len(p), routing0)) + 1, 0, 0)
    routing1 = [
        [LogicGate(rpos1 + (x, 0, 0), "000000")
         for x in range(get_bits_required(total_pages))],

        [Timer(rpos1 + (x, 1, 0), "000000", (0, 0))
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos1 + (x, 1, 2), "000000")
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos1 + (x, 2, 0), "000000")
         for x in range(get_bits_required(num_address_per_cache))],

        [LogicGate(rpos1 + (x, 3, 0), "000000")
         for x in range(bit_length)],
    ]
    rpos2 = rpos1 + (max(map(lambda p: len(p), routing1)) + 1, 0, 0)
    routing2 = [
        [LogicGate(rpos2 + (x, 0, 0), "000000")
         for x in range(get_bits_required(total_pages))],

        [Timer(rpos2 + (x, 1, 0), "000000", (0, 0))
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos2 + (x, 1, 2), "000000")
         for x in range(get_bits_required(num_caches))],

        [LogicGate(rpos2 + (x, 2, 0), "000000")
         for x in range(get_bits_required(num_address_per_cache))],

        [LogicGate(rpos2 + (x, 3, 0), "000000")
         for x in range(bit_length)],
    ]

    l0 = [
        LogicGate(rpos + (0, -2, 0), "000000", 1),
        LogicGate(rpos + (1, -2, 0), "000000", 3),
        LogicGate(rpos + (2, -2, 0), "000000", 0),
    ]
    _old_connect(l0[0], l0[0])
    _old_connect(l0[0], l0[1:])
    _old_connect(l0[1], l0[2])
    _old_connect(execute, l0[0])
    for y in range(num_caches):
        l = num_to_bit_list(y, get_bits_required(num_caches))
        for i, b in enumerate(l):
            if b:
                _old_connect(l0[2], cache_table[0][i, y, 3])
    rpos3 = rpos1 + (0, 5, 0)
    l1 = [
        LogicGate(rpos3 + (0, 0, 0), "000000", 3),
        LogicGate(rpos3 + (1, 0, 0), "000000", 0),
        Timer(rpos3 + (2, 0, 0), "000000", divmod(1, TICKS_PER_SECOND)),
        Timer(rpos3 + (3, 0, 0), "000000", divmod(2, TICKS_PER_SECOND)),
        LogicGate(rpos3 + (4, 0, 0), "000000", 0),
        Timer(rpos3 + (5, 0, 0), "000000", divmod(0, TICKS_PER_SECOND)),

        Timer(rpos3 + (3, 1, 0), "000000", divmod(3, TICKS_PER_SECOND)),
        LogicGate(rpos3 + (4, 1, 0), "000000", 3),
        LogicGate(rpos3 + (5, 1, 0), "000000", 0),
    ]
    rpos4 = rpos3 + (10, 0, 0)
    l2 = [
        LogicGate(rpos4 + (0, 0, 0), "000000", 0),
        LogicGate(rpos4 + (1, 0, 0), "000000", 0),
        Timer(rpos4 + (2, 0, 0), "000000", divmod(1, TICKS_PER_SECOND)),
        Timer(rpos4 + (3, 0, 0), "000000", divmod(2, TICKS_PER_SECOND)),
        LogicGate(rpos4 + (4, 0, 0), "000000", 0),
        Timer(rpos4 + (5, 0, 0), "000000", divmod(0, TICKS_PER_SECOND)),
        Timer(rpos4 + (6, 0, 0), "000000", divmod(3, TICKS_PER_SECOND)),
        Timer(rpos4 + (7, 0, 0), "000000", divmod(0, TICKS_PER_SECOND)),

        Timer(rpos4 + (3, 1, 0), "000000", divmod(3, TICKS_PER_SECOND)),
        LogicGate(rpos4 + (4, 1, 0), "000000", 3),
        LogicGate(rpos4 + (5, 1, 0), "000000", 0),
    ]
    rpos5 = rpos3 + (0, 3, 0)
    l3 = [
        LogicGate(rpos5 + (0, 0, 0), "000000", 1),
        Timer(rpos5 + (1, 0, 0), "000000", divmod(0, TICKS_PER_SECOND)),
        Timer(rpos5 + (2, 0, 0), "000000", divmod(3, TICKS_PER_SECOND)),
        LogicGate(rpos5 + (3, 0, 0), "000000", 0),
        Timer(rpos5 + (4, 0, 0), "000000", divmod(0, TICKS_PER_SECOND)),
        Timer(rpos5 + (5, 0, 0), "000000", divmod(0, TICKS_PER_SECOND)),

        Timer(rpos5 + (2, 1, 0), "000000", divmod(4, TICKS_PER_SECOND)),
        LogicGate(rpos5 + (3, 1, 0), "000000", 3),
        LogicGate(rpos5 + (4, 1, 0), "000000", 0),  # 8
        LogicGate(rpos5 + (5, 1, 0), "0000FF", 2),
        Timer(rpos5 + (6, 1, 0), "000000", divmod(0, TICKS_PER_SECOND)),
        Timer(rpos5 + (7, 1, 0), "000000", divmod(3, TICKS_PER_SECOND)),
        Timer(rpos5 + (8, 1, 0), "000000", divmod(4, TICKS_PER_SECOND)),

        LogicGate(rpos5 + (10, 1, 0), "000000", 0),  # 13
        Timer(rpos5 + (11, 1, 0), "000000", divmod(1, TICKS_PER_SECOND)),
        LogicGate(rpos5 + (12, 1, 0), "0000FF", 2),
        Timer(rpos5 + (13, 1, 0), "000000", divmod(4, TICKS_PER_SECOND)),

        # 17
        Timer(rpos5 + (15, 1, 0), "000000", divmod(1, TICKS_PER_SECOND)),
        LogicGate(rpos5 + (16, 1, 0), "000000", 0),
        Timer(rpos5 + (17, 1, 0), "000000", divmod(2, TICKS_PER_SECOND)),
        Timer(rpos5 + (18, 1, 0), "000000", divmod(0, TICKS_PER_SECOND)),

    ]
    # l1
    _old_connect(l1[0:5], l1[1:6])
    _old_connect(read_write_register[0][:, 1], l1[0])
    _old_connect(execute, l1[1])
    _old_connect(l1[1], routing1[0])
    _old_connect(l1[2], cache_table_lookup_dec_enable)
    _old_connect(cache_table_lookup_out[-1], l1[4])
    _old_connect(l1[4], routing1[2])
    _old_connect(l1[4], routing1[3])
    _old_connect(l1[4], routing1[4])
    _old_connect(l1[5], cache[5])
    _old_connect(l1[5], execution_done)

    _old_connect(l1[2], l1[6])
    _old_connect(l1[6], l1[8])
    _old_connect(cache_table_lookup_out[-1], l1[7])
    _old_connect(l1[7], l1[8])
    _old_connect(l1[8], l3[0])

    # l2
    _old_connect(l2[0:7], l2[1:8])
    _old_connect(read_write_register[0][:, 1], l2[0])
    _old_connect(execute, l2[1])
    _old_connect(l2[1], routing2[0])
    _old_connect(l2[2], cache_table_lookup_dec_enable)
    _old_connect(l2[2], l2[8])
    _old_connect(cache_table_lookup_out[-1], l2[4])
    _old_connect(l2[4], routing2[2])
    _old_connect(l2[4], routing2[3])
    _old_connect(l2[5], cache[8])
    _old_connect(l2[6], routing2[4])
    _old_connect(l2[7], data_register[1])
    _old_connect(l2[7], execution_done)

    _old_connect(l2[8], l2[10])
    _old_connect(cache_table_lookup_out[-1], l2[9])
    _old_connect(l2[9], l2[10])
    _old_connect(l2[10], l3[0])

    # l3
    _old_connect(l3[0:5], l3[1:6])
    _old_connect(l3[0], routing0[0])
    _old_connect(l3[1], cache_table[8])
    _old_connect(l3[1], l3[6])
    _old_connect(cache_table[2][-1], l3[3])
    _old_connect(l3[3], routing0[2])
    _old_connect(l3[3], routing0[3])
    _old_connect(l3[3], cache_pointer[1])
    _old_connect(l3[4], cache_table[5])
    _old_connect(l3[5], l3[0])

    _old_connect(l3[8:12], l3[9:13])
    _old_connect(l3[6], l3[8])
    _old_connect(cache_table[2][-1], l3[7])
    _old_connect(l3[7], l3[8])
    _old_connect(l3[9], l3[9])
    _old_connect(l3[9], routing0[4])
    _old_connect(l3[9], address_comparator[1])
    _old_connect(l3[10], cache_table[8])
    _old_connect(l3[11], routing0[5])
    _old_connect(l3[11], routing0[6])
    _old_connect(l3[11], routing0[7])
    _old_connect(l3[12], address_comparator[1])

    _old_connect(l3[13:16], l3[14:17])
    _old_connect(address_comparator[1], l3[13])
    _old_connect(l3[13], cache_full_page[8])
    _old_connect(l3[14], timer_bank_decoder_write_keep_enable)
    _old_connect(l3[14], l3[9])
    _old_connect(l3[15], l3[15])
    _old_connect(l3[15], routing0[8])
    _old_connect(l3[15], routing0[9])
    _old_connect(l3[15], routing0[10])
    _old_connect(l3[15], address_comparator[2])
    _old_connect(l3[16], address_comparator[2])

    _old_connect(l3[17:20], l3[18:21])
    _old_connect(address_comparator[2], l3[17])
    _old_connect(l3[18], timer_bank_decoder_read_enable)
    _old_connect(l3[19], routing0[11])
    _old_connect(l3[19], routing0[12])
    _old_connect(l3[19], cache_full_page[5])
    _old_connect(l3[20], l3[15])
    _old_connect(l3[20], cache_table[5])
    _old_connect(l3[20], execute)

    # _old_connect routing
    # routing0
    _old_connect(cache_pointer[0][:, 0], routing0[0])
    _old_connect(routing0[0], cache_table[6])

    _old_connect(cache_table[2], routing0[1])
    _old_connect(routing0[1], routing0[2])

    _old_connect(routing0[2], cache_table[1])

    _old_connect(cache_pointer[0][:, 0], routing0[3])
    _old_connect(routing0[3], cache_table[3])

    _old_connect(cache_pointer[0][:, 0], routing0[4])
    _old_connect(routing0[4], cache_table[6])

    _old_connect(cache_table[2], routing0[5])
    _old_connect(routing0[5], address_comparator[0])

    _old_connect(cache_table[2][-get_bits_required(num_timer_banks)-1:],
            routing0[6])
    _old_connect(routing0[6], timer_bank_decoder_write_keep_in)

    _old_connect(cache_pointer[0][:, 0], routing0[7])
    _old_connect(routing0[7], cache_full_page[6])

    _old_connect(address_register[0][get_bits_required(num_address_per_cache):, 1],
            routing0[8])
    _old_connect(routing0[8], address_comparator[0])

    _old_connect(address_register[0][-get_bits_required(num_timer_banks):, 1],
            routing0[9])
    _old_connect(routing0[9], timer_bank_decoder_read_in)

    _old_connect(cache_pointer[0][:, 0], routing0[10])
    _old_connect(routing0[10], cache_full_page[3])

    _old_connect(address_register[0][-get_bits_required(total_pages):, 1],
            routing0[11])
    _old_connect(routing0[11], cache_table[1])

    _old_connect(cache_pointer[0][:, 0], routing0[12])
    _old_connect(routing0[12], cache_table[3])

    # routing1
    _old_connect(address_register[0][-get_bits_required(total_pages):, 1],
            routing1[0])
    _old_connect(routing1[0], cache_table_lookup_in)

    _old_connect(cache_table_lookup_out, routing1[1])
    _old_connect(routing1[1], routing1[2])

    _old_connect(routing1[2],
            cache[3][-get_bits_required(num_caches):, :])

    _old_connect(address_register[0][:, 1], routing1[3])
    _old_connect(routing1[3], cache[3])

    _old_connect(data_register[0][:, 1], routing1[4])
    _old_connect(routing1[4], cache[1])

    # routing2
    _old_connect(address_register[0][-get_bits_required(total_pages):, 1],
            routing2[0])
    _old_connect(routing2[0], cache_table_lookup_in)

    _old_connect(cache_table_lookup_out, routing2[1])
    _old_connect(routing2[1], routing2[2])

    _old_connect(routing2[2],
            cache[6][-get_bits_required(num_caches):, :])

    _old_connect(address_register[0][:, 1], routing2[3])
    _old_connect(routing2[3], cache[6])

    _old_connect(cache[2], routing2[4])
    _old_connect(routing2[4], data_register[0][:, 3])

    bp.add(cache_arr[:, :, :3], cache_full_page_in, cache_full_page_out,
           timer_bank, timer_bank_decoder_read, timer_bank_decoder_read_in, timer_bank_decoder_read_enable,
           timer_bank_decoder_write_keep, timer_bank_decoder_write_keep_in, timer_bank_decoder_write_keep_enable,
           cache_table_lookup, cache_table_set_flag, cache_table_lookup_in, cache_table_lookup_out, cache_table_lookup_dec, cache_table_lookup_dec_enable,
           execute, execution_done, address_comparator,
           routing0, routing1, routing2,
           l0, l1, l2, l3,
           BarrierBlock((-3 - get_bits_required(total_pages) - 1, 0, -3),
                        "000000",
                        (bit_length*3 + 1 + 3 + get_bits_required(total_pages) + 1, 27, 1), xaxis=1, zaxis=3))

    print(
        f"Total memory: {total_bits/8} bytes, "
        f"Cached memory: {cached_bits/8} bytes, ")
