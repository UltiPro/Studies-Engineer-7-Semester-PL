from OpenGL.GL import *
import ctypes
from shader_util import Shader
import glm
from abc import ABC, abstractmethod

QUAD_VERTICES = glm.array(
    glm.float32,
    -0.5,
    0.5,
    0.0,  # top left - yellow
    0.5,
    0.5,
    0.0,  # top right - white
    -0.5,
    -0.5,
    0.0,  # bottom left - green
    0.5,
    -0.5,
    0.0,  # bottom right - cyan
)

QUAD_COLORS = glm.array(
    glm.float32,
    1.0,
    1.0,
    0.0,  # yellow
    1.0,
    1.0,
    1.0,  # white
    0.0,
    1.0,
    0.0,  # green
    0.0,
    1.0,
    1.0,  # cyan
)


QUAD_INDICES = glm.array(glm.uint32, 0, 1, 3, 0, 3, 2)

CUBE_VERTICES = glm.array(
    glm.float32,
    -0.5,
    0.5,
    0.5,
    1.0,
    1.0,
    0.0,  # top left front - yellow
    -0.5,
    0.5,
    -0.5,
    1.0,
    0.0,
    0.0,  # top left back - red
    0.5,
    0.5,
    -0.5,
    1.0,
    0.0,
    1.0,  # top right back - magenta
    0.5,
    0.5,
    0.5,
    1.0,
    1.0,
    1.0,  # top right front - white
    -0.5,
    -0.5,
    0.5,
    0.0,
    1.0,
    0.0,  # bottom left front - green
    -0.5,
    -0.5,
    -0.5,
    0.0,
    0.0,
    0.0,  # bottom left back - black
    0.5,
    -0.5,
    -0.5,
    0.0,
    0.0,
    1.0,  # bottom right back - blue
    0.5,
    -0.5,
    0.5,
    0.0,
    1.0,
    1.0,  # bottom right front - cyan
)

CUBE_INDICES = glm.array(
    glm.uint32,
    0,
    1,
    2,  # top face
    0,
    2,
    3,
    4,
    0,
    3,  # front face
    4,
    3,
    7,
    5,
    1,
    0,  # left face
    5,
    0,
    4,
    7,
    3,
    2,  # right face
    7,
    2,
    6,
    2,
    6,
    5,  # back face
    2,
    5,
    1,
    6,
    7,
    4,  # bottom face
    6,
    4,
    5,
)


class Model(ABC):
    def __init__(self, shader: Shader):
        self.shader = shader
        self.transformation = glm.mat4()

    @abstractmethod
    def initialize_model(self):
        """Initializes data for the model"""

    @abstractmethod
    def render(self):
        """Takes care of rendiring the model"""


class CubeModel(Model):
    def initialize_model(self):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, CUBE_VERTICES.nbytes, CUBE_VERTICES.ptr, GL_STATIC_DRAW
        )

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            CUBE_INDICES.nbytes,
            CUBE_INDICES.ptr,
            GL_STATIC_DRAW,
        )

        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None
        )
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            6 * glm.sizeof(glm.float32),
            ctypes.c_void_p(3 * glm.sizeof(glm.float32)),
        )
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def render(self):
        self.shader.send_mat4("model", self.transformation)

        self.shader.use()
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(CUBE_INDICES), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def rotate(self, dx: float, dy: float) -> None:
        """Rotates the model in world space based on dx and dy offsets"""

        rotation_factor = 0.002

        rot_matrix = glm.mat3(self.transformation)
        rot_axis_y = glm.inverse(rot_matrix) * glm.vec3(-1.0, 0.0, 0.0)
        rot_axis_x = glm.inverse(rot_matrix) * glm.vec3(0.0, -1.0, 0.0)

        self.transformation = glm.rotate(
            self.transformation, dx * rotation_factor, rot_axis_x
        )
        self.transformation = glm.rotate(
            self.transformation, dy * rotation_factor, rot_axis_y
        )


class QuadModel(Model):
    def initialize_model(self):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        self.cross_val = 0.0

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, QUAD_VERTICES.nbytes * 2, None, GL_DYNAMIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, QUAD_VERTICES.nbytes, QUAD_VERTICES.ptr)
        glBufferSubData(
            GL_ARRAY_BUFFER, QUAD_VERTICES.nbytes, QUAD_COLORS.nbytes, QUAD_COLORS.ptr
        )

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            QUAD_VERTICES.nbytes,
            QUAD_INDICES.ptr,
            GL_STATIC_DRAW,
        )

        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None
        )
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            3 * glm.sizeof(glm.float32),
            ctypes.c_void_p(QUAD_VERTICES.nbytes),
        )
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def render(self):
        self.shader.send_mat4("model", self.transformation)

        self.shader.use()
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(QUAD_INDICES), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def translate(self, dx: float, dy: float, dz: float):
        self.transformation = glm.translate(self.transformation, glm.vec3(dx, dy, dz))

    def slide(self, dx):
        slide_factor = 0.001

        self.cross_val -= dx * slide_factor
        self.cross_val = glm.clamp(self.cross_val, 0.0, 1.0)

        new_colors = glm.array(
            glm.float32,
            *vec3lerp(glm.vec3(1.0, 1.0, 0.0), glm.vec3(1.0, 0.0, 0.0), self.cross_val),
            *vec3lerp(glm.vec3(1.0, 1.0, 1.0), glm.vec3(1.0, 0.0, 1.0), self.cross_val),
            *vec3lerp(glm.vec3(0.0, 1.0, 0.0), glm.vec3(0.0, 0.0, 0.0), self.cross_val),
            *vec3lerp(glm.vec3(0.0, 1.0, 1.0), glm.vec3(0.0, 0.0, 1.0), self.cross_val)
        )

        glBindVertexArray(self.vao)
        glBufferSubData(
            GL_ARRAY_BUFFER, QUAD_VERTICES.nbytes, new_colors.nbytes, new_colors.ptr
        )

        glBindVertexArray(0)


def vec3lerp(a: glm.vec3, b: glm.vec3, c: float):
    x = glm.lerp(a.x, b.x, c)
    y = glm.lerp(a.y, b.y, c)
    z = glm.lerp(a.z, b.z, c)

    return x, y, z
