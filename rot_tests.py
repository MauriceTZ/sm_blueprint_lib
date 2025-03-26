from pprint import pp

from src.sm_blueprint_lib import *

bp = Blueprint()

g0 = LogicGate((1, 0, 0), "ffffff")  # .rotate("up", "right")
g1 = LogicGate((2, 0, 0), "ffffff").rotate("up", "left")
g2 = LogicGate((3, 0, 0), "ffffff").rotate("up", "up")
g3 = LogicGate((4, 0, 0), "ffffff").rotate("up", "down")
g4 = LogicGate((5, 0, 0), "ffffff").rotate("up", "right")

bp.add(g0,
       g1,
       g2,
       g3,
       g4,
       # show the axis just for debugging
       BarrierBlock((0, 0, -1), "ffffff", (1, 1, 1)),
       BarrierBlock((1, -1, -1), "ff0000", (5, 3, 1)),
       BarrierBlock((0, 1, -1), "00ff00", (1, 3, 1)),
       BarrierBlock((0, 0, 0), "0000ff", (1, 1, 5)),
       )
path = r"C:\Users\mauri\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198400983548\Blueprints\c35f6e4e-52cb-4b00-8afa-f0ffd3fbb012\blueprint.json"

pp(bp)
save_blueprint(bp, path)
