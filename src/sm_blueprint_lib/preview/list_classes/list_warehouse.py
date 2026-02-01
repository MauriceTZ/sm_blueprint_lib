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

shapeset_json_path = os.path.join(GAME_DATA, "Objects", "Database", "ShapeSets", "warehouse.json")
print(shapeset_json_path)
survival_shapeset_json_path = os.path.join(SURVIVAL_DATA, "Objects", "Database", "ShapeSets", "warehouse.json")
print(survival_shapeset_json_path)

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


with open(survival_shapeset_json_path) as fp:
    survival_parts_json = json.load(fp)
    # pp(survival_decor_json)

all_parts = survival_parts_json["partList"]
# pp(all_decor)

for part in all_parts:
    part["name2"] = part["name"]
    part["name"] = all_inventory_descriptions[part["uuid"]]["title"] if all_inventory_descriptions.get(part["uuid"]) else part["name"]
    if isinstance(part["renderable"], str):
        with open(part["renderable"].replace("$GAME_DATA", GAME_DATA).replace("$SURVIVAL_DATA", SURVIVAL_DATA)) as fp:
            part["renderable"] = json.load(fp)
pp(all_parts)

print("\n"*10)

classes = "".join(  # TODO: check more cylinder cases
f'''
@dataclass
class {b["name"].replace(" ", "").replace("-", "").replace("'", "").replace(":", "_")}(BasePart):
    """Class that represents a {b["name"]}.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.{b["name"].replace(" ", "_").replace("-", "_").replace("'", "").replace(":", "_")})

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3{(b['hull']['x'], b['hull']['y'], b['hull']['z']) if b.get('hull') else
                         (b["box"]['x'], b["box"]['y'], b["box"]['z']) if b.get('box') else
                         (  (b["cylinder"]["diameter"],
                             b["cylinder"]["depth"],
                             b["cylinder"]["diameter"]) if b["cylinder"]["axis"] == "Y" else
                            (b["cylinder"]["depth"],
                             b["cylinder"]["diameter"],
                             b["cylinder"]["diameter"]) if b["cylinder"]["axis"] == "X" else
                            (b["cylinder"]["diameter"],
                             b["cylinder"]["diameter"],
                             b["cylinder"]["depth"]) if b["cylinder"]["axis"] == "Z" else
                             (1,1,1)) if b.get("cylinder") else
                         (b['wedge']['x'], b['wedge']['y'], b['wedge']['z']) if b.get('wedge') else
                         (1, 1, 1)}
'''
    for b in all_parts
)
print(classes)
