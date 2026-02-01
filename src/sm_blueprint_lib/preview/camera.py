from typing import Iterable
import glm


class Camera:
    def __init__(self,
                 viewport: tuple[int, int],
                 pos: glm.vec3 = glm.vec3(-10, 0, 0),
                 fov: float = 90,
                 znear: float = 1,
                 zfar: float = 500,
                 up: glm.vec3 = glm.vec3(0, 0, 1),
                 looking_at: glm.vec3 = glm.vec3(0, 0, 0)) -> None:
        self.viewport = viewport
        self.pos = pos
        self.fov = fov
        self.znear = znear
        self.zfar = zfar
        self.up = up
        self.looking_at = looking_at

    def set_viewport(self, v: Iterable[int]):
        self.viewport = tuple(v)

    def view_proj(self):
        return self.projection() * self.view()

    def projection(self):
        return glm.perspective(glm.radians(self.fov),
                               self.viewport[0] / self.viewport[1],
                               self.znear, self.zfar)

    def view(self):
        return glm.lookAt(self.pos,
                          self.looking_at,
                          self.up)