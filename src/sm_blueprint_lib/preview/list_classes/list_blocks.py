import json
import os
from pprint import pp

path_to_steam = r"C:\Program Files (x86)\Steam"
GAME_DATA = os.path.join(path_to_steam, "steamapps", "common", "Scrap Mechanic", "Data")
print(GAME_DATA)
SURVIVAL_DATA = os.path.join(path_to_steam, "steamapps", "common", "Scrap Mechanic", "Survival")
print(SURVIVAL_DATA)

inventory_item_descriptions_json_path = os.path.join(GAME_DATA, "Gui", "Language", "English", "InventoryItemDescriptions.json")
print(inventory_item_descriptions_json_path)
survival_inventory_descriptions_json_path = os.path.join(SURVIVAL_DATA, "Gui", "Language", "English", "inventoryDescriptions.json")
print(survival_inventory_descriptions_json_path)

blocks_json_path = os.path.join(GAME_DATA, "Objects", "Database", "ShapeSets", "blocks.json")
print(blocks_json_path)
survival_blocks_json_path = os.path.join(SURVIVAL_DATA, "Objects", "Database", "ShapeSets", "blocks.json")
print(survival_blocks_json_path)

with open(inventory_item_descriptions_json_path) as fp:
    inventory_item_descriptions_json = json.load(fp)
    # pp(inventory_item_descriptions_json)
    
with open(survival_inventory_descriptions_json_path) as fp:
    survival_inventory_descriptions_json = json.load(fp)
    # pp(survival_inventory_descriptions_json)

all_inventory_descriptions = {}
all_inventory_descriptions.update(inventory_item_descriptions_json)
all_inventory_descriptions.update(survival_inventory_descriptions_json)
# pp(all_inventory_descriptions)

with open(blocks_json_path) as fp:
    blocks_json = json.load(fp)
    # pp(blocks_json)

with open(survival_blocks_json_path) as fp:
    survival_blocks_json = json.load(fp)
    # pp(survival_blocks_json)

all_blocks = blocks_json["blockList"] + survival_blocks_json["blockList"]
# pp(all_blocks)

for block in all_blocks:
    block["name"] = all_inventory_descriptions[block["uuid"]]["title"]
# pp(all_blocks)

# # I used this to copy all the textures via powershell lol... 
# print(", ".join('"'+block["dif"]
#                .replace("$GAME_DATA", GAME_DATA)
#                .replace("$SURVIVAL_DATA", SURVIVAL_DATA)+'"'
#                for block in all_blocks))

classes = "".join(
f'''
@dataclass
class {b["name"].replace(" ", "")}(BaseBoundablePart):
    """Class that represents a {b["name"]}.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.{b["name"].replace(" ", "_")})

    def __post_init__(self):
        super().__post_init__()
        self._tiling = {b["tiling"]}
'''
    for b in all_blocks
)
print(classes)
