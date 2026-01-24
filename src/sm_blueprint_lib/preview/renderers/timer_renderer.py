from itertools import chain
from os import PathLike
from os.path import join
from dataclasses import astuple
import numpy as np
import json
from pprint import pp

import moderngl as mgl
import glm
import pyassimp

from ..camera import Camera
from ..shader_program import ShaderProgram
from ..texture import Texture
from ...bases.parts.basepart import BasePart
from ...parts.timer import Timer


class TimerGateRenderer:
    def __init__(self, context: mgl.Context, shaders_dir: PathLike, game_dir: PathLike) -> None:
        self.context = context
        self.shader = ShaderProgram(
            self.context,
            join(shaders_dir, "timerbody"),
            join(shaders_dir, "timerstrip"),
        )

        GAME_DATA = join(game_dir, "Data")
        rend_file = join(GAME_DATA, "Objects", "Renderable", "Interactive", "obj_interactive_timer.rend")

        with open(rend_file) as fp:
            rend_json = json.load(fp)

        mesh_file = rend_json["lodList"][0]["mesh"].replace("$GAME_DATA", GAME_DATA)
        texture_file = rend_json["lodList"][0]["subMeshList"][0]["textureList"][0].replace("$GAME_DATA", GAME_DATA)

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
        self.alpha = self.context.buffer(reserve=1, dynamic=True)

        self.vao_content_body = [
            (self.vertices_body, "2f 3f 3f", "uv", "normal", "vert"),
            (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
            (self.colors, "3f /i", "color"),
            (self.alpha, "1f /i", "alpha"),
        ]
        self.vao_content_screen = [
            (self.vertices_screen, "2f 3f 3f", "uv", "normal", "vert"),
            (self.models, "4f 4f 4f 4f /i", "M0", "M1", "M2", "M3"),
            (self.colors, "3f /i", "color"),
            (self.states, "1f /i", "state"),
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
        instances: list[Timer] = []
        for part in parts:
            if isinstance(part, Timer):
                instances.append(part)

        if not instances:
            return
        
        models = np.array([self.get_model(timer).to_list()
                           for timer in instances], dtype="f4")
        self.models.orphan(models.nbytes)
        self.models.write(models)

        colors = np.array([self.get_color(timer).to_list()
                          for timer in instances], dtype="f4")
        self.colors.orphan(colors.nbytes)
        self.colors.write(colors)

        states = np.array([self.get_state(timer)
                          for timer in instances], dtype="f4")
        self.states.orphan(states.nbytes)
        self.states.write(states)

        alpha = np.array([timer.a for timer in instances], dtype="f4")
        self.alpha.orphan(alpha.nbytes)
        self.alpha.write(alpha)

        self.shader.programs[0]["V"] = chain(*camera.view().to_tuple())
        self.shader.programs[0]["P"] = chain(*camera.projection().to_tuple())
        self.shader.programs[0]["tex"] = 0
        self.texture.textures["obj_interactive_timer_dif"].use(0)
        self.vao_body.render(instances=len(instances))

        self.shader.programs[1]["V"] = chain(*camera.view().to_tuple())
        self.shader.programs[1]["P"] = chain(*camera.projection().to_tuple())
        self.shader.programs[1]["tex"] = 1
        self.texture.textures["obj_interactive_timer_dif"].use(1)
        self.vao_screen.render(instances=len(instances))

    def get_state(self, timer: Timer):
        return timer.controller.active

    def get_color(self, timer: Timer):
        c = int(timer.color, 16)
        return glm.vec3(
            (c >> 16) & 0xFF,
            (c >> 8) & 0xFF,
            (c >> 0) & 0xFF,
        ) / 0xFF

    def get_model(self, timer: Timer):
        pos = astuple(timer.pos)
        return (
            glm.translate(glm.vec3(pos))
            *
            self.get_rot(timer)
        )

    def get_rot(self, timer: Timer):
        x = glm.vec3()
        z = glm.vec3()
        x[abs(timer.xaxis) - 1] = glm.sign(timer.xaxis)
        z[abs(timer.zaxis) - 1] = glm.sign(timer.zaxis)
        y = glm.cross(z, x)
        return glm.mat4_cast(glm.quatLookAtLH(z, y)) * glm.translate(glm.vec3(0.5, 1, 0.5))
