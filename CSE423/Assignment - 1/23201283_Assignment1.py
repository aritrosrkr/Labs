# Task - 1

from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
base_length = 30                # Base length for raindrops
base_speed = 0.8                # Ball movement speed
angle = 3*math.pi/2
sky_color = [0.4, 0.4, 0.4]
target_color = [0.4, 0.4, 0.4]
transition_speed = 0.0005

# ===== Draw Functions =====
def draw_point(x, y, size):
    """Draws a single point at (x, y) with given size."""
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_line(x, y, length, angle):
    glLineWidth(2)          # Set line width
    glBegin(GL_LINES)      # Start drawing lines
    glVertex2f(x, y)        # Specify the (x, y) coordinate of the point
    glVertex2f(x+length*math.cos(angle), y+length*math.sin(angle))   # Specify the (x, y) coordinate of the point
    glEnd()                 # Finish drawing


def draw_quad(l, b, x = 0, y = 0, rgb = (1,1,1)):
    glColor3f(rgb[0], rgb[1], rgb[2])
    glBegin(GL_TRIANGLES)
    glVertex2d(x, y)
    glVertex2d(x+l, y)
    glVertex2d(x+l, y+b)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glVertex2d(x, y+b)
    glVertex2d(x+l, y+b)
    glVertex2d(x, y)
    glEnd()
    

def draw_house():
    draw_quad(120, 80, -60, -80, (0.8, 0.6, 0.4))
    
    # Roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.3, 0.2)  # Dark brown
    glVertex2f(-80, 0)
    glVertex2f(0, 50)
    glVertex2f(80, 0)
    glEnd()
    
    # Door
    draw_quad(30, 50, -15, -80, (0.4, 0.2, 0.1))
    
    # Window left
    glColor3f(0.7, 0.9, 1.0)    #Light blue
    glLineWidth(2)
    
    glBegin(GL_LINES)

    glVertex2f(-50, -30)
    glVertex2f(-50, -50)
    
    glVertex2f(-50, -30)
    glVertex2f(-30, -30)
    
    glVertex2f(-30, -30)
    glVertex2f(-30, -50)
    
    glVertex2f(-30, -50)
    glVertex2f(-50, -50)
    
    # Cross
    glVertex2f(-40, -30)
    glVertex2f(-40, -50)
    
    glVertex2f(-50, -40)
    glVertex2f(-30, -40)
    glEnd()
    
    # Window right
    glBegin(GL_LINES)

    glVertex2f(50, -30)
    glVertex2f(50, -50)
    
    glVertex2f(50, -30)
    glVertex2f(30, -30)
    
    glVertex2f(30, -30)
    glVertex2f(30, -50)
    
    glVertex2f(30, -50)
    glVertex2f(50, -50)
    
    # Cross
    glVertex2f(40, -30)
    glVertex2f(40, -50)
    
    glVertex2f(50, -40)
    glVertex2f(30, -40)
    glEnd()


def draw_ground():
    draw_quad(500, 200, -250, -250, (0.3, 0.6, 0.3))


def draw_skybox():
    global sky_color
    draw_quad(500, 500, -250, -50, (sky_color[0], sky_color[1], sky_color[2]))
    
    
# Raindrop List // drop = [x, y, length, speed]
layer_1 = []
layer_2 = []
layer_3 = []
for i in range(200):
    if i < 30:
        layer_1.append([random.randint(-250, 250), random.randint(-250, 250), base_length*1.5,  base_speed*2])
    elif i < 100:
        layer_2.append([random.randint(-250, 250), random.randint(-250, 250), base_length, base_speed])
    else:
        layer_3.append([random.randint(-250, 250), random.randint(-250, 250), base_length*0.6, base_speed*0.75])

    
# ===== Keyboard & Mouse Interaction =====
def special_key_listener(key, x, y):
    """Handles special keys (arrows, F-keys, etc.)."""
    global base_speed, angle, target_color
    if key == GLUT_KEY_UP:
        target_color = [0.4, 0.4, 0.4]
    if key == GLUT_KEY_DOWN:
        target_color = [0, 0, 0]

    if key == GLUT_KEY_RIGHT:
        if (angle + math.pi/12) <= 11*math.pi/6:
            angle += math.pi/12
    if key == GLUT_KEY_LEFT:
        if (angle - math.pi/12) >= 7*math.pi/6:
            angle -= math.pi/12
    glutPostRedisplay()


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
    
    draw_skybox()
    # drop = [x, y, length, speed]
    glColor3f(0.7, 0.9, 1.0)
    for drop in layer_3:
        draw_line(drop[0], drop[1], drop[2], angle)
    
    draw_ground()
    draw_house()
    
    glColor3f(0.7, 0.9, 1.0)
    for drop in layer_1:
        draw_line(drop[0], drop[1], drop[2], angle)
    for drop in layer_2:
        draw_line(drop[0], drop[1], drop[2], angle)

    glutSwapBuffers()


layers = [layer_1, layer_2, layer_3]

def animate():
    """Continuously moves the ball diagonally."""
    global layers, angle, sky_color, target_color, transition_speed
    dx = math.cos(angle)
    dy = math.sin(angle)

    # Change color
    for i in range(3):
        if sky_color[i] < target_color[i]:
            sky_color[i] = sky_color[i] + transition_speed
        elif sky_color[i] > target_color[i]:
            sky_color[i] = sky_color[i] - transition_speed

    for layer in layers:
        for drop in layer:
            drop[0] += dx*drop[3]  # x = x + cos(angle)*speed
            drop[1] += dy*drop[3]
            if drop[1] < -250:
                drop[1] = 250
            if drop[0] < -250:
                drop[0] = 250
            elif drop[0] > 250:
                drop[0] = -250

    glutPostRedisplay()
    

# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Task - 1")

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)

    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()




# Task - 2

from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
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