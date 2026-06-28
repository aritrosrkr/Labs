from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

# Grid/wall setup
CELL_SIZE = 100
WALL_HEIGHT = 300

# (cx, cy, width_x, depth_y, height_z)
WALLS = [
    # (-350,   0, 20, 500, WALL_HEIGHT),
    # ( 350,   0, 20, 500, WALL_HEIGHT),
    # (   0, 350, 20, 120, WALL_HEIGHT),
    # (   0,-350, 20, 120, WALL_HEIGHT),
    # (   0,   0, 20, 120, WALL_HEIGHT),
    
    (500 ,-750, 20, 500, WALL_HEIGHT),
    
    (925, -500,150,  20, WALL_HEIGHT),      # Doorway
    (575, -500,150,  20, WALL_HEIGHT),
    
    (500 , 250, 20, 500, WALL_HEIGHT),
    (250 , 500,500,  20, WALL_HEIGHT),
    (-500, 500, 20,1000, WALL_HEIGHT),
    (-500,-750, 20, 500, WALL_HEIGHT)
]

SPAWN = [750, -750, 0]

t0 = time.time()
dt = 0

game_start = False
game_over = False

cheat_mode = False
cheat_vision = False
t0_cshot = 0

fps = True
score = 0
missed = 0
player_lives = 5

player_pos = [*SPAWN]
mvmt_direction = 0
aim_direction = 0

bullets = []
bullet_speed = 2800

fovY = 110  # Field of view
GRID_LENGTH = 1000  # Length of grid lines

enemies = []

# Camera-related variables
cam_h = 1400
cam_r = 800
cam_angle = 0
render_distance = 3000

def convert_coordinate(x, y):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


def draw_wall_box(cx, cy, w, d, h, color=(0.2, 0.2, 0.25)):
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(cx, cy, h*0.5)   # sihft up by h/2 so that base on z=0
    glScalef(w, d, h)
    glutSolidCube(1.0)
    glPopMatrix()


def draw_level1():
    glBegin(GL_QUADS)
    # glVertex3f(500, -500, 0)
    # glVertex3f(500, -1000, 0)
    # glVertex3f(500, -1000, WALL_HEIGHT)
    # glVertex3f(500, -500, WALL_HEIGHT)
    
    # glVertex3f(500, -500, 0)
    # glVertex3f(1000, -500, 0)
    # glVertex3f(1000, -500, WALL_HEIGHT)
    # glVertex3f(500, -500, WALL_HEIGHT)
    
    glVertex3f(500, 0, 0)
    glVertex3f(500, 500, 0)
    glVertex3f(500, 500, WALL_HEIGHT)
    glVertex3f(500, 0, WALL_HEIGHT)
    glEnd()


