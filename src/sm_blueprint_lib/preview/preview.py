import os
from pprint import pp
import pygame as pg
import moderngl as mgl
import glm

from ..blueprint import Blueprint
from .camera import Camera
from ..pos import Pos
from ..utils import get_paths

from dataclasses import astuple


class LazyRendererManager:
    """Lazy loading manager for renderers to improve startup performance"""
    def __init__(self, context, shaders_path, game_path, meshes_path):
        self._context = context
        self._shaders_path = shaders_path
        self._game_path = game_path
        self._meshes_path = meshes_path
        self._renderers = {}
    
    def get_renderer(self, renderer_type):
        """Get renderer instance, creating it lazily if needed"""
        if renderer_type not in self._renderers:
            if renderer_type == 'part':
                from .renderers import PartRenderer
                self._renderers[renderer_type] = PartRenderer(self._context, self._shaders_path, self._game_path)
            elif renderer_type == 'logic_gate':
                from .renderers import LogicGateRenderer
                self._renderers[renderer_type] = LogicGateRenderer(self._context, self._shaders_path, self._game_path)
            elif renderer_type == 'timer_gate':
                from .renderers import TimerGateRenderer
                self._renderers[renderer_type] = TimerGateRenderer(self._context, self._shaders_path, self._game_path)
            elif renderer_type == 'block':
                from .renderers import BlockRenderer
                self._renderers[renderer_type] = BlockRenderer(self._context, self._shaders_path, self._game_path, self._meshes_path)
        return self._renderers[renderer_type]


def preview(bp: Blueprint):
    class BlueprintPreviewEngine:
        def __init__(self, window_size=(1080, 720)):
            _, self.game_path = get_paths()
            assert self.game_path, "Your game files ain't filing..."
            pg.init()

            self.window_size = window_size
            self.clear_color = 0.3, 0.3, 0
            self.framerate = 60
            self.deltatime = 0

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
            self.camera.looking_at = glm.vec3(astuple(sum((p.pos for p in bp.all_parts()), start=Pos(0,0,0)))) / len(list(bp.all_parts()))
            self.rot_radius = 20
            self.rot_vec = glm.vec2(0)
            self.start_drag = None
            self.mouse_sensitivity = 0.01
            self.camera_velocity = 10

            base_path = os.path.join(os.path.abspath(os.getcwd()), "src", "sm_blueprint_lib", "preview")
            shaders_path = os.path.join(base_path, "shaders")
            meshes_path = os.path.join(base_path, "meshes")

            # Use lazy renderer manager for better startup performance
            self.renderer_manager = LazyRendererManager(self.context, shaders_path, self.game_path, meshes_path)

            self.running = True
        
        def run(self):
            while self.running:
                self.context.gc()
                self.context.clear(color=self.clear_color)
                self.handle_events()
                self.render()
                pg.display.flip()
                self.deltatime = self.clock.tick(self.framerate) * 0.001

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
                    case pg.WINDOWRESIZED:
                        self.set_win_size((event.x, event.y))

            keys = pg.key.get_pressed()

            forward = self.camera.looking_at - self.camera.pos
            forward.z = 0
            forward = glm.normalize(forward)
            right = glm.cross(forward, (0, 0, 1))
            if keys[pg.K_e]:
                self.camera.looking_at.z += self.camera_velocity * self.deltatime
            if keys[pg.K_q]:
                self.camera.looking_at.z -= self.camera_velocity * self.deltatime
            if keys[pg.K_w]:
                self.camera.looking_at += forward * self.camera_velocity * self.deltatime
            if keys[pg.K_a]:
                self.camera.looking_at -= right * self.camera_velocity * self.deltatime
            if keys[pg.K_s]:
                self.camera.looking_at -= forward * self.camera_velocity * self.deltatime
            if keys[pg.K_d]:
                self.camera.looking_at += right * self.camera_velocity * self.deltatime

            self.rot_vec.y = glm.clamp(
                self.rot_vec.y, -glm.half_pi() + 0.01, glm.half_pi() - 0.01)
            self.rot_radius = glm.max(self.rot_radius, 1)
            self.camera.pos = self.camera.looking_at + glm.vec3(
                -glm.sin(self.rot_vec.x) * glm.cos(self.rot_vec.y),
                -glm.cos(self.rot_vec.x) * glm.cos(self.rot_vec.y),
                glm.sin(self.rot_vec.y),
            ) * self.rot_radius

        def render(self):
            # Use lazy renderer manager - renderers are created only when needed
            parts = list(bp.all_parts())
            for part in parts:
                # Determine renderer type based on part class
                renderer_type = None
                if hasattr(part, '__class__'):
                    class_name = part.__class__.__name__.lower()
                    if 'logicgate' in class_name:
                        renderer_type = 'logic_gate'
                    elif 'timer' in class_name:
                        renderer_type = 'timer_gate'
                    elif 'block' in class_name:
                        renderer_type = 'block'
                    else:
                        renderer_type = 'part'
                
                if renderer_type:
                    renderer = self.renderer_manager.get_renderer(renderer_type)
                    renderer.render(self.camera, [part])
        
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