from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

t0 = time.time()
dt = 0

game_over = False

cheat_mode = False
cheat_vision = False
t0_cshot = 0

fps = False
score = 0
missed = 0
player_lives = 5

player_pos = [0,0,0]
mvmt_direction = 0
aim_direction = 0

bullets = []
bullet_speed = 2800

fovY = 100  # Field of view
GRID_LENGTH = 1000  # Length of grid lines

enemies = []

# Camera-related variables
cam_h = 1400
cam_r = 800
cam_angle = 0

def hasCollided(obj1, obj2):
    d_x, d_y, d_z, _ = obj1
    p_x, p_y, p_z, _ = obj2

    if obj1[3] == 'b':
        d_z += 102.5
        dx, dy, dz = 7.5, 7.5, 15           
    elif obj1[3] == 'p':
        dx, dy, dz = 30, 30, 180        # xyz starts at feet level (z=0)
    elif obj1[3] == 'e':
        dx, dy, dz = 40, 40, 160        # xyz starts at feet level (z=0)

    if obj2[3] == 'b':
        p_z += 105
        px, py, pz = 5, 5, 10            
    elif obj2[3] == 'p':
        px, py, pz = 30, 30, 180        # xyz starts at feet level (z=0)
    elif obj2[3] == 'e':
        px, py, pz = 40, 40, 160        # xyz starts at feet level (z=0)
    
    d_left = d_x - dx
    d_right = d_x + dx
    d_top = d_z + dz
    d_bottom = d_z
    d_near = d_y - dy
    d_far = d_y + dy
    
    p_left = p_x - px
    p_right = p_x + px
    p_top = p_z + pz
    p_bottom = p_z
    p_near = p_y - py
    p_far = p_y + py
    
    return  (d_bottom <= p_top and d_bottom >= p_bottom) and\
            (d_left <= p_right and d_right >= p_left) and\
            (d_near <= p_far and d_far >= p_near)


def bulletCollision(bx, by, bz):
    global score, missed, enemies
    
    for enemy in enemies:
        ex, ey, ez, _ = enemy
        if hasCollided((bx, by, bz, 'b'), (ex, ey, ez, 'e')): 
            enemies.remove(enemy)
            return True
    return False


def playerCollision():
    global player_lives, enemies
    px, py, pz = player_pos
    
    for enemy in enemies:
        ex, ey, ez, _ = enemy
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
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
    glRotatef(-90, 1, 0, 0)
    
    # head
    glColor3f(0, 0, 0)
    glTranslatef(0, 45, 40)
    gluSphere(gluNewQuadric(), 25, 10, 10)

    glPopMatrix()  # Restore the previous matrix state


def draw_enemy(x,y,z):
    if game_over:
        return
    
    glPushMatrix()  # Save the current matrix state
    glTranslatef(x, y, z)
    
    # hitbox visualization
    # glColor3f(0, 0, 1)
    # glScalef(1, 1, 2)
    # glTranslatef(0, 0, 30)
    # glutSolidCube(80)
    # glTranslatef(0, 0, -30)
    # glScalef(1, 1, 0.5)
    
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 50, 10, 10)
    
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 50)
    gluSphere(gluNewQuadric(), 30, 10, 10)

    glPopMatrix()  # Restore the previous matrix 


