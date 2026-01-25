from itertools import chain
from os import PathLike
from os.path import join, basename, splitext
from dataclasses import astuple
import numpy as np
from pprint import pp
import json
from itertools import groupby

import moderngl as mgl
import glm
import pyassimp

from ..camera import Camera
from ..shader_program import ShaderProgram
from ..texture import Texture
from ...bases.parts.basepart import BasePart
from ...bases.parts.basenormalpart import BaseNormalPart


class PartRenderer:
    def __init__(self, context: mgl.Context, shaders_dir: PathLike, game_dir: PathLike) -> None:
        self.context = context
        self.shader = ShaderProgram(
            self.context,
            join(shaders_dir, "normalpart"),
        )
        self.UUID_DATA = {}
        GAME_DATA = join(game_dir, "Data")
        SURVIVAL_DATA = join(game_dir, "Survival")
        ShapeSetPath = join(GAME_DATA, "Objects", "Database", "ShapeSets")
        SurvivalShapeSetPath = join(SURVIVAL_DATA, "Objects", "Database", "ShapeSets")

        self.models = self.context.buffer(reserve=1, dynamic=True)
        self.colors = self.context.buffer(reserve=1, dynamic=True)
        self.alpha = self.context.buffer(reserve=1, dynamic=True)

        with open(join(ShapeSetPath, "decor.json")) as fp:
            decor_json = json.load(fp)
        with open(join(ShapeSetPath, "containers.json")) as fp:
            containers_json = json.load(fp)
        with open(join(SurvivalShapeSetPath, "containers.json")) as fp:
            survival_containers_json = json.load(fp)
        all_parts = decor_json["partList"] + containers_json["partList"] + survival_containers_json["partList"]
        for part in all_parts:
            if isinstance(part["renderable"], str):
                with open(part["renderable"].replace("$GAME_DATA", GAME_DATA)) as fp:
                    part["renderable"] = json.load(fp)
        for part in all_parts:
            part_data = part["renderable"]["lodList"][0]
            mesh = part_data["mesh"].replace("$GAME_DATA", GAME_DATA).replace("$SURVIVAL_DATA", SURVIVAL_DATA)
            texture = part_data["subMeshList"][0]["textureList"][0].replace("$GAME_DATA", GAME_DATA).replace("$SURVIVAL_DATA", SURVIVAL_DATA)
            with pyassimp.load(mesh) as m:
                part_model = m.meshes[0]
                model_vertex = self.context.buffer(np.concatenate((part_model.texturecoords[0, :, :2],
                                                                    part_model.normals,
                                                                    part_model.vertices), axis=1).astype(np.float32))
                model_faces = self.context.buffer(part_model.faces)
                model_vao = self.context.vertex_array(
                    self.shader.programs[0],
                    [(model_vertex, "2f 3f 3f", "uv", "normal", "vert"),
                        (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
                        (self.colors, "3f /i", "color"),
                        (self.alpha, "1f /i", "alpha")],
                    skip_errors=False,
                    index_buffer=model_faces
                )
                self.UUID_DATA[part["uuid"]] = {
                    "vao": model_vao,
                    "texture": texture,
                    "texture_id": splitext(basename(texture))[0],
                }
        textures = [v["texture"] for k, v in self.UUID_DATA.items()]
        self.texture = Texture(self.context, *textures)

    def render(self, camera: Camera, parts: list[BasePart]):
        instances: list[BaseNormalPart] = []
        for part in parts:
            if isinstance(part, BaseNormalPart):
                instances.append(part)

        if not instances:
            return
        
        for uuid, g in groupby(sorted(instances, key=lambda i: i.shapeId), key=lambda i: i.shapeId):
            instances_group = list(g)
        
            models = np.array([self.get_model(normalpart).to_list()
                            for normalpart in instances_group], dtype="f4")
            self.models.orphan(models.nbytes)
            self.models.write(models)

            colors = np.array([self.get_color(normalpart).to_list()
                            for normalpart in instances_group], dtype="f4")
            self.colors.orphan(colors.nbytes)
            self.colors.write(colors)

            alpha = np.array([normalpart.a for normalpart in instances_group], dtype="f4")
            self.alpha.orphan(alpha.nbytes)
            self.alpha.write(alpha)

            self.shader.programs[0]["V"] = chain(*camera.view().to_tuple())
            self.shader.programs[0]["P"] = chain(*camera.projection().to_tuple())
            self.shader.programs[0]["tex"] = 0
            self.texture.textures[self.UUID_DATA[uuid]["texture_id"]].use(0)
            self.UUID_DATA[uuid]["vao"].render(instances=len(instances_group))

    def get_color(self, part: BaseNormalPart):
        c = int(part.color, 16)
        return glm.vec3(
            (c >> 16) & 0xFF,
            (c >> 8) & 0xFF,
            (c >> 0) & 0xFF,
        ) / 0xFF

    def get_model(self, part: BaseNormalPart):
        pos = astuple(part.pos)
        return (
            glm.translate(glm.vec3(pos))
            *
            self.get_rot(part)
        )

    def get_rot(self, part: BaseNormalPart):
        x = glm.vec3()
        z = glm.vec3()
        x[abs(part.xaxis) - 1] = glm.sign(part.xaxis)
        z[abs(part.zaxis) - 1] = glm.sign(part.zaxis)
        y = glm.cross(z, x)
        return glm.mat4_cast(glm.quatLookAtLH(z, y)) * glm.translate(part._box/2) * glm.translate(part._offset)
