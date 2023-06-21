import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *
import pyrr
import math
import numpy as np
from pyrr import Vector3, vector, vector3, matrix44
import random
from math import sin, cos, radians

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 4.0, 3.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0
    #recuperer la vue camera qui est adaptée de la scène
    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    #gestion du pointeur de souris dans l'espace
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=False):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    # Deplacement de la vue camera grace au clavier
    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity

# creation de l'objet camera
cam = Camera()

boules = []
taillesBoules = []
vitessesBoules = []
compteur = 0
WIDTH, HEIGHT = 1400, 800
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False

# evolution de la taille des boules 
def nextSize(c):
    op = random.choice([1, -1])
    ret = c+op*0.01
    if ret > 0:
        if ret < 1:
            return ret
        return 1
    return 0

sphere = gluNewQuadric()

# mise à jour coordonnées du lorenz
def update_lorenz(x, y, z, dt):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    x += dx
    y += dy
    z += dz
    return x, y, z

# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False

# fonction qui permet de bouger en vue camera
def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.25)
    if right:
        cam.process_keyboard("RIGHT", 0.25)
    if forward:
        cam.process_keyboard("FORWARD", 0.25)
    if backward:
        cam.process_keyboard("BACKWARD", 0.25)
# fonction de la souris
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

# vertex et le fragment 
vertex_src = """
#version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""
fragment_src = """
#version 330

in vec2 v_texture;

out vec4 out_color;

void main()
{
    vec3 position = vec3(gl_FragCoord.x / 1400, gl_FragCoord.y / 800, 0.5);
    vec3 rainbow_color = vec3(
        abs((position.x + 2 * position.y) / 2.0),   // Red component
        abs(position.y),                           // Green component
        abs(position.x)                            // Blue component
    );
    out_color = vec4(rainbow_color, 1);
}
"""
def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creation fenêtre
window = glfw.create_window(WIDTH, HEIGHT, "Lorenz 3D By QUIQUE Paul, RHOURRI Yassine, RAFIQUL Saad ", None, None)

# verification de la creation de fenêtre
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# position de la fenêtre
glfw.set_window_pos(window, 400, 200)

# changement de la taille de la fenêtre
glfw.set_window_size_callback(window, window_resize_clb)
# position souris
glfw.set_cursor_pos_callback(window, mouse_look_clb)
# entrées clavier
glfw.set_key_callback(window, key_input_clb)
# capture de la souris
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

glfw.make_context_current(window)
#chargement du shader pour le programme fragment et vertex
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

glUseProgram(shader)
glClearColor(0.025, 0.025, 0.025, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# transformation de l'espace 3D vers le 2D de l'écran
projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
# position dans l'espace 3D
init_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

#envois des données pour le shader
model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# fonction de dessin pour le lorenz ainsi que la generation des spheres
def draw_lorenz(lorenz_points):
    global compteur, taillesBoules
    glLineWidth(4.0)  # Définir l'épaisseur de ligne
    glColor3f(1, 1, 1)  # Définir la couleur de ligne (rouge)
    glBegin(GL_LINE_STRIP)
    for i in range(len(lorenz_points)):
        point = lorenz_points[i]
        glVertex3f(point[0], point[1], point[2])
    glEnd()
    last_point = lorenz_points[-1]
    if compteur > 100:
        if len(boules) > 15:
            boules.pop()
            taillesBoules.pop()
            vitessesBoules.pop()
        boules.append(random.randint(0, len(lorenz_points)-1))
        taillesBoules.append(random.random())
        vitessesBoules.append([random.randint(0, 10), 0])
        compteur=0
    else:
        compteur+=1
    for i in range(len(boules)):
        numPoint = boules[i]
        if vitessesBoules[i][1] == vitessesBoules[i][0]:
            vitessesBoules[i][1]=0
            if numPoint < len(lorenz_points):
                boules[i]+=1
            else:
                boules[i]=random.randint(0, len(lorenz_points-1))
        else:
            vitessesBoules[i][1]+=1
        taillesBoules[i] = nextSize(taillesBoules[i])
        sphere_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3(lorenz_points[numPoint]))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, sphere_pos)
        gluSphere(sphere, taillesBoules[i], 32, 16)

cam.camera_pos = Vector3([-51.14677836  ,57.72648968 , 59.36484827])
cam.jaw = -25
cam.pitch = -45
cam.update_camera_vectors()

# la boucle principale
def main():
    lorenz_points = []
    lorenz_x, lorenz_y, lorenz_z = -0.9, -0.9, -0.9  # Valeurs initiales pour l'attracteur de Lorenz
    lorenz_dt = 0.004  # Pas de temps pour la mise à jour de l'attracteur

    while not glfw.window_should_close(window):
        print(cam.jaw, cam.pitch)
        glfw.poll_events()
        do_movement()
        lorenz_size = 0.5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-lorenz_size, lorenz_size, -lorenz_size, lorenz_size, -lorenz_size, lorenz_size)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        lorenz_x, lorenz_y, lorenz_z = update_lorenz(lorenz_x, lorenz_y, lorenz_z, lorenz_dt)
        lorenz_points.append([lorenz_x, lorenz_y, lorenz_z])
        draw_lorenz(lorenz_points)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, init_pos)
        glfw.swap_buffers(window)

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
    glfw.terminate()       
