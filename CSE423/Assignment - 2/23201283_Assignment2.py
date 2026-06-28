from OpenGL.GL import * # Core OpenGL functions
from OpenGL.GLUT import * # GLUT library for window and input handling
from OpenGL.GLU import * # OpenGL Utility library
import math
import random
import time

# ===== Global Variables ===== #
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 500
WIDTH_HALF, HEIGHT_HALF = WINDOW_WIDTH//2, WINDOW_HEIGHT//2
speed = [150, 0]        #pixels/sec
paused = False
cheat = False
game_over = False
score = 0

color = random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)
diamond_pos = [random.randint(-WIDTH_HALF, WIDTH_HALF - 30), HEIGHT_HALF - 30]
platform_pos = [0, -HEIGHT_HALF + 10]

t0 = time.time()

# ===== Coordinate Conversion =====
def convert_coordinate(x, y):
    """Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space, but OpenGL center is (0,0)."""
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


class MPL:
    @staticmethod
    def findZone(dx, dy):
        if dx >= 0 and dy >= 0:
            if dx > dy:
                return 0
            return 1
        elif dx < 0 and dy >= 0:
            if abs(dx) > dy:
                return 3
            return 2
        elif dx < 0 and dy < 0:
            if abs(dx) > abs(dy):
                return 4
            return 5
        elif dx >= 0 and dy < 0:
            if dx > abs(dy):
                return 7
            return 6
    
    @staticmethod
    def convertZone(x, y, zone, back=False):
        if back:
            if zone == 0:
                return x, y
            elif zone == 1:
                return y, x
            elif zone == 2:
                return -y, x
            elif zone == 3:
                return -x, y
            elif zone == 4:
                return -x, -y
            elif zone == 5:
                return -y, -x
            elif zone == 6:
                return y, -x
            elif zone == 7:
                return x, -y
            
        else:
            if zone == 0:
                return x, y, zone
            elif zone == 1:
                return y, x, zone
            elif zone == 2:
                return y, -x, zone
            elif zone == 3:
                return -x, y, zone
            elif zone == 4:
                return -x, -y, zone
            elif zone == 5:
                return -y, -x, zone
            elif zone == 6:
                return -y, x, zone
            elif zone == 7:
                return x, -y, zone
    
    
    @staticmethod
    def calculateMPL(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        zone = MPL.findZone(dx, dy)
        x1, y1, prev = MPL.convertZone(x1, y1, zone)
        x2, y2, prev = MPL.convertZone(x2, y2, zone)
        
        dx = x2 - x1
        dy = y2 - y1
        
        d = 2*dy - dx
        dE = 2*dy
        dNE = 2*dy - 2*dx
        
        pixels = []
        
        x, y = x1, y1               # Starting point (converted to zone 0)
        while x <= x2:              # Zone 0 guarantees x2 >= x1
            pixels.append(MPL.convertZone(x, y, prev, back=True)) # Convert back to original zone
            if d < 0:
                d += dE
                x += 1
            else:
                d += dNE
                x += 1
                y += 1
        
        return pixels


# ===== Draw Functions =====
def drawUI():
    pixels = MPL.calculateMPL(-WIDTH_HALF, HEIGHT_HALF - 40, WIDTH_HALF, HEIGHT_HALF - 40)
    
    glColor3f(1,1,1)
    if game_over:
        glColor3f(1,0,0)
    
    glPointSize(3)
    glBegin(GL_POINTS)
    for px, py in pixels:
        glVertex2f(px, py)
    
    # Pause button
    glColor3f(1, 0.8, 0.2)
    pixels = MPL.calculateMPL(-10, HEIGHT_HALF - 10, -10, HEIGHT_HALF - 30)
    for px, py in pixels:
        glVertex2f(px, py)
        
    if not paused:
        pixels = MPL.calculateMPL(10, HEIGHT_HALF - 10, 10, HEIGHT_HALF - 30)
        for px, py in pixels:
            glVertex2f(px, py)
    
    elif paused:
        pixels = MPL.calculateMPL(-10, HEIGHT_HALF - 10, 10, HEIGHT_HALF - 20)
        for px, py in pixels:
            glVertex2f(px, py)
        
        pixels = MPL.calculateMPL(-10, HEIGHT_HALF - 30, 10, HEIGHT_HALF - 20)
        for px, py in pixels:
            glVertex2f(px, py)
        
    
    # Close button
    glColor3f(1.0, 0.3, 0.3)
    pixels = MPL.calculateMPL(WIDTH_HALF - 30, HEIGHT_HALF - 10, WIDTH_HALF - 10, HEIGHT_HALF - 30)
    for px, py in pixels:
        glVertex2f(px, py)

    pixels = MPL.calculateMPL(WIDTH_HALF - 30, HEIGHT_HALF - 30, WIDTH_HALF - 10, HEIGHT_HALF - 10)
    for px, py in pixels:
        glVertex2f(px, py)
    
    
    # Restart button
    glColor3f(0.3, 0.8, 1.0)
    pixels = MPL.calculateMPL(-WIDTH_HALF + 10, HEIGHT_HALF - 20, -WIDTH_HALF + 35, HEIGHT_HALF - 20)
    for px, py in pixels:
        glVertex2f(px, py)

    pixels = MPL.calculateMPL(-WIDTH_HALF + 10, HEIGHT_HALF - 20, -WIDTH_HALF + 20, HEIGHT_HALF - 10)
    for px, py in pixels:
        glVertex2f(px, py)
    
    pixels = MPL.calculateMPL(-WIDTH_HALF + 10, HEIGHT_HALF - 20, -WIDTH_HALF + 20, HEIGHT_HALF - 30)
    for px, py in pixels:
        glVertex2f(px, py)
        
    glEnd()
    
    
def drawDiamond():
    global diamond_pos, color
    if game_over:
        return
    
    x, y = diamond_pos
    pixels = MPL.calculateMPL(x, y, x+10, y-15)         # bottom left
    pixels += MPL.calculateMPL(x+10, y-15, x+20, y)     # bottom right
    pixels += MPL.calculateMPL(x+20, y, x+10, y+15)     # top right
    pixels += MPL.calculateMPL(x+10, y+15, x, y)        # top left

    glColor3f(*color)
    glPointSize(2)
    glBegin(GL_POINTS)
    for px, py in pixels:
        glVertex2f(px, py)
    glEnd()


def drawPlatform():
    global platform_pos
    x, y = platform_pos
    pixels = MPL.calculateMPL(x-40, y, x+40, y)
    pixels += MPL.calculateMPL(x+40, y, x+50, y+15)
    pixels += MPL.calculateMPL(x+50, y+15, x-50, y+15)
    pixels += MPL.calculateMPL(x-50, y+15, x-40, y)
    
    glColor3f(1,1,1)
    if game_over:
        glColor3f(1,0,0)

    glPointSize(2)
    glBegin(GL_POINTS)
    for px, py in pixels:
        glVertex2f(px, py)
    glEnd()


def hasCollided():
    global diamond_pos, platform_pos
    d_x, d_y = diamond_pos
    p_x, p_y = platform_pos
    
    d_left = d_x
    d_right = d_x + 20
    d_bottom = d_y - 15
    
    p_top = p_y + 15
    p_left = p_x - 50
    p_right = p_x + 50
    
    return  (d_bottom <= p_top and d_bottom >= p_y) and\
            (d_right >= p_left and d_left <= p_right)


# ===== Keyboard & Mouse Interaction =====
def keyboard_listener(key, x, y):
    """Handles normal keyboard inputs."""
    global paused, cheat
    if game_over:
        return
    
    if key == b'c':
        cheat = not cheat
        print(f"Toggled Cheat Mode: {cheat}!")
    glutPostRedisplay()


def special_key_listener(key, x, y):
    """Handles special keys (arrows, F-keys, etc.)."""
    if paused or game_over:
        return
    
    dx = 7
    if key == GLUT_KEY_LEFT:
        platform_pos[0] -= dx
        if platform_pos[0] < -WIDTH_HALF+50:
            platform_pos[0] = -WIDTH_HALF+50
            
    elif key == GLUT_KEY_RIGHT:
        platform_pos[0] += dx
        if platform_pos[0] > WIDTH_HALF-50:
            platform_pos[0] = WIDTH_HALF-50
            
    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    """
    Handles mouse clicks.
    Left-click: Move ball.
    Right-click: Create a new point.
    """
    global paused, speed, game_over, diamond_pos, platform_pos, color, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        a, b = convert_coordinate(x, y)
        if -10 <= a <= 10 and (HEIGHT_HALF - 30 <= b <= HEIGHT_HALF - 10):
            paused = not paused
            speed[0], speed[1] = speed[1], speed[0]

        if (WIDTH_HALF - 30 <= a <= WIDTH_HALF - 10) and (HEIGHT_HALF - 30 <= b <= HEIGHT_HALF - 10):
            print("Goodbye! Final Score:", score)
            glutLeaveMainLoop()
        
        if (-WIDTH_HALF + 10 <= a <= -WIDTH_HALF + 30) and (HEIGHT_HALF - 30 <= b <= HEIGHT_HALF - 10):
            print("Starting Over!")
            speed[0] = 150
            score = 0
            paused = False
            game_over = False
            diamond_pos = [random.randint(-WIDTH_HALF, WIDTH_HALF - 30), HEIGHT_HALF - 60]
            platform_pos = [0, -HEIGHT_HALF + 10]
            color = random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)


# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-200, 200, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# ===== Display & Animation =====
def display():
    """Main display callback for rendering each frame."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)      #type: ignore
    glLoadIdentity()
    setup_projection()
    
    drawUI()
    drawDiamond()
    drawPlatform()
    
    glutSwapBuffers()
    
def animate():
    """Continuously moves the ball diagonally."""
    global color, diamond_pos, t0, speed, score, game_over, cheat

    t1 = time.time()
    dt = t1 - t0
    t0 = t1
    
    if paused or game_over:
        return
    
    diamond_pos[1] = diamond_pos[1] - speed[0]*dt
    
    if hasCollided():
        diamond_pos[1] = HEIGHT_HALF - 60
        diamond_pos[0] = random.randint(-WIDTH_HALF, WIDTH_HALF - 30)
        color = random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)

        speed[0] += 10
        score += 1
        print(f"Score: {score}")
    
    if diamond_pos[1] < -HEIGHT_HALF:
        game_over = True
        print("Game Over! Final Score:", score)
    
    if cheat:
        if abs(platform_pos[0] - diamond_pos[0] - 10) > 5:
            plt_speed = 2000*dt
            if platform_pos[0] < diamond_pos[0] + 10:
                if platform_pos[0] < WIDTH_HALF - 50:
                    platform_pos[0] += plt_speed
            else:
                if platform_pos[0] > -WIDTH_HALF + 50:
                    platform_pos[0] -= plt_speed
                
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
    glutKeyboardFunc(keyboard_listener)
    glutMouseFunc(mouse_listener)
    glutSpecialFunc(special_key_listener)
    glutMainLoop()


# ===== Entry Point =====
if __name__ == "__main__":
    main()