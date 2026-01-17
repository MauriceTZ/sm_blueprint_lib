import os
from pprint import pp
import pygame as pg
import moderngl as mgl
import glm

from ..blueprint import Blueprint
from .renderers import LogicGateRenderer, TimerGateRenderer, BlockRenderer
from .camera import Camera


def preview(bp: Blueprint):
    class BlueprintPreviewEngine:
        def __init__(self, window_size=(1080, 720)):
            pg.init()

            self.window_size = window_size
            self.clear_color = 0.3, 0.3, 0
            self.framerate = 60

            pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
            pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 5)
            pg.display.gl_set_attribute(
                pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

            pg.display.set_mode(self.window_size, flags=pg.OPENGL |
                                pg.DOUBLEBUF | pg.RESIZABLE)
            pg.display.set_caption("sm_blueprint_lib_preview")

            self.context = mgl.create_context()
            self.context.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE |
                                mgl.BLEND)
            self.context.gc_mode = "context_gc"

            self.clock = pg.time.Clock()
            self.camera = Camera(self.window_size)
            self.rot_radius = 20
            self.rot_vec = glm.vec2(0)
            self.start_drag = None
            self.mouse_sensitivity = 0.01

            base_path = os.path.join(os.path.abspath(os.getcwd()), "src", "sm_blueprint_lib", "preview")
            shaders_path = os.path.join(base_path, "shaders")
            textures_path = os.path.join(base_path, "textures")
            meshes_path = os.path.join(base_path, "meshes")

            self.renderers = [
                LogicGateRenderer(self.context, shaders_path, textures_path, meshes_path),
                TimerGateRenderer(self.context, shaders_path, textures_path, meshes_path),
                BlockRenderer(self.context, shaders_path, textures_path, meshes_path),
            ]

            self.running = True
        
        def run(self):
            while self.running:
                self.context.gc()
                self.context.clear(color=self.clear_color)
                self.handle_events()
                self.render()
                pg.display.flip()
                self.clock.tick(self.framerate)

        def handle_events(self):
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        self.running = False
                    case pg.MOUSEBUTTONDOWN:
                        self.start_drag = glm.vec2(event.pos)
                    case pg.MOUSEBUTTONUP:
                        self.start_drag = None
                    case pg.MOUSEMOTION:
                        if self.start_drag:
                            self.rot_vec += glm.vec2(event.rel) * \
                                self.mouse_sensitivity
                    case pg.MOUSEWHEEL:
                        self.rot_radius *= 1 - event.precise_y * self.mouse_sensitivity * 10
                        self.rot_vec.x -= event.precise_x * self.mouse_sensitivity * 10
                        # print(self.rot_radius, self.rot_vec.x)
                    case pg.WINDOWRESIZED:
                        self.set_win_size((event.x, event.y))
            
            self.rot_vec.y = glm.clamp(
                self.rot_vec.y, -glm.half_pi() + 0.01, glm.half_pi() - 0.01)
            self.rot_radius = glm.max(self.rot_radius, 1)
            self.camera.pos = glm.vec3(
                -glm.sin(self.rot_vec.x) * glm.cos(self.rot_vec.y),
                -glm.cos(self.rot_vec.x) * glm.cos(self.rot_vec.y),
                glm.sin(self.rot_vec.y),
            ) * self.rot_radius

        def render(self):
            for renderer in self.renderers:
                renderer.render(self.camera, bp.all_parts())
        
        def set_win_size(self, size: tuple[int, int]):
            self.window_size = size
            self.camera.set_viewport(self.window_size)
            

    bpp = BlueprintPreviewEngine()
    bpp.run()


def compute_rotation_matrix(xaxis: int, zaxis: int):
    """
    This function generates the needed rotation matrix from the xaxis and zaxis
    attributes of a Part in order for the preview code to render them in the
    correct orientation and position.
    
    :param xaxis: The xaxis attribute of a part.
    :type xaxis: int
    :param zaxis: The zaxis attribute of a part.
    :type zaxis: int
    """
    x, z = glm.vec3(0), glm.vec3(0)
    x[int(abs(xaxis)) - 1] = glm.sign(xaxis)
    z[int(abs(zaxis)) - 1] = glm.sign(zaxis)
    y = glm.cross(z, x)
    # First translate the object by (0.5, 0.5, 0.5) and THEN rotate
    return glm.mat4_cast(glm.quatLookAtLH(z, y)) * glm.translate(glm.vec3(0.5, 0.5, 0.5))