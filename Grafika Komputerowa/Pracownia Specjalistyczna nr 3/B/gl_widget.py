from OpenGL.GL import *
import glm
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from shader_util import Shader
from pathlib import Path
from model import CubeModel, QuadModel


WIDTH, HEIGHT = 800, 600


class OpenGLApp:
    def __init__(self, shader: Shader):
        self.w = 1280
        self.h = 720
        self.shader = shader

        self.mouse_down = False
        self.mouse_down_r = False
        self.mouse_prev = glm.vec2(WIDTH / 2, HEIGHT / 2)

    def initializeGL(self) -> None:
        glfwInit()
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfwWindowHint(GLFW_SAMPLES, 4)

        self.window = glfwCreateWindow(WIDTH, HEIGHT, "Grafika_Kostka", None, None)
        if self.window == None:
            print("Failed to create GLFW window")
            glfwTerminate()

        glfwSetWindowUserPointer(self.window, self)

        glfwMakeContextCurrent(self.window)
        glfwSetFramebufferSizeCallback(self.window, framebuffer_size_callback)
        glfwSetMouseButtonCallback(self.window, mouse_button_callback)
        glfwSetCursorPosCallback(self.window, mouse_pos_callback)

        glfwSetInputMode(self.window, GLFW_STICKY_MOUSE_BUTTONS, GLFW_TRUE)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        self.shader.initialize_shader()
        self.shader.use()

        self.cube = CubeModel(self.shader)
        self.cube.initialize_model()

        self.quad = QuadModel(self.shader)
        self.quad.initialize_model()
        self.quad.translate(2.0, 0.0, 0.0)

        view = glm.mat4()
        proj = glm.mat4()

        view = glm.translate(view, glm.vec3(-1.0, 0.0, -3.0))
        proj = glm.perspective(glm.radians(45.0), self.w / self.h, 0.1, 100.0)

        self.shader.send_mat4("view", view)
        self.shader.send_mat4("projection", proj)

    def render(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.cube.render()
        self.quad.render()

        glfwSwapBuffers(self.window)


def framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:
    glViewport(0, 0, width, height)


def mouse_button_callback(window: GLFWwindow, button: int, action: int, mods: int):
    app: OpenGLApp = glfwGetWindowUserPointer(window)

    app.mouse_prev.x, app.mouse_prev.y = glfwGetCursorPos(window)

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        app.mouse_down = True
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
        app.mouse_down = False

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        app.mouse_down_r = True
    elif button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE:
        app.mouse_down_r = False


def mouse_pos_callback(window: GLFWwindow, xpos: float, ypos: float):
    app: OpenGLApp = glfwGetWindowUserPointer(window)

    dx = xpos - app.mouse_prev.x
    dy = ypos - app.mouse_prev.y

    if app.mouse_down:
        app.cube.rotate(dx, dy)

    if app.mouse_down_r:
        app.quad.slide(dx)

    app.mouse_prev.x, app.mouse_prev.y = glfwGetCursorPos(window)


def main():
    v_path = Path(__file__).parent / "shaders" / "vertex.glsl"
    f_path = Path(__file__).parent / "shaders" / "fragment.glsl"

    shader = Shader(v_path.absolute(), f_path.absolute())
    app = OpenGLApp(shader)
    app.initializeGL()

    while not glfwWindowShouldClose(app.window):
        app.render()
        glfwPollEvents()


if __name__ == "__main__":
    main()
