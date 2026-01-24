from itertools import chain
from os import PathLike
from os.path import join
from dataclasses import astuple
import numpy as np
from pprint import pp
import json

import moderngl as mgl
import glm
import pyassimp

from ..camera import Camera
from ..shader_program import ShaderProgram
from ..texture import Texture
from ...bases.parts.basepart import BasePart
from ...parts.logicgate import LogicGate


class LogicGateRenderer:
    def __init__(self, context: mgl.Context, shaders_dir: PathLike, game_dir: PathLike) -> None:
        self.context = context
        self.shader = ShaderProgram(
            self.context,
            join(shaders_dir, "logicgatebody"),
            join(shaders_dir, "logicgatehead"),
        )
        GAME_DATA = join(game_dir, "Data")
        rend_file = join(GAME_DATA, "Objects", "Renderable", "Interactive", "obj_interactive_logicgate.rend")

        with open(rend_file) as fp:
            rend_json = json.load(fp)

        mesh_file = rend_json["lodList"][0]["mesh"].replace("$GAME_DATA", GAME_DATA)
        texture_file = rend_json["lodList"][0]["subMeshMap"]["logicgate"]["textureList"][0].replace("$GAME_DATA", GAME_DATA)
        
        self.texture = Texture(
            self.context,
            texture_file,
        )

        with pyassimp.load(mesh_file) as scene:
            body = scene.meshes[0]
            screen = scene.meshes[1]


        self.vertices_body = self.context.buffer(np.concatenate((body.texturecoords[0, :, :2],
                                                                 body.normals,
                                                                 body.vertices), axis=1).astype(np.float32))
        self.faces_body = self.context.buffer(body.faces)

        self.vertices_screen = self.context.buffer(np.concatenate((screen.texturecoords[0, :, :2],
                                                                   screen.normals,
                                                                   screen.vertices), axis=1).astype(np.float32))
        self.faces_screen = self.context.buffer(screen.faces)

        self.models = self.context.buffer(reserve=1, dynamic=True)
        self.colors = self.context.buffer(reserve=1, dynamic=True)
        self.states = self.context.buffer(reserve=1, dynamic=True)
        self.types = self.context.buffer(reserve=1, dynamic=True)
        self.alpha = self.context.buffer(reserve=1, dynamic=True)

        self.vao_content_body = [
            (self.vertices_body, "2f 3f 3f", "uv", "normal", "vert"),
            (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
            (self.colors, "3f /i", "color"),
            (self.states, "1f /i", "state"),
            (self.alpha, "1f /i", "alpha"),
        ]
        self.vao_content_screen = [
            (self.vertices_screen, "2f 3f 3f", "uv", "normal", "vert"),
            (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
            (self.colors, "3f /i", "color"),
            (self.states, "1f /i", "state"),
            (self.types, "1f /i", "type"),
            (self.alpha, "1f /i", "alpha"),
        ]
        self.vao_body = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_body,
            skip_errors=False,
            index_buffer=self.faces_body
        )
        self.vao_screen = self.context.vertex_array(
            self.shader.programs[1],
            self.vao_content_screen,
            skip_errors=False,
            index_buffer=self.faces_screen
        )


    def render(self, camera: Camera, parts: list[BasePart]):
        instances: list[LogicGate] = []
        for part in parts:
            if isinstance(part, LogicGate):
                instances.append(part)

        if not instances:
            return
        
        models = np.array([self.get_model(logicgate).to_list()
                           for logicgate in instances], dtype="f4")
        self.models.orphan(models.nbytes)
        self.models.write(models)

        colors = np.array([self.get_color(logicgate).to_list()
                          for logicgate in instances], dtype="f4")
        self.colors.orphan(colors.nbytes)
        self.colors.write(colors)

        states = np.array([self.get_state(logicgate)
                          for logicgate in instances], dtype="f4")
        self.states.orphan(states.nbytes)
        self.states.write(states)

        types = np.array([self.get_type(logicgate)
                         for logicgate in instances], dtype="f4")
        self.types.orphan(types.nbytes)
        self.types.write(types)

        alpha = np.array([logicgate.a for logicgate in instances], dtype="f4")
        self.alpha.orphan(alpha.nbytes)
        self.alpha.write(alpha)

        self.shader.programs[0]["V"] = chain(*camera.view().to_tuple())
        self.shader.programs[0]["P"] = chain(*camera.projection().to_tuple())
        self.shader.programs[0]["tex"] = 0
        self.texture.textures["obj_interactive_logicgate_dif"].use(0)
        self.vao_body.render(instances=len(instances))

        self.shader.programs[1]["V"] = chain(*camera.view().to_tuple())
        self.shader.programs[1]["P"] = chain(*camera.projection().to_tuple())
        self.shader.programs[1]["tex"] = 1
        self.texture.textures["obj_interactive_logicgate_dif"].use(1)
        self.vao_screen.render(instances=len(instances))

    def get_type(self, logicgate: LogicGate):
        return logicgate.controller.mode

    def get_state(self, logicgate: LogicGate):
        return logicgate.controller.active

    def get_color(self, logicgate: LogicGate):
        c = int(logicgate.color, 16)
        return glm.vec3(
            (c >> 16) & 0xFF,
            (c >> 8) & 0xFF,
            (c >> 0) & 0xFF,
        ) / 0xFF

    def get_model(self, logicgate: LogicGate):
        pos = astuple(logicgate.pos)
        return (
            glm.translate(glm.vec3(pos))
            *
            self.get_rot(logicgate)
        )

    def get_rot(self, logicgate: LogicGate):
        x = glm.vec3()
        z = glm.vec3()
        x[abs(logicgate.xaxis) - 1] = glm.sign(logicgate.xaxis)
        z[abs(logicgate.zaxis) - 1] = glm.sign(logicgate.zaxis)
        y = glm.cross(z, x)
        return glm.mat4_cast(glm.quatLookAtLH(z, y)) * glm.translate(glm.vec3(0.5))