def draw_bullet(x,y,z):
    glPushMatrix()  # Save the current matrix state

    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(x, y, z)
    glTranslatef(0, 0, 110)
    glutSolidCube(15)

    glPopMatrix()  # Restore the previous matrix


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
        player_pos[0] += 20 * math.cos(angle)
        player_pos[1] += 20 * math.sin(angle)
        
        if player_pos[0] > GRID_LENGTH:
            player_pos[0] = GRID_LENGTH
        elif player_pos[0] < -GRID_LENGTH:
            player_pos[0] = -GRID_LENGTH
        if player_pos[1] > GRID_LENGTH:
            player_pos[1] = GRID_LENGTH
        elif player_pos[1] < -GRID_LENGTH:
            player_pos[1] = -GRID_LENGTH
        
    # Move backward (S key)
    if key == b's':
        player_pos[0] -= 20 * math.cos(angle)
        player_pos[1] -= 20 * math.sin(angle)

        if player_pos[0] > GRID_LENGTH:
            player_pos[0] = GRID_LENGTH
        elif player_pos[0] < -GRID_LENGTH:
            player_pos[0] = -GRID_LENGTH
        if player_pos[1] > GRID_LENGTH:
            player_pos[1] = GRID_LENGTH
        elif player_pos[1] < -GRID_LENGTH:
            player_pos[1] = -GRID_LENGTH
            
    # Rotate player left (A key)
    if key == b'a':
        mvmt_direction += 5
        if not cheat_mode:
            aim_direction = mvmt_direction

    # Rotate player right (D key)
    if key == b'd':
        mvmt_direction -= 5
        if not cheat_mode:
            aim_direction = mvmt_direction

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
    
    global player_pos, mvmt_direction, bullets
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
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


def setupCamera():
    global player_pos, mvmt_direction, cam_angle, cam_h, cam_r, fps
    """
    Configures the camera's projection and view settings.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1, 0.1, 15000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Extract camera position and look-at target
    if fps:
        px, py, pz = player_pos[0], player_pos[1], player_pos[2]+150
        eye_x, eye_y, eye_z = px, py, pz+50

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
    global player_pos, fps, aim_direction, mvmt_direction, player_lives, enemies, bullets, bullet_speed, missed, score, t0, dt, game_over, t0_cshot, cheat_mode
    
    t1 = time.time()
    dt = t1 - t0
    t0 = t1
    
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
            if abs(x - player_pos[0]) >= 50 and abs(y - player_pos[1]) >= 50:
                break
        z = 0
        shot = False
        enemies.append([x, y, z, shot])
    
    t1_cshot = time.time()
    
    for enemy in enemies:
        direction = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])      # gives radian
        # shot = enemy[3]
        if cheat_mode:
            enemy_dir = (math.degrees(math.atan2(enemy[1] - player_pos[1], enemy[0] - player_pos[0])) + 360) % 360
            diff = abs((aim_direction - enemy_dir + 180) % 360 - 180)
            if (t1_cshot - t0_cshot) >= 0.1 and diff <= 10:
                # print(enemy_dir, aim_direction%360)
                bullets.append([player_pos[0], player_pos[1], player_pos[2], math.radians(enemy_dir)])
                t0_cshot = t1_cshot
                # enemy[3] = True
        
        enemy[0] += 50 * math.cos(direction) * dt
        enemy[1] += 50 * math.sin(direction) * dt
        
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
        
        if abs(bullet[0]) > GRID_LENGTH or abs(bullet[1]) > GRID_LENGTH:
            bullets.remove(bullet)
            missed += 1
            print(f"Missed: {missed}")
            if missed >= 10:
                game_over = True
                if fps:
                    fps = False
                
        elif bulletCollision(bullet[0], bullet[1], bullet[2]):
            score += 1
            bullets.remove(bullet)
    
    glutPostRedisplay()


scale = [0.7, 1]
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
    
    
    glBegin(GL_QUADS)
    
    glColor(0,0,1)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    
    glColor(0,1,0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)

    glColor(0,1,1)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)

    glColor(1,0,0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    
    glEnd()
    
    # Display game info text at a fixed screen position
    draw_text(10, 630, f"Player Lives: {player_lives}")
    draw_text(10, 600, f"Game Score: {score}")
    draw_text(10, 570, f"Bullets Missed: {missed}")
    
    draw_player()
    
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2])
    
    if pulse_up:        # 0.7 < 1
        i += 0.5 * dt
        if i >= scale[1]:
            i = scale[1]
            pulse_up = False
            
    elif i > scale[0]:        # 1 > 0.7
        i -= 0.5 * dt
        if i <= scale[0]:
            i = scale[0]
            pulse_up = True
        
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy[0], enemy[1], enemy[2])
        glScalef(i, i, i)
        draw_enemy(0,0,0)
        glPopMatrix()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(700, 700)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Assignment-3")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
