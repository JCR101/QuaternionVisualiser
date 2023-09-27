import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *

# Quaternion class definition


class Quaternion:
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

# Defines a rotation quaternion, e.g., 180-degree rotation around the y-axis
angle = 180 / 2  # half angle for quaternions
s = math.sin(math.radians(angle))
rotation_quaternion = Quaternion(math.cos(math.radians(angle)), 0, s, 0)

# Rotates the cube's vertices
rotated_vertices = [rotation_quaternion.rotate_point(v) for v in cube_vertices]


def draw_cube(vertices):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 3, 1, 1)  # Rotates for better visualization
        draw_cube(cube_vertices)  # Draws original cube
        draw_cube(rotated_vertices)  # Draws rotated cube
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
