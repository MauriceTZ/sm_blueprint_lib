from src.sm_blueprint_lib import *

# Create empty Blueprint
bp = Blueprint()

# Put here the path to your MIDI file, here are some examples:
file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\FE!N - Travis Scott (fein).mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\chopin-ballade3.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Undertale_-_Megalovania.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Erika - German Folk Song.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\QueenGreatest_hits_Bohemian_Rhapsody.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Careless-Whisper.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Thomas The Tank Engine Theme (MIDI).mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\ussr.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\arabesque_1_(c)oguri.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Hungarian Dance No.5.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Hungarian-Rhapsody-Nr-2.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Waltz-Of-The-Flowers-Opus-71a.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\andante_polacca_22_(c)finley.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Toccato-&-Fugue-in-D-Minor.mid"
file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\The Entertainer.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Chopin_Nocturne_Op9_No2.mid"
# file = r"demo_MIDIs\C. A. Debussy - Clair De Lune (1903).mid"
# file = r"demo_MIDIs\Smashmouth_-_All_Star.mid"
# file = r"demo_MIDIs\vanessa_carltona_thousand_miles.mid"

# Call midi_converter() to make the conversion
midi_converter(bp, file, 
               noblip=False, doglitchweld=True, dosustain=False, transpose=0, 
               color="5050FF", tryImitateInstruments=False, speed=1.0)

print(f"Prebuild size: {len(bp.bodies[0].childs)} parts")
# Save the creation into an existing blueprint in your lift, for example "MIDI converter output"
save_blueprint("MIDI converter output", bp)
