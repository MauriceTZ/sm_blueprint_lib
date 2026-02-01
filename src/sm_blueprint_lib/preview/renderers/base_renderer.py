from itertools import chain
from os import PathLike
from os.path import join, basename
from dataclasses import astuple
import numpy as np
from pprint import pp, pformat
import json
import re
import logging
from itertools import groupby

import pygame as pg
import moderngl as mgl
import glm

from ..camera import Camera
from ...bases import *
from ...parts import *
from ...constants import SHAPEID


logger = logging.getLogger("Rendering")
logging.basicConfig(level=logging.INFO)

class BaseRenderer:
    TexturesCache = {}
    ModelsCache = {}
    Parts = {}
    AllInventoryDescriptions = {}
    CubeVertexData = np.array([
        # Front Face (+Z)
        0.0, 0.0,   0.0,  0.0,  1.0,   -0.5, -0.5,  0.5, # Bottom-Left
        1.0, 0.0,   0.0,  0.0,  1.0,    0.5, -0.5,  0.5, # Bottom-Right
        1.0, 1.0,   0.0,  0.0,  1.0,    0.5,  0.5,  0.5, # Top-Right
        0.0, 1.0,   0.0,  0.0,  1.0,   -0.5,  0.5,  0.5, # Top-Left

        # Back Face (-Z)
        0.0, 0.0,   0.0,  0.0, -1.0,    0.5, -0.5, -0.5, 
        1.0, 0.0,   0.0,  0.0, -1.0,   -0.5, -0.5, -0.5, 
        1.0, 1.0,   0.0,  0.0, -1.0,   -0.5,  0.5, -0.5, 
        0.0, 1.0,   0.0,  0.0, -1.0,    0.5,  0.5, -0.5, 

        # Top Face (+Y)
        0.0, 0.0,   0.0,  1.0,  0.0,   -0.5,  0.5,  0.5, 
        1.0, 0.0,   0.0,  1.0,  0.0,    0.5,  0.5,  0.5, 
        1.0, 1.0,   0.0,  1.0,  0.0,    0.5,  0.5, -0.5, 
        0.0, 1.0,   0.0,  1.0,  0.0,   -0.5,  0.5, -0.5, 

        # Bottom Face (-Y)
        0.0, 0.0,   0.0, -1.0,  0.0,   -0.5, -0.5, -0.5, 
        1.0, 0.0,   0.0, -1.0,  0.0,    0.5, -0.5, -0.5, 
        1.0, 1.0,   0.0, -1.0,  0.0,    0.5, -0.5,  0.5, 
        0.0, 1.0,   0.0, -1.0,  0.0,   -0.5, -0.5,  0.5, 

        # Right Face (+X)
        0.0, 0.0,   1.0,  0.0,  0.0,    0.5, -0.5,  0.5, 
        1.0, 0.0,   1.0,  0.0,  0.0,    0.5, -0.5, -0.5, 
        1.0, 1.0,   1.0,  0.0,  0.0,    0.5,  0.5, -0.5, 
        0.0, 1.0,   1.0,  0.0,  0.0,    0.5,  0.5,  0.5, 

        # Left Face (-X)
        0.0, 0.0,  -1.0,  0.0,  0.0,   -0.5, -0.5, -0.5, 
        1.0, 0.0,  -1.0,  0.0,  0.0,   -0.5, -0.5,  0.5, 
        1.0, 1.0,  -1.0,  0.0,  0.0,   -0.5,  0.5,  0.5, 
        0.0, 1.0,  -1.0,  0.0,  0.0,   -0.5,  0.5, -0.5, 
    ], dtype=np.float32)

    CubeFaces = np.array([
        # Front
        [0,  1,  2], [0,  2,  3],
        # Back
        [4,  5,  6], [4,  6,  7],
        # Top
        [8,  9, 10], [8, 10, 11],
        # Bottom
        [12, 13, 14], [12, 14, 15],
        # Right
        [16, 17, 18], [16, 18, 19],
        # Left
        [20, 21, 22], [20, 22, 23]
    ], dtype=np.int32)


    def __init__(self, context: mgl.Context, game_dir: PathLike, all_parts: list[BasePart]) -> None:
        # Load pyassimp from the game (Windows only...)
        self.all_parts = all_parts
        from os import environ, pathsep
        environ["PATH"] += pathsep + join(game_dir, "Release")
        global pyassimp
        import pyassimp
        self.context = context
        vertex_shader = """\
            #version 450 core

            layout (location = 0) in vec2 uv;
            layout (location = 1) in vec3 normal;
            layout (location = 2) in vec3 vert;

            layout (location = 3) in vec4 M0;
            layout (location = 4) in vec4 M1;
            layout (location = 5) in vec4 M2;
            layout (location = 6) in vec4 M3;

            layout (location = 7) in vec3 color;
            layout (location = 8) in vec2 uv_offset;

            uniform mat4 V;
            uniform mat4 P;
            uniform float tiling;

            out vec2 UV;
            out vec3 NORMAL;
            out vec3 COLOR;

            void main() {
                // 1. Reconstruct Matrix
                mat4 M = mat4(M0, M1, M2, M3);
                
                // 2. Extract Scale from the Matrix Columns
                // The length of the columns tells us how much the object is stretched
                float scale_x = length(M0.xyz);
                float scale_y = length(M1.xyz);
                float scale_z = length(M2.xyz);

                // 3. Determine Tiling based on Face Normal
                // We use abs(normal) because a face pointing Left (-1,0,0) 
                // should behave the same as Right (1,0,0) regarding sizing.
                vec3 n = abs(normal);
                
                vec2 tile_factor = vec2(1.0, 1.0);

                // LOGIC:
                // If Normal is X (Side face) -> Tile by Depth (Z) and Height (Y)
                // If Normal is Y (Top face)  -> Tile by Width (X) and Depth (Z)
                // If Normal is Z (Front face)-> Tile by Width (X) and Height (Y)
                
                if (n.x > 0.5) {
                    tile_factor = vec2(scale_z, scale_y);
                } else if (n.y > 0.5) {
                    tile_factor = vec2(scale_x, scale_z);
                } else {
                    tile_factor = vec2(scale_x, scale_y);
                }

                // 4. Apply Tiling to UVs
                // We multiply the original 0-1 UVs by the scale size.
                UV = (uv * tile_factor) / tiling + uv_offset;
                
                NORMAL = normal;
                COLOR = color;
                gl_Position = P * V * M * vec4(vert, 1.0);
            }
        """
        fragment_shader = """\
            #version 450 core

            in vec2 UV;
            in vec3 COLOR;

            uniform sampler2D tex;

            out vec4 output_color;

            void main()
            {
                vec4 dif = texture(tex, UV);
                output_color = vec4(dif.xyz * dif.a + COLOR*(1 - dif.a), 1);
            }
        """
        self.program = self.context.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        self.models = self.context.buffer(reserve=1000, dynamic=True)
        self.colors = self.context.buffer(reserve=1000, dynamic=True)
        self.uv_offset = self.context.buffer(reserve=1000, dynamic=True)
        self.CubeVertexDataBuffer = self.context.buffer(self.CubeVertexData)
        self.CubeFacesBuffer = self.context.buffer(self.CubeFaces)
        self.CubeVao = self.context.vertex_array(
            self.program,
            [(self.CubeVertexDataBuffer, "2f 3f 3f", "uv", "normal", "vert"),
             (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
             (self.colors, "3f /i", "color"),
             (self.uv_offset, "2f /i", "uv_offset")],
            skip_errors=False,
            index_buffer=self.CubeFacesBuffer,
            index_element_size=4
        )
        self.GAME_DATA = join(game_dir, "Data")
        self.SURVIVAL_DATA = join(game_dir, "Survival")
        inventory_item_descriptions_json_path = join(self.GAME_DATA, "Gui", "Language", "English", "InventoryItemDescriptions.json")
        survival_inventory_descriptions_json_path = join(self.SURVIVAL_DATA, "Gui", "Language", "English", "inventoryDescriptions.json")
        with open(inventory_item_descriptions_json_path) as fp:
            inventory_item_descriptions_json = parse_json_with_comments(fp)
        with open(survival_inventory_descriptions_json_path) as fp:
            survival_inventory_descriptions_json = parse_json_with_comments(fp)
        # self.AllInventoryDescriptions = {}
        self.AllInventoryDescriptions.update(inventory_item_descriptions_json)
        self.AllInventoryDescriptions.update(survival_inventory_descriptions_json)
        with open(join(self.GAME_DATA, "Objects", "Database", "shapesets.json")) as fp:
            shapesets = parse_json_with_comments(fp)
        for shapeset_file in shapesets["shapeSetList"]:
            try:
                with open(self.resolve(shapeset_file)) as fp:
                    shapeset = parse_json_with_comments(fp)
                for list_name, objects in shapeset.items():
                    for object in objects:
                        if object["uuid"] not in [p.shapeId for p in self.all_parts]:
                            continue
                        object["humanName"] = self.AllInventoryDescriptions[object["uuid"]]["title"] if self.AllInventoryDescriptions.get(object["uuid"]) else None
                        if isinstance(renderable := object.get("renderable"), str):
                            with open(self.resolve(renderable)) as fp:
                                object["renderable"] = parse_json_with_comments(fp)
                        self.Parts[object["uuid"]] = self.Parts.get(object["uuid"], {"vaos": {}, "textures": {}, "humanName": object["humanName"],})
                        logger.info("Processing object %s, uuid=%s", object.get("name") or object["humanName"], object["uuid"])
                        try:
                            self.process_object(list_name, object)
                        except Exception as e:
                            logger.exception("\n"+pformat(object))
            except FileNotFoundError as e:
                logger.warning(e)

    def process_object(self, list_name, object):
        if list_name == "partList":
            lod0 = object["renderable"]["lodList"][0]

            if not (lod0["mesh"].lower().endswith(".fbx") or lod0["mesh"].lower().endswith(".mesh")):
                return logger.warning("Mesh type not supported (yet).")
            
            model = self.load_model(self.resolve(lod0["mesh"]))
            for mesh in model.meshes:
                if mesh.material.properties["name"] == "lightcone_mat" or mesh.material.properties["name"] == "lightflare_mat":
                    continue
                model_vertex_buffer = self.context.buffer(np.concatenate((mesh.texturecoords[0, :, :2],
                                                                          mesh.normals,
                                                                          mesh.vertices), axis=1).astype(np.float32))
                model_faces_buffer = self.context.buffer(mesh.faces)
                model_vao = self.context.vertex_array(
                    self.program,
                    [(model_vertex_buffer, "2f 3f 3f", "uv", "normal", "vert"),
                        (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
                        (self.colors, "3f /i", "color"),
                        (self.uv_offset, "2f /i", "uv_offset")],
                    skip_errors=False,
                    index_buffer=model_faces_buffer
                )
                self.Parts[object["uuid"]]["vaos"][mesh.material.properties["name"]] = model_vao
    
            if (subMeshMap := lod0.get("subMeshMap")):
                for name, material_texture in subMeshMap.items():
                    if name == "lightcone_mat" or name == "lightflare_mat":
                        continue
                    self.Parts[object["uuid"]]["textures"][name] = self.load_texture(self.resolve(material_texture["textureList"][0]))

            elif (subMeshList := lod0.get("subMeshList")):
                for index, material_texture in enumerate(subMeshList):
                    self.Parts[object["uuid"]]["textures"][index] = self.load_texture(self.resolve(material_texture["textureList"][0]))
            if object["uuid"] == "7bc20d55-6b49-450c-830c-16282ce7fb2d":
                self.Parts[object["uuid"]]["textures"][0], self.Parts[object["uuid"]]["textures"][1] = self.Parts[object["uuid"]]["textures"][1], self.Parts[object["uuid"]]["textures"][0]
        elif list_name == "blockList":
            self.Parts[object["uuid"]]["vaos"]["cube"] = self.CubeVao
            self.Parts[object["uuid"]]["textures"][0] = self.load_texture(self.resolve(object["dif"]))

    def resolve(self, rel_path):
        return rel_path.replace("$GAME_DATA", self.GAME_DATA).replace("$SURVIVAL_DATA", self.SURVIVAL_DATA)
    
    def load_texture(self, path: PathLike):
        if (texture := self.TexturesCache.get(basename(path))):
            return texture
        texture = pg.image.load(path).convert_alpha()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.context.texture(
            size=texture.get_size(), components=4,
            data=pg.image.tostring(texture, "RGBA"))
        texture.filter = mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR
        texture.build_mipmaps(max_level=10)
        # texture.anisotropy = 4
        self.TexturesCache[basename(path)] = texture
        return texture

    def load_model(self, path: PathLike):
        if (model := self.ModelsCache.get(basename(path))):
            return model
        with pyassimp.load(path) as m:
            self.ModelsCache[basename(path)] = m
            return m

    def render(self, camera: Camera, parts: list[BasePart]):
        instances: list[BasePart] = [p
                                            for p in parts
                                            if self.Parts.get(p.shapeId) and self.Parts[p.shapeId]["vaos"] != {}]

        if not instances:
            return

        for uuid, g in groupby(instances, key=lambda p: p.shapeId):
            if not (cls := SHAPEID.SHAPEID_TO_CLASS.get(uuid)):
                continue
            instance_group = list(g)

            models = np.array([self.get_model(normalpart).to_list()
                            for normalpart in instance_group], dtype="f4")
            self.models.orphan(models.nbytes)
            self.models.write(models)

            colors = np.array([self.get_color(normalpart).to_list()
                            for normalpart in instance_group], dtype="f4")
            self.colors.orphan(colors.nbytes)
            self.colors.write(colors)

            self.program["V"] = chain(*camera.view().to_tuple())
            self.program["P"] = chain(*camera.projection().to_tuple())
            self.program["tex"] = 0
            self.program["tiling"] = 1

            if issubclass(cls, BaseBoundablePart):
                self.program["tiling"] = instance_group[0]._tiling
                uv_offset = np.array([(0, 0) for _ in instance_group], dtype="f4")
                self.uv_offset.orphan(uv_offset.nbytes)
                self.uv_offset.write(uv_offset)
                for i, (vao_k, texture_k) in enumerate(zip(self.Parts[uuid]["vaos"].keys(), self.Parts[uuid]["textures"].keys())):
                    self.Parts[uuid]["textures"][i].use(0)
                    self.Parts[uuid]["vaos"][vao_k].render(instances=len(instance_group))
            elif issubclass(cls, LogicGate):
                uv_offset = np.array([(logicgate.controller.mode * 0.1666670, logicgate.controller.active * -0.16450)
                                      for logicgate in instance_group], dtype="f4")
                self.uv_offset.orphan(uv_offset.nbytes)
                self.uv_offset.write(uv_offset)
                self.Parts[uuid]["textures"]["screen"].use(0)
                self.Parts[uuid]["vaos"]["screen"].render(instances=len(instance_group))

                uv_offset = np.array([(0, 0) for _ in instance_group], dtype="f4")
                self.uv_offset.orphan(uv_offset.nbytes)
                self.uv_offset.write(uv_offset)
                self.Parts[uuid]["textures"]["logicgate"].use(0)
                self.Parts[uuid]["vaos"]["logicgate"].render(instances=len(instance_group))
            else:
                uv_offset = np.array([(0, 0) for _ in instance_group], dtype="f4")
                self.uv_offset.orphan(uv_offset.nbytes)
                self.uv_offset.write(uv_offset)
                for i, (vao_k, texture_k) in enumerate(zip(self.Parts[uuid]["vaos"].keys(), self.Parts[uuid]["textures"].keys())):
                    (self.Parts[uuid]["textures"].get(vao_k) or self.Parts[uuid]["textures"][i]).use(0)
                    self.Parts[uuid]["vaos"][vao_k].render(instances=len(instance_group))

    def get_color(self, part: BasePart):
        c = int(part.color, 16)
        return glm.vec3(
            (c >> 16) & 0xFF,
            (c >> 8) & 0xFF,
            (c >> 0) & 0xFF,
        ) / 0xFF

    def get_model(self, part: BasePart | BaseJoint):
        pos = astuple(part.pos if isinstance(part, BasePart) else part.posA)
        return (
            glm.translate(glm.vec3(pos))
            *
            (glm.scale(glm.vec3(*astuple(part.bounds)))
             if isinstance(part, BaseBoundablePart) else
             1)
            *
            self.get_rot(part)
        )

    def get_rot(self, part: BasePart):
        x = glm.vec3()
        z = glm.vec3()
        xaxis = part.xaxis if isinstance(part, BasePart) else part.xaxisA
        zaxis = part.zaxis if isinstance(part, BasePart) else part.zaxisA
        x[abs(xaxis) - 1] = glm.sign(xaxis)
        z[abs(zaxis) - 1] = glm.sign(zaxis)
        y = glm.cross(z, x)
        return glm.mat4_cast(glm.quatLookAtLH(z, y)) * glm.translate(part._box/2) * glm.translate(part._offset)

def parse_json_with_comments(fp):
    # *This was made by Gemini
    # This regex matches strings (ignoring content inside) OR comments
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
    
    def replacer(match):
        s = match.group(0)
        # If the match starts with '/', it's a comment -> replace with space
        if s.startswith('/'):
            return " " 
        # Otherwise, it's a string literal -> return it as is
        else:
            return s
            
    clean_json = re.sub(pattern, replacer, fp.read())
    return json.loads(clean_json)