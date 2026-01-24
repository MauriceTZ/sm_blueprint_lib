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
from ...bases.parts.baseboundablepart import BaseBoundablePart


class BlockRenderer:
    def __init__(self, context: mgl.Context, shaders_dir: PathLike, game_dir: PathLike, meshes_dir: PathLike) -> None:
        self.context = context
        self.shader = ShaderProgram(
            self.context,
            join(shaders_dir, "tileblock")
        )

        GAME_DATA = join(game_dir, "Data")
        SURVIVAL_DATA = join(game_dir, "Survival")

        blocks_json_path = join(GAME_DATA, "Objects", "Database", "ShapeSets", "blocks.json")
        survival_blocks_json_path = join(SURVIVAL_DATA, "Objects", "Database", "ShapeSets", "blocks.json")
        with open(blocks_json_path) as fp:
            blocks_json = json.load(fp)
        with open(survival_blocks_json_path) as fp:
            survival_blocks_json = json.load(fp)
        all_blocks = blocks_json["blockList"] + survival_blocks_json["blockList"]

        self.texture = Texture(
            self.context,
            *[b["dif"].replace("$GAME_DATA", GAME_DATA).replace("$SURVIVAL_DATA", SURVIVAL_DATA) for b in all_blocks],
        )
        # Yeah im sorry i was lazy...
        with pyassimp.load(join(meshes_dir, "block_front.obj")) as scene:
            block_front = scene.meshes[0]
        with pyassimp.load(join(meshes_dir, "block_back.obj")) as scene:
            block_back = scene.meshes[0]
        with pyassimp.load(join(meshes_dir, "block_top.obj")) as scene:
            block_top = scene.meshes[0]
        with pyassimp.load(join(meshes_dir, "block_botton.obj")) as scene:
            block_botton = scene.meshes[0]
        with pyassimp.load(join(meshes_dir, "block_right.obj")) as scene:
            block_right = scene.meshes[0]
        with pyassimp.load(join(meshes_dir, "block_left.obj")) as scene:
            block_left = scene.meshes[0]

        front = np.concatenate((block_front.texturecoords[0, :, :2],
                                block_front.normals,
                                block_front.vertices), axis=1)[block_front.faces]
        back = np.concatenate((block_back.texturecoords[0, :, :2],
                               block_back.normals,
                               block_back.vertices), axis=1)[block_back.faces]
        top = np.concatenate((block_top.texturecoords[0, :, :2],
                              block_top.normals,
                              block_top.vertices), axis=1)[block_top.faces]
        botton = np.concatenate((block_botton.texturecoords[0, :, :2],
                                 block_botton.normals,
                                 block_botton.vertices), axis=1)[block_botton.faces]
        right = np.concatenate((block_right.texturecoords[0, :, :2],
                                block_right.normals,
                                block_right.vertices), axis=1)[block_right.faces]
        left = np.concatenate((block_left.texturecoords[0, :, :2],
                               block_left.normals,
                               block_left.vertices), axis=1)[block_left.faces]

        self.vertices_front = self.context.buffer(front.astype(np.float32))
        self.vertices_back = self.context.buffer(back.astype(np.float32))
        self.vertices_top = self.context.buffer(top.astype(np.float32))
        self.vertices_botton = self.context.buffer(botton.astype(np.float32))
        self.vertices_right = self.context.buffer(right.astype(np.float32))
        self.vertices_left = self.context.buffer(left.astype(np.float32))

        self.vao_content_front = [
            (self.vertices_front, "2f 3f 3f", "uv", "normal", "vert"),
        ]
        self.vao_front = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_front,
            skip_errors=False 
        )
        self.vao_content_back = [
            (self.vertices_back, "2f 3f 3f", "uv", "normal", "vert"),
        ]
        self.vao_back = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_back,
            skip_errors=False 
        )
        self.vao_content_top = [
            (self.vertices_top, "2f 3f 3f", "uv", "normal", "vert"),
        ]
        self.vao_top = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_top,
            skip_errors=False 
        )
        self.vao_content_botton = [
            (self.vertices_botton, "2f 3f 3f", "uv", "normal", "vert"),
        ]
        self.vao_botton = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_botton,
            skip_errors=False 
        )
        self.vao_content_right = [
            (self.vertices_right, "2f 3f 3f", "uv", "normal", "vert"),
        ]
        self.vao_right = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_right,
            skip_errors=False 
        )
        self.vao_content_left = [
            (self.vertices_left, "2f 3f 3f", "uv", "normal", "vert"),
        ]
        self.vao_left = self.context.vertex_array(
            self.shader.programs[0],
            self.vao_content_left,
            skip_errors=False 
        )

    def render(self, camera: Camera, parts: list[BasePart]):
        instances: list[BaseBoundablePart] = []
        for part in parts:
            if isinstance(part, BaseBoundablePart):
                instances.append(part)

        if not instances:
            return

        for instance in instances:
            self.shader.programs[0]["M"] = chain(*self.get_model(instance).to_tuple())
            self.shader.programs[0]["V"] = chain(*camera.view().to_tuple())
            self.shader.programs[0]["P"] = chain(*camera.projection().to_tuple())
            self.shader.programs[0]["color"] = self.get_color(instance).to_tuple()
            self.shader.programs[0]["alpha"] = instance.a
            self.shader.programs[0]["tex"] = 0
            self.texture.textures[instance._texture_id].use(0)

            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.x, instance.bounds.z) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.x, instance.pos.z) / instance._tiling).to_tuple()
            self.vao_front.render()
            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.x, instance.bounds.z) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.x, instance.pos.z) / instance._tiling).to_tuple()
            self.vao_back.render()

            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.x, instance.bounds.y) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.x, instance.pos.y) / instance._tiling).to_tuple()
            self.vao_top.render()
            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.x, instance.bounds.y) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.x, instance.pos.y) / instance._tiling).to_tuple()
            self.vao_botton.render()

            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.y, instance.bounds.z) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.y, instance.pos.z) / instance._tiling).to_tuple()
            self.vao_right.render()
            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.x, instance.bounds.z) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.y, instance.pos.z) / instance._tiling).to_tuple()
            self.vao_right.render()

            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.y, instance.bounds.z) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.y, instance.pos.z) / instance._tiling).to_tuple()
            self.vao_left.render()
            self.shader.programs[0]["bounds"] = (glm.vec2(instance.bounds.x, instance.bounds.z) / instance._tiling).to_tuple()
            self.shader.programs[0]["offset"] = (glm.vec2(instance.pos.y, instance.pos.z) / instance._tiling).to_tuple()
            self.vao_left.render()

    def get_color(self, block: BaseBoundablePart):
        c = int(block.color, 16)
        return glm.vec3(
            (c >> 16) & 0xFF,
            (c >> 8) & 0xFF,
            (c >> 0) & 0xFF,
        ) / 0xFF

    def get_model(self, block: BaseBoundablePart):
        pos = astuple(block.pos)
        return (
            glm.translate(glm.vec3(pos))
            *
            glm.scale(astuple(block.bounds))
            *
            self.get_rot(block)
        )

    def get_rot(self, block: BaseBoundablePart):
        offset = glm.translate(glm.vec3(0.5))
        x = glm.vec3()
        z = glm.vec3()
        x[abs(block.xaxis) - 1] = glm.sign(block.xaxis)
        z[abs(block.zaxis) - 1] = glm.sign(block.zaxis)
        y = glm.cross(z, x)
        return glm.mat4_cast(glm.quatLookAtLH(z, y)) * offset * glm.rotate(glm.half_pi(), (1, 0, 0))
