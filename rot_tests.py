from src.sm_blueprint_lib import *
bp = Blueprint()
g0 = LogicGate((0, 0, 0), "ffffff"); r0 = Rot(g0.xaxis, g0.zaxis)
g1 = LogicGate((1, 0, 0), "ffffff"); r1 = Rot(g1.xaxis, g1.zaxis)
g2 = LogicGate((2, 0, 0), "ffffff"); r2 = Rot(g2.xaxis, g2.zaxis)
g3 = LogicGate((3, 0, 0), "ffffff"); r3 = Rot(g3.xaxis, g3.zaxis)
g4 = LogicGate((4, 0, 0), "ffffff"); r4 = Rot(g4.xaxis, g4.zaxis)

set_rotation(g0.pos, r0, "up", "right"); g0.xaxis = r0.x_axis; g0.zaxis = r0.y_axis
# set_rotation(g1.pos, r1, "up", "left"); g1.xaxis = r1.x_axis; g1.zaxis = r1.y_axis
set_rotation(g2.pos, r2, "up", "up"); g2.xaxis = r2.x_axis; g2.zaxis = r2.y_axis
set_rotation(g3.pos, r3, "up", "down"); g3.xaxis = r3.x_axis; g3.zaxis = r3.y_axis
set_rotation(g4.pos, r4, "up", "right"); g4.xaxis = r4.x_axis; g4.zaxis = r4.y_axis


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