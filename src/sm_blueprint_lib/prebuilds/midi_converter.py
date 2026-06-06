import math
from pprint import pp

from mido import MidiFile, tick2second
from mido.midifiles.tracks import _to_abstime
import numpy as np

from ..blueprint import Blueprint
from ..parts import LogicGate, Timer, TotebotHead_Bass, TotebotHead_Blip, TotebotHead_SynthVoice, TotebotHead_Percussion, Button
from ..utils import _old_connect
from ..constants import TICKS_PER_SECOND
from ..pos import Pos


def midi_converter(bp: Blueprint, midi_file: str, *, noblip=False, doglitchweld=False, dosustain=False, transpose=0, color="00FFFF", tryImitateInstruments=True, speed=1.0, pitch_bend_semitones=2):
    mid = MidiFile(midi_file, clip=True)
    # tempo = 500000
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)
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
    
    # NUEVA LÓGICA: Añadir notas adyacentes para el pitch bend
    notes_per_channel = {}
    for chan, msgs in messages_per_channel.items():
        base_notes = set(msg.note for msg in msgs if hasattr(msg, "note"))
        has_pitchwheel = any(msg.type == 'pitchwheel' for msg in msgs)
        
        if has_pitchwheel and chan != 9:  # Evitamos hacer bend al canal de percusión
            bent_notes = set()
            for note in base_notes:
                # Añadimos el margen basado en el parámetro dinámico
                for bend in range(-pitch_bend_semitones, pitch_bend_semitones + 1):
                    bent_notes.add(max(0, min(127, note + bend)))
            notes_per_channel[chan] = sorted(bent_notes)
        else:
            notes_per_channel[chan] = sorted(base_notes)

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
    print(f"max note: {max_note}")
    # TODO: add the rest of the cases
    percussion_table = {
        # midi percussion note to TotebotHead_Percussion equivalent
        # reference: https://soundprogramming.net/file-formats/general-midi-drum-note-numbers/
        35: (2, 1),
        36: (2, 1),
        37: (0, 1),
        38: (7, 1),
        39: (5, 1),
        40: (8, 1),
        41: (0, 1),
        42: (10, 1),
        43: (4, 1),
        44: (14, 1),
        45: (2, 1),
        46: (12, 1),
        47: (2, 0),
        48: (13, 0),
        49: (20, 1),
        50: (3, 0),
        51: (21, 1),
        52: (20, 1),
        53: (12, 1),
        54: (23, 1),
        55: (20, 1),
        57: (21, 1),
        59: (21, 1),
        60: (17, 0),
        61: (19, 0),
        62: (19, 0),
        63: (19, 0),
        64: (3, 0),
        67: (17, 0),
        68: (19, 0),
        69: (13, 1),
        80: (12, 0),
        82: (14, 1)
    }
    for chan in channels:
        if chan == 9:
            try:
                totebots[chan] = [TotebotHead_Percussion(((note-min_note) * 2 * (not doglitchweld), 0, chan * 2 * (not doglitchweld)), color, (percussion_table[note][1], map_range(percussion_table[note][0]+48, 48, 72, 0, 1), 30), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
            except KeyError as e:
                raise KeyError(f"This MIDI percussion instrument is yet to be mapped to a TotebotHead_Percussion note. -> {e.args[0]}")
        else:
            if not tryImitateInstruments:
                totebots[chan] = [
                    (TotebotHead_Bass(((note-min_note) * 2 * (not doglitchweld), 0, 2 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)
                    if 48 >= note else
                    TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 60), xaxis=1, zaxis=-2)
                    if 72 >= note else
                    TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)
                    if not noblip else
                    (TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 30), xaxis=1, zaxis=-2),
                    TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)))
                    for note in notes_per_channel[chan]]
            else:
                match program_per_channel[chan]:
                    case 4:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                    case 6 | 7:
                        totebots[chan] = [TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                    case prog if 7 >= prog >= 0:
                        totebots[chan] = [TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 50), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case prog if 15 >= prog >= 8:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case prog if 23 >= prog >= 16:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case 25 | 27 | 29 | 30 | 31:
                        totebots[chan] = [(TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose+12), 100), xaxis=1, zaxis=-2)
                                           if 48 >= note else
                                          (TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose+12), 100), xaxis=1, zaxis=-2),
                                           TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 40), xaxis=1, zaxis=-2))) for note in notes_per_channel[chan]]
                    case prog if 31 >= prog >= 24:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case prog if 38 >= prog >= 36:
                        totebots[chan] = [TotebotHead_Bass(((note-min_note) * 2 * (not doglitchweld), 0, 2 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 40), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                    case prog if 39 >= prog >= 32:
                        totebots[chan] = [TotebotHead_Bass(((note-min_note) * 2 * (not doglitchweld), 0, 2 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 70), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case 65:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                    case 66:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case 48:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 2 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 50), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                    case 49:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]


                    case 79:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]
                    case 80:
                        totebots[chan] = [TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 100), xaxis=1, zaxis=-2) for note in notes_per_channel[chan]]

                    case 81:
                        totebots[chan] = [(TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch(note+transpose), 30), xaxis=1, zaxis=-2),
                                           TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch(note+transpose), 70), xaxis=1, zaxis=-2)) for note in notes_per_channel[chan]]

                    case unknown:
                        print(f"unknown program: {unknown}")
                        totebots[chan] = [
                            (TotebotHead_Bass(((note-min_note) * 2 * (not doglitchweld), 0, 2 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)
                            if 48 >= note else
                            TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 60), xaxis=1, zaxis=-2)
                            if 72 >= note else
                            TotebotHead_Blip(((note-min_note) * 2 * (not doglitchweld), 0, 6 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)
                            if not noblip else
                            (TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (0, _midi_note_to_totebot_pitch((note+transpose)), 30), xaxis=1, zaxis=-2),
                            TotebotHead_SynthVoice(((note-min_note) * 2 * (not doglitchweld), 0, 4 * doglitchweld + chan * 2 * (not doglitchweld)), color, (1, _midi_note_to_totebot_pitch((note+transpose)), 100), xaxis=1, zaxis=-2)))
                            for note in notes_per_channel[chan]]
        xors[chan] = [[LogicGate(((note-min_note) * 2 * (not doglitchweld) + 1, 1, chan * 2 * (not doglitchweld)), color, 2, xaxis=-2, zaxis=-1),
                       LogicGate(((note-min_note) * 2 * (not doglitchweld) + 1, 3, chan * 2 * (not doglitchweld)), "000000", 1, xaxis=-2, zaxis=-1)] for note in notes_per_channel[chan]]
        
        # NUEVO ESTADO: Separamos sustenidas de activas y guardamos el offset
        states[chan] = {
            "sustain": False,
            "sustained_notes": set(),
            "active_base_notes": set(),
            "pitch_offset": 0
        }
        
    for chan in channels:
        for i in range(len(notes_per_channel[chan])):
            _old_connect(xors[chan][i][0], totebots[chan][i])
            _old_connect(xors[chan][i][0], xors[chan][i][0])

    timers = [Timer((0, 2, 0), "000000", (0, 0))]
    iter_messages = iter(all_messages)
    last_tick = 0
    lost_ticks = 0
    
    # FUNCIONES AUXILIARES PARA REFACTORIZAR EL MANEJO DEL BÚFER
    def advance_time(msg_time):
        nonlocal last_tick, lost_ticks
        current_tick = math.floor(msg_time * TICKS_PER_SECOND * 1 / speed)
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
                    timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 2, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000", divmod(dt, 40)))
                except AssertionError:
                    timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 2, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000", (59, 40)))
                    dt -= 2399
                    continue
                break
            last_tick = current_tick

    def send_signal(chan, physical_note):
        nonlocal lost_ticks
        if physical_note not in notes_to_index[chan]:
            return
        buffer = xors[chan][notes_to_index[chan][physical_note]]
        while True:
            try:
                _old_connect(timers[-1], buffer[-1])
            except IndexError:
                buffer.append(LogicGate(buffer[-1].pos + Pos(0, 1, 0) * (not doglitchweld), "000000", 1, xaxis=-2, zaxis=-1))
                continue
            except ValueError:
                timers.append(Timer((len(timers) % (2*length_creation) * (not doglitchweld), 2, 2*(len(timers)//(2*length_creation)) * (not doglitchweld)), "000000", divmod(0, 40)))
                lost_ticks += 1
                continue
            break

    try:
        while True:
            msg = next(iter_messages)
            
            if dosustain:
                if msg.is_cc(64):
                    states[msg.channel]["sustain"] = 64 >= msg.value
                    if msg.value < 64:
                        # Se liberó el sustain: apagar las notas físicamente
                        advance_time(msg.time)
                        for base_note in states[msg.channel]["sustained_notes"]:
                            physical_note = base_note + states[msg.channel]["pitch_offset"]
                            send_signal(msg.channel, physical_note)
                        states[msg.channel]["sustained_notes"].clear()
                
                elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                    base_note = msg.note
                    states[msg.channel]["active_base_notes"].discard(base_note)
                    if states[msg.channel]["sustain"]:
                        states[msg.channel]["sustained_notes"].add(base_note)
                        continue # Evita enviar la señal de apagado al buffer físico
                        
                elif msg.type == "note_on":
                    base_note = msg.note
                    states[msg.channel]["active_base_notes"].add(base_note)
                    if base_note in states[msg.channel]["sustained_notes"]:
                        # Retriggering: si estaba sostenida, apagarla físicamente antes del note_on
                        advance_time(msg.time)
                        physical_note = base_note + states[msg.channel]["pitch_offset"]
                        send_signal(msg.channel, physical_note)
                        states[msg.channel]["sustained_notes"].remove(base_note)
            else:
                if msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                    states[msg.channel]["active_base_notes"].discard(msg.note)
                elif msg.type == "note_on":
                    states[msg.channel]["active_base_notes"].add(msg.note)

            # LÓGICA PITCH WHEEL INTERCEPTADA
            if msg.type == 'pitchwheel' and msg.channel != 9:
                
                # Calculamos dinámicamente cuántos "puntos" de msg.pitch equivalen a 1 semitono
                points_per_semitone = 8192 / pitch_bend_semitones
                
                # Convertimos a semitono discreto aproximado
                new_offset = round(msg.pitch / points_per_semitone)
                
                # Aseguramos que el offset no exceda el límite establecido
                new_offset = max(-pitch_bend_semitones, min(pitch_bend_semitones, new_offset))
                
                if new_offset != states[msg.channel]["pitch_offset"]:
                    old_offset = states[msg.channel]["pitch_offset"]
                    states[msg.channel]["pitch_offset"] = new_offset
                    
                    # Intercambiamos solo las notas que están sonando en este instante
                    all_playing = states[msg.channel]["active_base_notes"] | states[msg.channel].get("sustained_notes", set())
                    if all_playing:
                        advance_time(msg.time)
                        for base_note in all_playing:
                            old_physical = base_note + old_offset
                            new_physical = base_note + new_offset
                            send_signal(msg.channel, old_physical)
                            send_signal(msg.channel, new_physical)
                continue
                
            if not (msg.type == "note_on" or msg.type == "note_off"):
                continue

            # FLUJO ESTÁNDAR NOTE_ON / NOTE_OFF CON OFFSET APLICADO
            advance_time(msg.time)
            physical_note = msg.note + states[msg.channel]["pitch_offset"]
            send_signal(msg.channel, physical_note)

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