from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Camera-related variables
camera_pos = (0,500,500)
camera_angle_deg = 90.0   # 90° => (x=0, y=+radius)
camera_radius = 700.0
camera_height = 500.0

fovY = 100  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
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


def draw_shapes():

    glPushMatrix()  # Save the current matrix state
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
    
    # gun
    glColor3f(0.8, 0.8, 0.8)
    glTranslatef(-30, 0, 45)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
    
    # head
    glColor3f(0, 0, 0)
    glTranslatef(0, 35, -50)
    gluSphere(gluNewQuadric(), 25, 10, 10)
    
    glPopMatrix()  # Restore the previous matrix state
    # glScalef(2, 2, 2)
    # gluCylinder(gluNewQuadric(), 15, 20, 60, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100) 
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    glPopMatrix()  # Restore the previous matrix state


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':  

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_angle_deg, camera_height

    # Rotate camera around origin (constant radius)
    if key == GLUT_KEY_LEFT:
        camera_angle_deg -= 2.0
    if key == GLUT_KEY_RIGHT:
        camera_angle_deg += 2.0

    # Move camera up/down
    if key == GLUT_KEY_UP:
        camera_height += 10.0
    if key == GLUT_KEY_DOWN:
        camera_height -= 10.0


# def specialKeyListener(key, x, y):
#     """
#     Handles special key inputs (arrow keys) for adjusting the camera angle and height.
#     """
#     global camera_pos
#     x, y, z = camera_pos
#     # Move camera up (UP arrow key)
#     # if key == GLUT_KEY_UP:

#     # # Move camera down (DOWN arrow key)
#     # if key == GLUT_KEY_DOWN:

#     # moving camera left (LEFT arrow key)
#     if key == GLUT_KEY_LEFT:
#         x -= 1  # Small angle decrement for smooth movement

#     # moving camera right (RIGHT arrow key)
#     if key == GLUT_KEY_RIGHT:
#         x += 1  # Small angle increment for smooth movement

#     if key == GLUT_KEY_DOWN:
#         y -= 1 # Small angle decrement for smooth movement
    
#     if key == GLUT_KEY_UP:
#         y += 1 # Small angle increment for smooth movement
        
#     camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
        # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def setupCamera():
    """
    Configures the camera's projection and view settings.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Compute orbit position from angle + fixed radius
    rad = math.radians(camera_angle_deg)
    cam_x = camera_radius * math.cos(rad)
    cam_y = camera_radius * math.sin(rad)
    cam_z = camera_height

    gluLookAt(
        cam_x, cam_y, cam_z,  # camera position
        0, 0, 0,              # look-at target
        0, 0, 1               # up vector
    )


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)


    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")

    draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
