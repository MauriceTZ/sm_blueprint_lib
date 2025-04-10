import moderngl_window as mglw
from moderngl_window import scene
import glm

from ..blueprint import Blueprint


class BlueprintPreviewer(mglw.WindowConfig):
    window_size = 1080, 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.wnd.mouse_exclusivity = True
        self.button = self.load_scene(
            r"C:\Users\mauri\Documents\Proyects\Python\Scrap Mechanic\sm_blueprint_lib\src\sm_blueprint_lib\preview\models\obj_interactive_button_on.obj")
        self.camera = scene.KeyboardCamera(
            self.wnd.keys,
            fov=75.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )
        self.camera.velocity = 10.0
        self.camera.mouse_sensitivity = 0.25
        self.camera.position = (
            self.button.get_center()
            + glm.vec3(0.0, 0.0, self.button.diagonal_size / 0.5)
        )
    def on_render(self, time, frame_time):
        self.button.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time,
        )


def preview(bp: Blueprint):
    BlueprintPreviewer.run()
