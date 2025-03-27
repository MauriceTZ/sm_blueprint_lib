from src.sm_blueprint_lib import *

bp = Blueprint()


ship = Block(SHAPEID.Spaceship_Block,(0,0,0),COLOR.Spaceship_Block)

print(ship.color)
print(ship.shapeId)
print(ship.pos)

wood = Block(SHAPEID.Wood_Block_1,(1,0,0),COLOR.Wood_Block_1)

print(wood.color)
print(wood.shapeId)
print(wood.pos)
