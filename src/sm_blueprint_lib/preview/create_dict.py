import json
from pprint import pp
import glob
from os.path import join


def create_dictionary_uuid_to_obj():
    """
    We need a way to associate each Part's UUID to a OBJ file so it is renderable,
    this function joints the information from interactive.json (for now) and all the
    *.rend files that were taken from the game to achieve that.
    """
    with open(r"src\sm_blueprint_lib\preview\relations\interactive.json") as fp:
        interactive = json.load(fp)

    for item in interactive["partList"]:
        item["renderable"] = item["renderable"].split("/")[-1]

    uuid_to_obj = {}

    for item in interactive["partList"]:
        try:
            with open(join(r"src\sm_blueprint_lib\preview\relations", item["renderable"])) as rend_file:
                rend = json.load(rend_file)
                obj = rend["lodList"][0]["mesh"].split("/")[-1].replace("fbx", "obj")
                uuid_to_obj[item["uuid"]] = obj
        except FileNotFoundError:
            pass

    return uuid_to_obj
