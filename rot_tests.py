from src.sm_blueprint_lib import *
bp = Blueprint()
g0 = LogicGate((0, 0, 0), "ffffff")
g1 = LogicGate((1, 0, 0), "ffffff")
g2 = LogicGate((2, 0, 0), "ffffff")
g3 = LogicGate((3, 0, 0), "ffffff")
g4 = LogicGate((4, 0, 0), "ffffff")

set_rotation(g0.pos, g0.xaxis, g0.zaxis , "up", "right")
# set_rotation(g1.pos, g1.xaxis, g1.zaxis, "up", "left")
set_rotation(g2.pos, g2.xaxis, g2.zaxis, "up", "up")
set_rotation(g3.pos, g3.xaxis, g3.zaxis, "up", "down")
set_rotation(g4.pos, g4.xaxis, g4.zaxis, "up", "right")


bp.add(g0,
       g1,
       g2,
       g3,
       g4,
       BarrierBlock((0,0,-1),"ff0000", (1,1,1)),
       BarrierBlock((1,0,-1),"ff0000", (1,1,1)),
       BarrierBlock((2,0,-1),"ff0000", (1,1,1)),
       BarrierBlock((3,0,-1),"ff0000", (1,1,1)),
       BarrierBlock((4,0,-1),"ff0000", (1,1,1)))
path = r"C:\Users\mauri\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198400983548\Blueprints\c35f6e4e-52cb-4b00-8afa-f0ffd3fbb012\blueprint.json"
save_blueprint(bp, path)