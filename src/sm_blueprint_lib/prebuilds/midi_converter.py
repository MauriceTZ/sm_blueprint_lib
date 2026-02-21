import math

from mido import MidiFile, tick2second
from mido.midifiles.tracks import _to_abstime
import numpy as np

from ..blueprint import Blueprint
from ..parts import LogicGate, Timer, TotebotHead_Bass, TotebotHead_Blip, TotebotHead_SynthVoice, Button
from ..utils import _old_connect


def midi_converter(bp: Blueprint, midi_file: str):
    mid = MidiFile(midi_file)
    tempo = 500000

    for i, track in enumerate(mid.tracks):
        # print('Track {}: {}'.format(i, track.name))
        for msg in track:
            # print(msg)
            # msg.time = tick2second(msg.time, mid.ticks_per_beat, tempo)
            if msg.type == 'set_tempo':
                tempo = msg.tempo

    print(mid.tracks[0].name)

    length = mid.length
    midi_messages = [msg for msg in _to_abstime(mid) if not msg.is_meta]
    midi_notes_to_index = {n: i for i, n in enumerate(sorted(
        {msg.note for msg in midi_messages if msg.type == "note_on" or msg.type == "note_off"}))}
    print(f"duration of piece in ticks: {length * 40}")
    print(
        f"notes used in this piece in midi notes: {midi_notes_to_index.keys()} ({len(midi_notes_to_index)} in total)")
    print(f"number of midi messages: {len(midi_messages)}")

    totebots = [TotebotHead_Bass((i * 2, 0, 0), "0000FF", (0, _midi_note_to_totebot_pitch(midi_note), 100), xaxis=1, zaxis=-2)
                if 48 >= midi_note else
                TotebotHead_SynthVoice((i * 2, 0, 0), "FF0000", (0, _midi_note_to_totebot_pitch(midi_note), 70), xaxis=1, zaxis=-2)
                if 72 >= midi_note >= 49 else
                TotebotHead_Blip((i * 2, 0, 0), "0000FF", (0, _midi_note_to_totebot_pitch(midi_note), 100), xaxis=1, zaxis=-2)
                for midi_note, i in midi_notes_to_index.items()]
    xors = [LogicGate((i * 2 + 1, 1, 0), "0000FF", 2, xaxis=-2, zaxis=-1)
            for i in range(len(midi_notes_to_index))]
    states = [0] * len(midi_notes_to_index)

    timers = [Timer((0, 1, 0), "000000", (0, 0))]
    msg_iter = iter(midi_messages)
    last_tick = 0
    add_tick = 0
    is_percussive = False
    try:
        while True:
            msg = next(msg_iter)
            if msg.type == "program_change":
                print(msg)
                is_percussive = 128 >= msg.program >= 133
            if msg.type == "control_change":
                print(msg)
            if not (msg.type == "note_on" or msg.type == "note_off") or is_percussive:
                continue
            if msg.channel == 9:
                continue

            if states[midi_notes_to_index[msg.note]] == 0 and msg.type == "note_on" and msg.velocity > 0:
                states[midi_notes_to_index[msg.note]] = 1
            elif states[midi_notes_to_index[msg.note]] == 1 and msg.type == "note_on" and msg.velocity > 0:
                continue
            elif states[midi_notes_to_index[msg.note]] == 0 and msg.type == "note_on" and msg.velocity == 0:
                continue
            elif states[midi_notes_to_index[msg.note]] == 1 and msg.type == "note_on" and msg.velocity == 0:
                states[midi_notes_to_index[msg.note]] = 0
            elif states[midi_notes_to_index[msg.note]] == 1 and msg.type == "note_off":
                states[midi_notes_to_index[msg.note]] = 0
            elif states[midi_notes_to_index[msg.note]] == 0 and msg.type == "note_off":
                continue
            current_tick = math.floor(msg.time * 45)
            if current_tick != last_tick:
                while True:
                    try:
                        timers.append(Timer((len(timers)%(2*len(xors)), 1, 2*(len(timers)//(2*len(xors)))), "000000", divmod(max(0, current_tick-last_tick-add_tick-1), 40)))
                        break
                    except AssertionError:
                        timers.append(Timer((len(timers)%(2*len(xors)), 1, 2*(len(timers)//(2*len(xors)))), "000000", (59, 39)))
                    last_tick += 60 * 40
                last_tick = current_tick
            try:
                _old_connect(timers[-1], xors[midi_notes_to_index[msg.note]])
                add_tick = 0
            except ValueError:
                add_tick = 1
                timers.append(Timer((len(timers)%(2*len(xors)), 1, 2*(len(timers)//(2*len(xors)))), "000000", divmod(0, 40)))
                _old_connect(timers[-1], xors[midi_notes_to_index[msg.note]])
                # timers[-1].disconnect(xors[midi_notes_to_index[msg.note]])
            # print(f"timer: {len(timers)}, tick: {current_tick}, {msg.type}: {msg.note}, velocity: {msg.velocity}")
    except StopIteration:
        pass

    b = Button((0, 3, 1), "000000")
    tick_gen = [LogicGate((1, 3, 0), "FF0000", 0, xaxis=-2, zaxis=-1),
                LogicGate((1, 4, 0), "FF0000", 3, xaxis=-2, zaxis=-1)]
    _old_connect(b, tick_gen)
    tick_gen[1].connect(tick_gen[0])
    _old_connect(tick_gen[0], timers[0])
    _old_connect(xors, xors)
    _old_connect(xors, totebots)
    _old_connect(timers, timers[1:])
    bp.add(totebots, xors, timers, b, tick_gen)


def _midi_note_to_totebot_pitch(midi_note: int):
    while midi_note >= 72:
        midi_note -= 24
    while midi_note <= 48:
        midi_note += 24
    return map_range(midi_note, 48, 72, 0, 1)

# Source - https://stackoverflow.com/a/70659904
# Posted by CrazyChucky, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-18, License - CC BY-SA 4.0


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
