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

decor_json_path = os.path.join(GAME_DATA, "Objects", "Database", "ShapeSets", "decor.json")
print(decor_json_path)
survival_decor_json_path = os.path.join(SURVIVAL_DATA, "Objects", "Database", "ShapeSets", "decor.json")
print(survival_decor_json_path)

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

with open(decor_json_path) as fp:
    decor_json = json.load(fp)
    # pp(decor_json)

with open(survival_decor_json_path) as fp:
    survival_decor_json = json.load(fp)
    # pp(survival_decor_json)

all_decor = decor_json["partList"] + survival_decor_json["partList"]
# pp(all_decor)

for block in all_decor:
    block["name2"] = block["name"]
    block["name"] = all_inventory_descriptions[block["uuid"]]["title"]
    if isinstance(block["renderable"], str):
        with open(block["renderable"].replace("$GAME_DATA", GAME_DATA).replace("$SURVIVAL_DATA", SURVIVAL_DATA)) as fp:
            block["renderable"] = json.load(fp)
pp(all_decor)

# # # I used this to copy all the textures via powershell lol... 
# # print(", ".join('"'+block["dif"]
# #                .replace("$GAME_DATA", GAME_DATA)
# #                .replace("$SURVIVAL_DATA", SURVIVAL_DATA)+'"'
# #                for block in all_decor))

classes = "".join(
f'''
@dataclass
class {b["name"].replace(" ", "").replace("-", "")}(BaseNormalPart):
    """Class that represents a {b["name"]}.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.{b["name"].replace(" ", "_").replace("-", "_")})

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3{(b['hull']['x'], b['hull']['y'], b['hull']['z']) if b.get('hull') else
                         (b["box"]['x'], b["box"]['y'], b["box"]['z']) if b.get('box') else
                         (1, 1, 1)}
'''
    for b in all_decor
)
print(classes)



        # self._texture_id = "{os.path.splitext(os.path.basename(b["renderable"]["lodList"][0]["subMeshList"][0]["textureList"][0]))[0]
        #                      if b["renderable"]["lodList"][0].get("subMeshList") else
        #                      os.path.splitext(os.path.basename(b["renderable"]["lodList"][0]["subMeshMap"][0]["textureList"][0]))[0]}"


# object_list = {}
# block_list = {}

# path_to_steam = r"C:\Program Files (x86)\Steam"

# creative_shapesets = os.listdir(f"{path_to_steam}/steamapps/common/Scrap Mechanic/Data/Objects/Database/ShapeSets")
# survival_shapesets = os.listdir(f"{path_to_steam}/steamapps/common/Scrap Mechanic/Survival/Objects/Database/ShapeSets")

# colors = {}

# partslist = {}

# banned_objects = ["Piston","Handbook","Spud_Gun","Lift","Connect_Tool","Off_Road_Suspension","Sport_Suspension","Paint_Tool","Sledgehammer","Weld_Tool"]

# for file in creative_shapesets:
#     with open(f"{path_to_steam}/steamapps/common/Scrap Mechanic/Data/Objects/Database/ShapeSets/{file}","r") as file_json:
#         blocks = json.loads(file_json.read())
#         pp(blocks)

#         # try:
#         #     if "blocks" in file:
#         #         for each in blocks["blockList"]:
#         #             partslist[each["uuid"]] = {}
#         #             partslist[each["uuid"]]["name"] = each["name"]
#         #             partslist[each["uuid"]]["color"] = each["color"]
#         #     else:
#         #         for each in blocks["partList"]:
#         #             partslist[each["uuid"]] = {}
#         #             partslist[each["uuid"]]["name"] = each["name"]
#         #             partslist[each["uuid"]]["color"] = each["color"]
#         # except:
#         #     print("error",each)

# for file in survival_shapesets:
#     with open(f"{path_to_steam}/steamapps/common/Scrap Mechanic/Survival/Objects/Database/ShapeSets/{file}","r") as file_json:
#         blocks = json.loads(file_json.read())
#         # pp(blocks)

#         # try:
#         #     if "blocks" in file:
#         #         for each in blocks["blockList"]:
#         #             partslist[each["uuid"]] = {}
#         #             partslist[each["uuid"]]["name"] = each["name"]
#         #             partslist[each["uuid"]]["color"] = each["color"]
#         #     else:
#         #         for each in blocks["partList"]:
#         #             partslist[each["uuid"]] = {}
#         #             partslist[each["uuid"]]["name"] = each["name"]
#         #             partslist[each["uuid"]]["color"] = each["color"]
#         # except:
#         #     print("error",each)



# with open(f"{path_to_steam}/steamapps/common/Scrap Mechanic/Data/Gui/Language/English/InventoryItemDescriptions.json","r") as survival_items:
#     items = json.loads(survival_items.read())
#     # pp(items)

#     # for each in items:
#     #     block = items[each]["title"]
#     #     block = block.replace(" ", "_")
#     #     block = block.replace("-", "_")
#     #     block = block.replace("'","")
#     #     block = block.replace(":","")
#     #     block = block.replace("(","")
#     #     block = block.replace(")","")
#     #     block = block.replace(".","_")
#     #     try:
#     #         if "_Block" in block or block == "Net_Fence":
#     #             block_list[block] = {}
#     #             block_list[block]["uuid"] = each
#     #             block_list[block]["color"] = partslist[each]["color"]
#     #             partslist[each]["name"] = block
#     #             print(partslist[each])
#     #         elif block not in banned_objects:
#     #             object_list[block] = {}
#     #             object_list[block]["uuid"] = each
#     #             object_list[block]["color"] = partslist[each]["color"]
#     #             partslist[each]["name"] = block
#     #             print(partslist[each])
#     #     except:
#     #         print("error",block)

# with open(f"{path_to_steam}/steamapps/common/Scrap Mechanic/Survival/Gui/Language/English/inventoryDescriptions.json","r") as survival_items:
#     items = json.loads(survival_items.read())
#     # for each in items:
#     #     block = items[each]["title"]
#     #     block = block.replace(" ", "_")
#     #     block = block.replace("-", "_")
#     #     block = block.replace("'","")
#     #     block = block.replace(":","")
#     #     block = block.replace("(","")
#     #     block = block.replace(")","")
#     #     block = block.replace(".","_")
#     #     try:
#     #         if "_Block" in block or block == "Net_Fence":
#     #             block_list[block] = {}
#     #             block_list[block]["uuid"] = each
#     #             block_list[block]["color"] = partslist[each]["color"]
#     #             partslist[each]["name"] = block
#     #             print(partslist[each])
#     #         elif block not in banned_objects:
#     #             object_list[block] = {}
#     #             object_list[block]["uuid"] = each
#     #             object_list[block]["color"] = partslist[each]["color"]
#     #             partslist[each]["name"] = block
#     #             print(partslist[each])
#     #     except:
#     #         print("error",block)

# with open("block_list.py", "w") as block_list_json:
#     block_list_json.write('class objects:\n')
#     block_list_json.write('    def __init__(self):\n')
#     for block in object_list:
#         block_list_json.write(f'        self.{block} = {object_list[block]}\n')
#     block_list_json.write('class blocks:\n')
#     block_list_json.write('    def __init__(self):\n')
#     for block in block_list:
#         block_list_json.write(f'        self.{block} = {block_list[block]}\n')





