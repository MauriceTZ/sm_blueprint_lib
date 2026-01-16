from itertools import chain
from os import PathLike
from os.path import join
from dataclasses import astuple
import numpy as np

import moderngl as mgl
import glm
import pywavefront

from ..camera import Camera
from ..shader_program import ShaderProgram
from ..texture import Texture
from ...bases.parts.basepart import BasePart
from ...parts.logicgate import LogicGate


class LogicGateRenderer:
    def __init__(self, context: mgl.Context, shaders_dir: PathLike, textures_dir: PathLike, meshes_dir: PathLike) -> None:
        self.context = context
        self.shader = ShaderProgram(
            self.context,
            join(shaders_dir, "logicgatebody"),
            join(shaders_dir, "logicgatehead"),
        )
        self.texture = Texture(
            self.context,
            join(textures_dir, "obj_interactive_logicgate_dif.tga"),
        )
        scene_body = pywavefront.Wavefront(join(meshes_dir, "obj_interactive_logicgate_on_body.obj"))
        scene_screen = pywavefront.Wavefront(join(meshes_dir, "obj_interactive_logicgate_on_screen.obj"))

        body = scene_body.materials["default0"]
        head = scene_screen.materials["screen"]

        print(body.vertex_format)
        self.vertices_body = self.context.buffer(np.array(body.vertices, dtype=np.float32))

        print(head.vertex_format)
        self.vertices_head = self.context.buffer(np.array(head.vertices, dtype=np.float32))

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
        self.vao_content_head = [
            (self.vertices_head, "2f 3f 3f", "uv", "normal", "vert"),
            (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
            (self.colors, "3f /i", "color"),
            (self.states, "1f /i", "state"),
            (self.types, "1f /i", "type"),
            (self.alpha, "1f /i", "alpha"),
        ]
        self.vao_body = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_body,
            skip_errors=False 
        )
        self.vao_head = self.context.vertex_array(
            self.shader.programs[1],
            self.vao_content_head,
            skip_errors=False
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
        self.texture.textures[0].use(0)
        self.vao_body.render(instances=len(instances))

        self.shader.programs[1]["V"] = chain(*camera.view().to_tuple())
        self.shader.programs[1]["P"] = chain(*camera.projection().to_tuple())
        self.shader.programs[1]["tex"] = 1
        self.texture.textures[0].use(1)
        self.vao_head.render(instances=len(instances))

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
        offset = glm.translate(glm.vec3(0.5))
        x = glm.vec3()
        z = glm.vec3()
        x[abs(logicgate.xaxis) - 1] = glm.sign(logicgate.xaxis)
        z[abs(logicgate.zaxis) - 1] = glm.sign(logicgate.zaxis)
        y = glm.cross(z, x)
        return glm.mat4_cast(glm.quatLookAtLH(z, y)) * offset * glm.rotate(glm.half_pi(), (1, 0, 0))
