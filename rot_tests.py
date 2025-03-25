from pprint import pp

from src.sm_blueprint_lib import *
bp = Blueprint()
g0 = LogicGate((1, 0, 0), "ffffff")
g1 = LogicGate((2, 0, 0), "ffffff")
g2 = LogicGate((3, 0, 0), "ffffff")
g3 = LogicGate((4, 0, 0), "ffffff")
g4 = LogicGate((5, 0, 0), "ffffff")

# set_rotation(g0, "up", "right")
set_rotation(g1, "up", "left")
set_rotation(g2, "up", "up")
set_rotation(g3, "up", "down")
# Passing the same part to see what happens lol
set_rotation(g4, "up", "right")
set_rotation(g4, "up", "right")


bp.add(g0,
       g1,
       g2,
       g3,
       g4,
       # show the axis just for debugging
       BarrierBlock((0,0,-1),"ffffff", (1,1,1)),
       BarrierBlock((1,0,-1),"ff0000", (5,1,1)),
       BarrierBlock((0,1,-1),"00ff00", (1,5,1)),
       BarrierBlock((0,0,0),"0000ff", (1,1,5)),
       )
path = r"C:\Users\mauri\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198400983548\Blueprints\c35f6e4e-52cb-4b00-8afa-f0ffd3fbb012\blueprint.json"

pp(bp)
save_blueprint(bp, path)