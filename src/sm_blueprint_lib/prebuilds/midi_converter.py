import math
from pprint import pp

from mido import MidiFile, tick2second
from mido.midifiles.tracks import _to_abstime
import numpy as np

from ..blueprint import Blueprint
from ..parts import LogicGate, Timer, TotebotHead_Bass, TotebotHead_Blip, TotebotHead_SynthVoice, TotebotHead_Percussion, Button
from ..utils import _old_connect
from ..constants import TICKS_PER_SECOND


def midi_converter(bp: Blueprint, midi_file: str, *, noblip=False, doglitchweld=False, dosustain=False, transpose=0, speed=1.0):
    mid = MidiFile(midi_file)
    # tempo = 500000
    # for i, track in enumerate(mid.tracks):
    #     # print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         # print(msg)
    #         if msg.type == 'set_tempo':
    #             tempo = msg.tempo
    #         msg.time = tick2second(msg.time, mid.ticks_per_beat, tempo)

    length = mid.length
    all_messages = [msg for msg in _to_abstime(
        mid) if not msg.is_meta and hasattr(msg, "channel")]
    channels = sorted(set(msg.channel for msg in all_messages))
    messages_per_channel = {}
    for msg in all_messages:
        messages_per_channel.setdefault(msg.channel, []).append(msg)
    print("Messages per channel:")
    pp({chan: len(msgs) for chan, msgs in messages_per_channel.items()})
    notes_per_channel = {chan: sorted(set(msg.note for msg in msgs if hasattr(
        msg, "note"))) for chan, msgs in messages_per_channel.items()}
    print("Notes per channel:")
    pp(notes_per_channel)
    program_per_channel = {chan: ([msg.program for msg in msgs if msg.type == "program_change"] or [
                                  0])[0] for chan, msgs in messages_per_channel.items()}
    print("Programs used in each channel:")
    pp(program_per_channel)
    print(f"duration of file: {length * 40:.0f} ticks or {length:.2f} seconds")
    print(f"number of midi messages: {len(all_messages)}")
    print(f"channels: {channels}")

    notes_to_index = {chan: {note: index for index, note in enumerate(
        notes)} for chan, notes in notes_per_channel.items()}

    totebots = {}
    states = {}
    xors = {}
    min_note = min(note for l in notes_per_channel.values() for note in l)
    max_note = max(note for l in notes_per_channel.values() for note in l)
    length_creation = max_note - min_note + 1
    print(f"min note: {min_note}")
    print(f"min note: {max_note}")
    # TODO: add the rest of the cases
    percussion_table = {
        # midi percussion note to TotebotHead_Percussion equivalent
        35: 2,
        36: 2,
        38: 7,
        40: 8,
        41: 0,
        42: 10,
        43: 4,
        45: 2,
        46: 12,
        49: 20,
        51: 21,
        52: 20,
        55: 20,
        57: 21,
    }
    for chan in channels:
        if chan == 9:
            try:
                totebots[chan] = [TotebotHead_Percussion(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), "00FFFF", (1, map_range(percussion_table[note]+48, 48, 72, 0, 1), 60), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
            except KeyError as e:
                raise KeyError(f"This MIDI percussion instrument is yet to be mapped to a TotebotHead_Percussion note. -> {e.args[0]}")
        else:
            match program_per_channel[chan]:
                # case 4:
                #     totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2, 0, chan * 2), "00FFFF", (1, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                # case 6 | 7:
                #     totebots[chan] = [TotebotHead_Blip(((note-min_note) * 2, 0, chan * 2), "00FFFF", (1, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                # case prog if 7 >= prog >= 0:
                #     totebots[chan] = [TotebotHead_Blip(((note-min_note) * 2, 0, chan * 2), "00FFFF", (0, _midi_note_to_totebot_pitch(note), 60), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                # case prog if 15 >= prog >= 8:
                #     totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2, 0, chan * 2), "00FFFF", (1, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                # case prog if 23 >= prog >= 16:
                #     totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2, 0, chan * 2), "00FFFF", (0, _midi_note_to_totebot_pitch(note), 60), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                # case 25 | 27 | 29 | 30 | 31:
                #     totebots[chan] = [TotebotHead_Blip(((note-min_note) * 2, 0, chan * 2), "00FFFF", (1, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                # case prog if 31 >= prog >= 24:
                #     totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2, 0, chan * 2), "00FFFF", (1, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                # case prog if 38 >= prog >= 36:
                #     totebots[chan] = [TotebotHead_Bass(((note-min_note) * 2, 0, chan * 2), "00FFFF", (1, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                # case prog if 39 >= prog >= 32:
                #     totebots[chan] = [TotebotHead_Bass(((note-min_note) * 2, 0, chan * 2), "00FFFF", (0, _midi_note_to_totebot_pitch(note), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                case _:
                    totebots[chan] = [
                        (TotebotHead_Bass(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), "00FFFF", (0, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)
                        if 48 >= note else
                        TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), "00FFFF", (0, _midi_note_to_totebot_pitch((note+transpose)), 60), xaxis=1, zaxis=-2)
                        if 72 >= note else
                        TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), "00FFFF", (0, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)
                        if not noblip else
                        (TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), "00FFFF", (0, _midi_note_to_totebot_pitch((note+transpose)), 30), xaxis=1, zaxis=-2),
                         TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), "00FFFF", (1, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)))
                        for note in notes_per_channel[chan]]
        xors[chan] = [[LogicGate(((note-min_note) * 2 * (not doglitchweld) + 1, 1, chan * 2 * (not doglitchweld)), "00FFFF", 2, xaxis=-2, zaxis=-1),
                       LogicGate(((note-min_note) * 2 * (not doglitchweld) + 1, 3, chan * 2 * (not doglitchweld)), "000000", 1, xaxis=-2, zaxis=-1)] for note in notes_per_channel[chan]]
        states[chan] = {"sustain": False,
                        "notes": set()}
    for chan in channels:
        for i in range(len(notes_per_channel[chan])):
            _old_connect(xors[chan][i][0], totebots[chan][i])
            _old_connect(xors[chan][i][0], xors[chan][i][0])

    timers = [Timer((0, 1, 0), "000000", (0, 0))]
    iter_messages = iter(all_messages)
    last_tick = 0
    lost_ticks = 0
    try:
        while True:
            msg = next(iter_messages)
            if dosustain:
                if msg.is_cc(64):
                    print("pedal", msg.channel, msg.value)
                    states[msg.channel]["sustain"] = 64 >= msg.value
                    if msg.value < 64:
                        for chan, note in states[msg.channel]["notes"]:
                            buffer = xors[chan][notes_to_index[chan][note]]
                            while True:
                                try:
                                    _old_connect(timers[-1], buffer[-1])
                                except IndexError:
                                    buffer.append(LogicGate((buffer[-1].pos + (0, 1, 0)) * (not doglitchweld), "000000", 1, xaxis=-2, zaxis=-1))
                                    continue
                                except ValueError:
                                    timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 1, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000",
                                                        divmod(0, 40)))
                                    lost_ticks += 1
                                    continue
                                break
                        states[msg.channel]["notes"].clear()
                elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                    note_id = (msg.channel, msg.note)
                    if states[msg.channel]["sustain"]:
                        states[msg.channel]["notes"].add(note_id)
                        continue
                elif msg.type == "note_on":
                    note_id = (msg.channel, msg.note)
                    if note_id in states[msg.channel]["notes"]:
                        buffer = xors[msg.channel][notes_to_index[msg.channel][msg.note]]
                        while True:
                            try:
                                _old_connect(timers[-1], buffer[-1])
                            except IndexError:
                                buffer.append(LogicGate((buffer[-1].pos + (0, 1, 0)) * (not doglitchweld), "000000", 1, xaxis=-2, zaxis=-1))
                                continue
                            except ValueError:
                                timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 1, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000",
                                                    divmod(0, 40)))
                                lost_ticks += 1
                                continue
                            break
                        states[msg.channel]["notes"].remove(note_id)
            if not (msg.type == "note_on" or msg.type == "note_off"):
                continue
            current_tick = math.floor(msg.time * TICKS_PER_SECOND * 1 / speed)
            dt = 0
            if current_tick != last_tick:
                if lost_ticks > 0:
                    dt = current_tick - last_tick - 1 - lost_ticks
                    if dt < 0:
                        lost_ticks += dt
                        dt = 0
                    else:
                        lost_ticks = 0
                else:
                    dt = current_tick - last_tick - 1
                while True:
                    try:
                        timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 1, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000",
                                            divmod(dt, 40)))
                    except AssertionError:
                        timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 1, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000",
                                            (59, 40)))
                        dt -= 2399
                        continue
                    break

            buffer = xors[msg.channel][notes_to_index[msg.channel][msg.note]]
            while True:
                try:
                    _old_connect(timers[-1], buffer[-1])
                except IndexError:
                    buffer.append(LogicGate((buffer[-1].pos + (0, 1, 0)) * (not doglitchweld), "000000", 1, xaxis=-2, zaxis=-1))
                    continue
                except ValueError:
                    timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 1, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000",
                                        divmod(0, 40)))
                    lost_ticks += 1
                    continue
                break
            last_tick = current_tick
    except StopIteration:
        pass

    b = Button((-1, 2, 1), "000000")
    tick_gen = [LogicGate((0, 2, 0), "FF0000", 0, xaxis=-2, zaxis=-1),
                LogicGate((0, 3, 0), "FF0000", 3, xaxis=-2, zaxis=-1)]
    _old_connect(b, tick_gen)
    tick_gen[1].connect(tick_gen[0])
    _old_connect(tick_gen[0], timers[0])
    _old_connect(timers, timers[1:])
    # for l in xors.values():
    #     _old_connect(l[:-1], l[-1])
    for chan in channels:
        for i in range(len(notes_per_channel[chan])):
            _old_connect(xors[chan][i][1:], xors[chan][i][0])
    bp.add(totebots.values(), xors.values(), timers, b, tick_gen)




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
