from src.sm_blueprint_lib import *

# Create empty Blueprint
bp = Blueprint()

# Put here the path to your MIDI file, here are some examples:
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Toccato-&-Fugue-in-D-Minor.mid"
file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\The Entertainer.mid"
# file = r"C:\Users\mauri\OneDrive\Documents\GeneralUser-GS\demo MIDIs\Chopin_Nocturne_Op9_No2.mid"
# file = r"demo_MIDIs\C. A. Debussy - Clair De Lune (1903).mid"
# file = r"demo_MIDIs\Smashmouth_-_All_Star.mid"
# file = r"demo_MIDIs\vanessa_carltona_thousand_miles.mid"

# Call midi_converter() to make the conversion
midi_converter(bp, file, noblip=True, doglitchweld=True)

print(f"Prebuild size: {len(bp.bodies[0].childs)} parts")
# Save the creation into an existing blueprint in your lift, for example "MIDI converter output"
save_blueprint("MIDI converter output", bp)