def draw_floor():
    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH//2, GRID_LENGTH//2, 0)
    glVertex3f(0, GRID_LENGTH//2, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH//2, 0, 0)

    glVertex3f(GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    glVertex3f(0, -GRID_LENGTH//2, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH//2, 0, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)

    glVertex3f(-GRID_LENGTH//2, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    
    glVertex3f(GRID_LENGTH//2, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, GRID_LENGTH//2, 0)
    
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, -GRID_LENGTH, 0)


    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH//2, 0)

    glVertex3f(GRID_LENGTH//2, GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH//2, 0)

    glVertex3f(-GRID_LENGTH, GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH//2, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, -GRID_LENGTH//2, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)

    glVertex3f(-GRID_LENGTH//2, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, GRID_LENGTH//2, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, GRID_LENGTH//2, 0)
    glVertex3f(GRID_LENGTH//2, GRID_LENGTH, 0)

    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, -GRID_LENGTH//2, 0)
    glVertex3f(-GRID_LENGTH//2, -GRID_LENGTH, 0)
    glEnd()


def draw_boundary_walls():
    
    glBegin(GL_QUADS)
    
    glColor(0,0,1)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    
    glColor(0,1,0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)

    glColor(0,1,1)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)

    glColor(1,0,0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    
    glEnd()


def draw_internal_walls():
    for cx, cy, w, d, h in WALLS:
        draw_wall_box(cx, cy, w, d, h, color=(0.25, 0.25, 0.3))


def getHitbox(obj):
    x, y, z, t, *wall = obj
    hb = None
    if t == 'p':                                # player feet-anchored
        hb = (x-30, x+30, y-30, y+30, z, z+180)
    if t == 'e':                                # enemy feet-anchored
        hb = (x-30, x+30, y-30, y+30, z, z+180)
    if t == 'b':                                # bullet center (drawn at z+130)
        z += 102.5
        hb = (x-7.5, x+7.5, y-7.5, y+7.5, z-15, z+15)
    if t == 'w':                                # wall (center + size)
        w, d, h = wall
        hb = (x-w/2, x+w/2, y-d/2, y+d/2, z, z+h)
    return hb


def hasCollided(obj1, obj2):
    ax0, ax1, ay0, ay1, az0, az1 = getHitbox(obj1)
    bx0, bx1, by0, by1, bz0, bz1 = getHitbox(obj2)
    return (ax0 <= bx1 and ax1 >= bx0 and
            ay0 <= by1 and ay1 >= by0 and
            az0 <= bz1 and az1 >= bz0)

    # d_x, d_y, d_z, _ = obj1
    # p_x, p_y, p_z, _ = obj2

    # if obj1[3] == 'b':
    #     d_z += 102.5
    #     dx, dy, dz = 7.5, 7.5, 15           
    # elif obj1[3] == 'p':
    #     dx, dy, dz = 30, 30, 180        # xyz starts at feet level (z=0)
    # elif obj1[3] == 'e':
    #     dx, dy, dz = 40, 40, 160        # xyz starts at feet level (z=0)

    # if obj2[3] == 'b':
    #     p_z += 105
    #     px, py, pz = 5, 5, 10            
    # elif obj2[3] == 'p':
    #     px, py, pz = 30, 30, 180        # xyz starts at feet level (z=0)
    # elif obj2[3] == 'e':
    #     px, py, pz = 40, 40, 160        # xyz starts at feet level (z=0)
    
    # d_left = d_x - dx
    # d_right = d_x + dx
    # d_top = d_z + dz
    # d_bottom = d_z
    # d_near = d_y - dy
    # d_far = d_y + dy
    
    # p_left = p_x - px
    # p_right = p_x + px
    # p_top = p_z + pz
    # p_bottom = p_z
    # p_near = p_y - py
    # p_far = p_y + py
    
    # return  (d_bottom <= p_top and d_bottom >= p_bottom) and\
    #         (d_left <= p_right and d_right >= p_left) and\
    #         (d_near <= p_far and d_far >= p_near)


def wallCollision(x, y, z, t):
    for cx, cy, w, d, h in WALLS:
        if hasCollided((x, y, z, t), (cx, cy, 0, 'w', w, d, h)):
            return True
    return False


def bulletCollision(bx, by, bz):
    global score, missed, enemies
    
    for enemy in enemies:
        ex, ey, ez = enemy[:3]
        if hasCollided((bx, by, bz, 'b'), (ex, ey, ez, 'e')): 
            enemies.remove(enemy)
            return True
    return False


def playerCollision():
    global player_lives, enemies
    px, py, pz = player_pos
    
    for enemy in enemies:
        ex, ey, ez = enemy[:3]
        if hasCollided((px, py, pz, 'p'), (ex, ey, ez, 'e')):
            enemies.remove(enemy)
            return True
    return False


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 800, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_player():
    global player_pos, aim_direction, mvmt_direction
    x, y, z = player_pos
    angle = aim_direction + 90
    
    glPushMatrix()  # Save the current matrix state
    glTranslatef(x, y, z)
    glRotatef(angle, 0, 0, 1)
    
    if game_over:
        glRotatef(-90, 1, 0, 0)
    # hitbox visualization
    # glColor3f(0, 0, 1)
    # glScalef(1, 1, 3)
    # glTranslatef(0, 0, z+30)
    # glutSolidCube(60)
    # glTranslatef(0, 0, z-30)
    # glScalef(1, 1, 0.333)
       
    # legs
    glColor3f(1, 0, 0)
    glTranslatef(-20, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    glTranslatef(40, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    
    # torso
    glColor3f(0, 0, 1)
    glTranslatef(-20, 0, 90) 
    glColor3f(0, 1, 0)
    glScalef(1, 0.5, 1.2)
    glutSolidCube(60) 
    glScalef(1, 2, 0.8333)
    
    # hands
    glColor3f(1, 1, 0)
    glTranslatef(-30, 0, 20)
    glRotatef(90, 1, 0, 0)
    glRotatef(30, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 7, 60, 10, 10)
    glRotatef(-30, 0, 1, 0)
    
    glTranslatef(60, 0, 0)
    glRotatef(-30, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 7, 60, 10, 10)
    glRotatef(30, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    
    # gun
    glColor3f(0.8, 0.8, 0.8)
    glTranslatef(-30, -45, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 10)
    glRotatef(-90, 1, 0, 0)
    
    # head
    # glColor3f(0, 0, 0)
    # glTranslatef(0, 45, 40)
    # gluSphere(gluNewQuadric(), 25, 10, 10)

    glPopMatrix()  # Restore the previous matrix state


def draw_enemy(x, y, z):
    if game_over:
        return
    
    glPushMatrix()  # Save the current matrix state
    # glTranslatef(x, y, z)
    # glRotatef(angle, 0, 0, 1)
    
    # hitbox visualization
    # glColor3f(0, 0, 1)
    # glScalef(1, 1, 3)
    # glTranslatef(0, 0, z+30)
    # glutSolidCube(60)
    # glTranslatef(0, 0, z-30)
    # glScalef(1, 1, 0.333)
       
    # legs
    glColor3f(1, 0, 0)
    glTranslatef(-20, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    glTranslatef(40, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    
    # torso
    glColor3f(0, 0, 1)
    glTranslatef(-20, 0, 90) 
    glColor3f(0, 1, 0)
    glScalef(1, 0.5, 1.2)
    glutSolidCube(60) 
    glScalef(1, 2, 0.8333)
    
    # hands
    glColor3f(1, 1, 0)
    glTranslatef(-30, 0, 20)
    glRotatef(90, 1, 0, 0)
    glRotatef(30, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 7, 60, 10, 10)
    glRotatef(-30, 0, 1, 0)
    
    glTranslatef(60, 0, 0)
    glRotatef(-30, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 7, 60, 10, 10)
    glRotatef(30, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    
    # gun
    glColor3f(0.8, 0.8, 0.8)
    glTranslatef(-30, -45, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 10)
    glRotatef(-90, 1, 0, 0)
    
    # head
    glColor3f(0, 0, 0)
    glTranslatef(0, 45, 40)
    gluSphere(gluNewQuadric(), 25, 10, 10)

    glPopMatrix()  # Restore the previous matrix state
    
    
    # glPushMatrix()  # Save the current matrix state
    # glTranslatef(x, y, z)
    
    # # hitbox visualization
    # # glColor3f(0, 0, 1)
    # # glScalef(1, 1, 2)
    # # glTranslatef(0, 0, 30)
    # # glutSolidCube(80)
    # # glTranslatef(0, 0, -30)
    # # glScalef(1, 1, 0.5)
    
    # glColor3f(1, 0, 0)
    # glTranslatef(0, 0, 40)
    # gluSphere(gluNewQuadric(), 70, 10, 10)
    
    # glColor3f(0, 0, 0)
    # glTranslatef(0, 0, 70)
    # gluSphere(gluNewQuadric(), 50, 10, 10)

    # glPopMatrix()  # Restore the previous matrix 


def draw_bullet(x,y,z):
    glPushMatrix()  # Save the current matrix state

    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(x, y, z)
    glTranslatef(0, 0, 130)
    glutSolidCube(10)

    glPopMatrix()  # Restore the previous matrix

def draw_crosshair():
    if game_over:
        return
    
    global player_pos, aim_direction
    
    glColor3f(1, 1, 1)
    glLineWidth(2)
    
    M = player_pos[0], player_pos[1], player_pos[2]+130
    
    x = M[0] + 700 * math.cos(math.radians(aim_direction))
    y = M[1] + 700 * math.sin(math.radians(aim_direction))
    z = M[2]
    
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 5, 5, 5)
    glPopMatrix()
    
    
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_pos, aim_direction, mvmt_direction, dt, cheat_mode, cheat_vision, score, missed, player_lives, enemies, bullets, game_over
    angle = math.radians(mvmt_direction)

    # Reset the game if R key is pressed
    if key == b'r':
        player_pos = [0,0,0]
        mvmt_direction = 0
        aim_direction = 0
        score = 0
        missed = 0
        player_lives = 5
        enemies.clear()
        bullets.clear()
        game_over = False
        cheat_mode = False
        cheat_vision = False

    if game_over:
        return
    
    # Move forward (W key)
    if key == b'w':  
        player_pos[0] += 30 * math.cos(angle)
        player_pos[1] += 30 * math.sin(angle)
        
    # Move backward (S key)
    if key == b's':
        player_pos[0] -= 30 * math.cos(angle)
        player_pos[1] -= 30 * math.sin(angle)
            
    # Rotate player left (A key)
    if key == b'a':
        player_pos[0] += 30 * math.cos(angle + math.pi/2)
        player_pos[1] += 30 * math.sin(angle + math.pi/2)

    # Rotate player right (D key)
    if key == b'd':
        player_pos[0] += 30 * math.cos(angle - math.pi/2)
        player_pos[1] += 30 * math.sin(angle - math.pi/2)

    # Toggle cheat mode (C key)
    if key == b'c':
        cheat_mode = not cheat_mode
        if not cheat_mode:
            mvmt_direction = aim_direction
    
    # Toggle cheat vision (V key)
    if key == b'v':
        cheat_vision = not cheat_vision
        if not cheat_vision:
            mvmt_direction = aim_direction
            
    # Reset the game if R key is pressed
    if key == b'r':
        player_pos = [0,0,0]
        mvmt_direction = 0
        aim_direction = 0
        score = 0
        missed = 0
        player_lives = 5
        enemies.clear()
        bullets.clear()
        game_over = False
        cheat_mode = False
        cheat_vision = False


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global cam_h, cam_r, cam_angle, fps, game_over
    
    if fps or game_over:
        return

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        cam_angle -= 2  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        cam_angle += 2  # Small angle increment for smooth movement

    if key == GLUT_KEY_DOWN:
        cam_h -= 5 # Small angle decrement for smooth movement
    
    if key == GLUT_KEY_UP:
        cam_h += 5 # Small angle increment for smooth movement


def mouseListener(button, state, x, y):
    if game_over:
        return
    
    global player_pos, mvmt_direction, bullets, game_start, fps
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # Left mouse button fires a bullet
    if game_start and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        angle = math.radians(mvmt_direction)
        x = player_pos[0]
        y = player_pos[1]
        z = player_pos[2]
        bullets.append([x, y, z, angle])  # Store bullet position and direction
        print("Player bullet fired!")
        
    # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        global fps
        fps = not fps


last_mx = None
aim_accum = 0
def mouseMotionListener(x, y):
    if game_over:
        return

    global aim_direction, mvmt_direction, last_mx, aim_accum

    if last_mx is None:
        last_mx = x
        return

    aim_accum -= x - last_mx
    last_mx = x
    aim_direction = mvmt_direction = (aim_accum * 0.8) % 360

    #   wrap around window edges
    if x <= 8 or x >= WINDOW_WIDTH - 8 or y <= 8 or y >= WINDOW_HEIGHT - 8:
        glutWarpPointer(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        last_mx = WINDOW_WIDTH // 2


def setupCamera():
    global player_pos, mvmt_direction, cam_angle, cam_h, cam_r, fps, render_distance
    """
    Configures the camera's projection and view settings.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1, 0.1, render_distance)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Extract camera position and look-at target
    if fps:
        px, py, pz = player_pos[0], player_pos[1], player_pos[2] + 150
        eye_x, eye_y, eye_z = px, py, pz

        a = math.radians(mvmt_direction)
        if cheat_vision:
            a = math.radians(aim_direction)
            
        look_x = eye_x + math.cos(a)
        look_y = eye_y + math.sin(a)
        look_z = eye_z

        gluLookAt(eye_x, eye_y, eye_z,
                  look_x, look_y, look_z,
                  0, 0, 1)
    
    else:
        x = cam_r * math.cos(math.radians(cam_angle))
        y = cam_r * math.sin(math.radians(cam_angle))
        z = cam_h
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)


def idle():
    global game_start, player_pos, fps, aim_direction, mvmt_direction, player_lives, enemies, bullets, bullet_speed, missed, score, t0, dt, game_over, t0_cshot, cheat_mode
    
    t1 = time.time()
    dt = t1 - t0
    t0 = t1
    
    if 500 <= player_pos[0] <= 1000 and -1000 <= player_pos[1] <= -500:
        game_start = False
    elif not game_start and not (500 <= player_pos[0] <= 1000 and -1000 <= player_pos[1] <= -500):
        game_start = True
        
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    if game_over:
        return
    
    if cheat_mode:
        aim_direction = (aim_direction + (600 * dt)) % 360
    
    while len(enemies) < 5:
        while True:
            x = random.randint(-GRID_LENGTH, GRID_LENGTH)
            y = random.randint(-GRID_LENGTH, GRID_LENGTH)
            if abs(x - player_pos[0]) >= 100 and abs(y - player_pos[1]) >= 100:
                if not wallCollision(x, y, 0, 'e'):
                    if x < 500 or y > -500:
                        break
                    
        z = 0
        enemies.append([x, y, z])
    
    t1_cshot = time.time()
    
    if game_start:
        for enemy in enemies:
            direction = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])      # gives radian
            if cheat_mode:
                enemy_dir = (math.degrees(math.atan2(enemy[1] - player_pos[1], enemy[0] - player_pos[0])) + 360) % 360
                diff = abs((aim_direction - enemy_dir + 180) % 360 - 180)
                if (t1_cshot - t0_cshot) >= 0.1 and diff <= 10:
                    bullets.append([player_pos[0], player_pos[1], player_pos[2], math.radians(enemy_dir)])
                    t0_cshot = t1_cshot

            ex = enemy[0] + 50 * math.cos(direction) * dt
            ey = enemy[1] + 50 * math.sin(direction) * dt

            if not wallCollision(ex, ey, enemy[2], 'e'):
                enemy[0] = ex
                enemy[1] = ey
            
        
        if playerCollision():
            player_lives -= 1
            print(f"Player lives remaining: {player_lives}")
            if player_lives <= 0:
                game_over = True
                if fps:
                    fps = False
    
        for bullet in bullets:
            bullet[0] += bullet_speed * math.cos(bullet[3]) * dt
            bullet[1] += bullet_speed * math.sin(bullet[3]) * dt
            
            if wallCollision(bullet[0], bullet[1], bullet[2], 'b'):
                bullets.remove(bullet)
                continue
            
            if abs(bullet[0]) > GRID_LENGTH or abs(bullet[1]) > GRID_LENGTH:
                bullets.remove(bullet)
                missed += 1
                print(f"Missed: {missed}")
                # if missed >= 10:
                #     game_over = True
                #     if fps:
                #         fps = False
                    
            elif bulletCollision(bullet[0], bullet[1], bullet[2]):
                score += 1
                bullets.remove(bullet)
    
    if player_pos[0] > GRID_LENGTH:
        player_pos[0] = GRID_LENGTH
    elif player_pos[0] < -GRID_LENGTH:
        player_pos[0] = -GRID_LENGTH
    if player_pos[1] > GRID_LENGTH:
        player_pos[1] = GRID_LENGTH
    elif player_pos[1] < -GRID_LENGTH:
        player_pos[1] = -GRID_LENGTH
    
    glutPostRedisplay()


scale = [1, 1]
i = scale[0]
pulse_up = True

def showScreen():
    global scale, i, pulse_up, dt
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                # Reset modelview matrix
    glViewport(0, 0, 700, 700)     # Set viewport size

    setupCamera()                   # Configure camera perspective

    draw_floor()
    draw_boundary_walls()
    draw_internal_walls()
    draw_level1()
    
    # Display game info text at a fixed screen position
    draw_text(10, 630, f"Player Lives: {player_lives}")
    draw_text(10, 600, f"Game Score: {score}")
    draw_text(10, 570, f"Bullets Missed: {missed}")
    
    
    draw_player()
    
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2])
    
    # if pulse_up:        # 0.7 < 1
    #     i += 0.5 * dt
    #     if i >= scale[1]:
    #         i = scale[1]
    #         pulse_up = False
            
    # elif i > scale[0]:        # 1 > 0.7
    #     i -= 0.5 * dt
    #     if i <= scale[0]:
    #         i = scale[0]
    #         pulse_up = True
        
    for enemy in enemies:
        direction = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])      # gives radian
        
        glPushMatrix()
        glTranslatef(enemy[0], enemy[1], enemy[2])
        glRotatef(90 + math.degrees(direction), 0, 0, 1)
        glScalef(i, i, i)
        draw_enemy(0,0,0)
        glPopMatrix()
    
    draw_crosshair()
    
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(700, 700)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Project")  # Create the window

    glEnable(GL_DEPTH_TEST)
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    glutWarpPointer(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  # Center the mouse cursor
    glutPassiveMotionFunc(mouseMotionListener)  # Register mouse motion listener for aiming
    glutSetCursor(GLUT_CURSOR_NONE)
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
