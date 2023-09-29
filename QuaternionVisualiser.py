import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class Quaternion:  # Quaternion class definition
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        return Quaternion(w, x, y, z)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def rotate_point(self, point):
        p = Quaternion(0, *point)
        rotated = self * p * self.conjugate()
        return (rotated.x, rotated.y, rotated.z)


def get_user_rotation():
    try:
        angle = float(input("Enter the angle of rotation (in degrees): "))
        x = float(input("Enter the x component of the rotation axis: "))
        y = float(input("Enter the y component of the rotation axis: "))
        z = float(input("Enter the z component of the rotation axis: "))

        # Normalizes the rotation axis
        magnitude = math.sqrt(x**2 + y**2 + z**2)
        x /= magnitude
        y /= magnitude
        z /= magnitude

        # Converts the angle to radians and compute half-angle for quaternions
        half_angle_rad = math.radians(angle / 2)
        s = math.sin(half_angle_rad)

        return Quaternion(math.cos(half_angle_rad), s*x, s*y, s*z)
    except ValueError:
        print("Invalid input! Using default rotation.")
        return Quaternion(1, 0, 0, 0)  # No rotation by default


def hex_to_rgb(hex_color):
    # Converts a hexadecimal color string (like '#RRGGBB') to a tuple of RGB values between 0 and 1.
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


# Defines the cube's vertices
cube_vertices = [
    (0.5, 0.5, 0.5),
    (0.5, 0.5, -0.5),
    (0.5, -0.5, 0.5),
    (0.5, -0.5, -0.5),
    (-0.5, 0.5, 0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, -0.5, -0.5),
]

# Defines cube edges
edges = [
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 3),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7),
]


# Gets the rotation quaternion from the user
rotation_quaternion = get_user_rotation()

# Rotates the cube's vertices
rotated_vertices = [rotation_quaternion.rotate_point(v) for v in cube_vertices]


def draw_cube(vertices, color=(1, 1, 1)):  # default color is white
    if isinstance(color, str):
        color = hex_to_rgb(color)
    glColor3f(*color)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # argNames=('fovy', 'aspect', 'zNear', 'zFar')
    gluPerspective(30, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Rotates about the y axis for better visualization
        glRotatef(1, 0, 1, 0)

        # Draws original cube in blue
        draw_cube(cube_vertices, color="#3089ff")
        # Draws rotated cube in red
        draw_cube(rotated_vertices, color="#ff2658")

        pygame.display.flip()
        pygame.time.wait(20)  # 20ms delay (how fast the cube rotates)


if __name__ == "__main__":
    main()
