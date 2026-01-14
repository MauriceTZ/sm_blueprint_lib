import pygame as pg
import moderngl as mgl
from os import PathLike


class Texture:
    def __init__(self, context: mgl.Context, *tex_paths: PathLike) -> None:
        self.context = context
        self.textures = [self.get_texture(path) for path in tex_paths]

    def get_texture(self, path: PathLike):
        texture = pg.image.load(path).convert_alpha()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.context.texture(
            size=texture.get_size(), components=4,
            data=pg.image.tostring(texture, "RGBA"))
        texture.filter = mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR
        texture.build_mipmaps()
        texture.anisotropy = 4
        return texture

    def destroy(self):
        for tex in self.textures:
            tex.release()
