from os import PathLike
import moderngl as mgl


class ShaderProgram:
    def __init__(self, context: mgl.Context, *shaders: PathLike) -> None:
        self.context = context
        self.programs: list[mgl.Program] = []
        for shader_path in shaders:
            self.programs.append(self._get_program(shader_path))

    def _get_program(self, shader: PathLike):
        with open(shader + ".vert") as file:
            vertex_shader = file.read()
        with open(shader + ".frag") as file:
            fragment_shader = file.read()

        program = self.context.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        return program

    def destroy(self):
        for program in self.programs:
            program.release()
