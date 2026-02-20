import math

from mido import MidiFile
from mido.midifiles.tracks import _to_abstime
import numpy as np

from ..blueprint import Blueprint
from ..parts import LogicGate, Timer, TotebotHead_Bass, TotebotHead_Blip, TotebotHead_SynthVoice, Button
from ..utils import _old_connect


def midi_converter(bp: Blueprint, midi_file: str):
    # mid = MidiFile(r"C:\Users\mauri\OneDrive\Escritorio\Smashmouth_-_All_Star.mid")
    mid = MidiFile(midi_file)

    # for i, track in enumerate(mid.tracks):
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         print(msg)

    length = mid.length
    midi_messages = [msg for msg in _to_abstime(mid) if not msg.is_meta]
    midi_notes_to_index = {n: i for i, n in enumerate(sorted(
        {msg.note for msg in midi_messages if msg.type == "note_on" or msg.type == "note_off"}))}
    print(f"duration of piece in ticks: {length * 40}")
    print(
        f"notes used in this piece in midi notes: {midi_notes_to_index.keys()} ({len(midi_notes_to_index)} in total)")
    print(f"number of midi messages: {len(midi_messages)}")

    totebots = [TotebotHead_Bass((0 * 2, 0, 0), "0000FF", (0, _midi_note_to_totebot_pitch(midi_note), 20), xaxis=1, zaxis=-2)
                if 48 >= midi_note else
                (TotebotHead_SynthVoice((0 * 2, 0, 2), "0000FF", (1, _midi_note_to_totebot_pitch(midi_note-12), clip(map_range(midi_note, 48, 100, 100, 50), 0, 100)), xaxis=1, zaxis=-2),
                 TotebotHead_SynthVoice((0 * 2, 0, 0), "0000FF", (0, _midi_note_to_totebot_pitch(midi_note-12), clip(map_range(midi_note, 48, 100, 0, 25), 0, 100)), xaxis=1, zaxis=-2))
                if 72 >= midi_note >= 49 else
                (TotebotHead_SynthVoice((0 * 2, 0, 2), "0000FF", (1, _midi_note_to_totebot_pitch(midi_note), clip(map_range(midi_note, 48, 100, 100, 50), 0, 100)), xaxis=1, zaxis=-2),
                 TotebotHead_SynthVoice((0 * 2, 0, 0), "0000FF", (0, _midi_note_to_totebot_pitch(midi_note), clip(map_range(midi_note, 48, 100, 0, 15), 0, 100)), xaxis=1, zaxis=-2))
                for midi_note, i in midi_notes_to_index.items()]
    xors = [LogicGate((0 * 2 + 1, 1, 0), "0000FF", 2, xaxis=-2, zaxis=-1)
            for x in range(len(midi_notes_to_index))]
    # timers = [Timer((x%(len(midi_notes_to_index)*2), 1, x//(len(midi_notes_to_index)*2) * 2), "000000", (0, 1))
    #           for x in range(len(midi_messages))]
    timers = []
    last_timer = Timer((0, 1, 0), "000000", (0, 0))
    last_time = 0
    is_percussive = False
    for midi_message in midi_messages:
        if midi_message.type == "program_change":
            is_percussive = 128 >= midi_message.program >= 133
        if is_percussive:
            continue
        if midi_message.type == "note_on" or midi_message.type == "note_off":
            current_time = math.floor(midi_message.time * 40)
            if current_time != last_time:
                last_timer = Timer((0, 1, 0), "000000", divmod(max(0, current_time - last_time - 1), 40))
                last_time = current_time
                _old_connect(last_timer, xors[midi_notes_to_index[midi_message.note]])
                if timers:
                    _old_connect(timers[-1], last_timer)
                timers.append(last_timer)
            else:
                _old_connect(last_timer, xors[midi_notes_to_index[midi_message.note]])

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
    # for msg in notes[:10]:
    #     print(msg)


def _midi_note_to_totebot_pitch(midi_note: int):
    while midi_note > 72:
        midi_note -= 12
    while midi_note < 48:
        midi_note += 12
    return map_range(midi_note, 48, 72, 0, 1)

# Source - https://stackoverflow.com/a/70659904
# Posted by CrazyChucky, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-18, License - CC BY-SA 4.0

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Source - https://stackoverflow.com/a/58470178
# Posted by Bill
# Retrieved 2026-02-19, License - CC BY-SA 4.0

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value
