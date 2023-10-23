from OpenGL.GL import *
from OpenGL.GL import shaders
import glm
import logging


logger = logging.getLogger(__name__)


def read_file(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()


def compile_shader(shader: GLuint) -> None:
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        logger.error("Shader compilation error:\n%s", error)


def link_program(program: GLuint, vshader: GLuint, fshader: GLuint) -> None:
    glAttachShader(program, vshader)
    glAttachShader(program, fshader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program)
        logger.error('Linking error:\n%s', error)
        raise RuntimeError("Linking Error")


def initialize_shader(vshader_path: str, fshader_path: str) -> GLuint:
    v_text = read_file(vshader_path)
    f_text = read_file(fshader_path)
    print(v_text)
    print(f_text)

    vertex = shaders.compileShader(v_text, GL_VERTEX_SHADER)
    fragment = shaders.compileShader(f_text, GL_FRAGMENT_SHADER)

    program = shaders.compileProgram(vertex, fragment)

    return program


class Shader:
    def __init__(self, vshader_path: str, fshader_path: str):
        self.shader_id = 0
        self.vshader_path = vshader_path
        self.fshader_path = fshader_path

    def initialize_shader(self) -> None:
        v_text = read_file(self.vshader_path)
        f_text = read_file(self.fshader_path)

        vertex = shaders.compileShader(v_text, GL_VERTEX_SHADER)
        fragment = shaders.compileShader(f_text, GL_FRAGMENT_SHADER)

        self.shader_id = shaders.compileProgram(vertex, fragment)

    def use(self) -> None:
        if self.shader_id != 0:
            glUseProgram(self.shader_id)

    def send_mat4(self, name: str, matrix: glm.mat4) -> None:
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader_id, name), 1, GL_FALSE, glm.value_ptr(matrix))
