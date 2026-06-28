# ====== PyOpenGL Interactive Example ======
# Features:
#   - Draws coordinate axes, triangle, and square
#   - Displays a moving point ("ball")
#   - Left-click to reposition ball
#   - Right-click to create an extra point
#   - Use UP/DOWN arrow keys to change ball speed
#   - Use W/S keys to increase/decrease ball size
#
#   Author: Abid Jahan Apon
# ===========================================

from ..OpenGL.GL import *      # Core OpenGL functions
from ..OpenGL.GLUT import *    # GLUT library for window and input handling
from ..OpenGL.GLU import *     # OpenGL Utility library
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
ball_speed = 0.03            # Ball movement speed
ball_size = 5                # Ball size (GL point size)
new_point = False            # Whether a new point is created on right-click
directions = [(1,1), (1,-1), (-1,-1), (-1,1)]
points = []
paused = False
blink = False
blink_timer = 0
visible = True

# ===== Coordinate Conversion =====
def convert_coordinate(x, y):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


# ===== Draw Functions =====
def draw_point(x, y, color = (1,1,1)):
    """Draws a single point at (x, y) with given size."""
    global ball_size
    glPointSize(ball_size)
    glColor3f(color[0], color[1], color[2])  # Red color for the point
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    """Handles normal keyboard inputs."""
    global ball_size, paused
    if key == b' ':
        paused = not paused

    glutPostRedisplay()


def special_key_listener(key, x, y):
    """Handles special keys (arrows, F-keys, etc.)."""
    global ball_speed
    if paused:
        return
    
    if key == GLUT_KEY_UP:
        ball_speed += 0.005
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        ball_speed -= 0.005
        if ball_speed < 0:
            ball_speed = 0
        print("Speed decreased")
    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    """
    Handles mouse clicks.
    Left-click: Move ball.
    Right-click: Create a new point.
    """
    global blink
    if paused:
        return
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        px, py = convert_coordinate(x, y)
        color = (random.random(), random.random(), random.random())
        points.append([px, py, random.choice(directions), color, color])


# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# ===== Display & Animation =====
def display():
    """Main display callback for rendering each frame."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
    glLoadIdentity()
    setup_projection()

    # Draw the right-clicked point (if any)
    for point in points:
        draw_point(point[0], point[1], point[3])
    glutSwapBuffers()


def animate():
    """Continuously moves the ball diagonally."""
    global ball_speed, blink, blink_timer, visible
    if paused:
        return
    
    # Blink
    if blink == True:
        blink_timer += 1
        if blink_timer >= 2000:
            visible = not visible
            for i in range(len(points)):
                if visible:
                    points[i][3] = points[i][4]
                else:
                    points[i][3] = (0, 0, 0)
            blink_timer = 0
    else:
        for i in range(len(points)):
            points[i][3] = points[i][4]
    
    # Move
    for point in points:
        direction = point[2]
        point[0] += direction[0]*ball_speed
        point[1] += direction[1]*ball_speed
        
        if abs(point[0]) > 250:
            point[2] = -direction[0], direction[1]
        if abs(point[1]) > 250:
            point[2] = direction[0], -direction[1]
            
    glutPostRedisplay()


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Task - 2")

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()