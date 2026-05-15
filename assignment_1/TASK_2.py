# Task 2
# Controls:
# right clicck-> spawn a coloured bouncing point at click position
# up -> double the speed of all points
# down -> halve the speed of all points
# left click -> toggle blinking of all points
# space-> freeze/unfreeze everything
#no other control works when frozen
# -0------------------------------------------------------

import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# window height width
W, H = 700, 700

# boundary of box
BOX_X1 = 50
BOX_Y1 = 50
BOX_X2 = 650
BOX_Y2 = 650

# Points - each entry = [x, y, dx, dy, r, g, b]
points = []

# speed
speedMultiplier = 1.0

# blinkState
blinking= False
blinkVisible = True
blinkCounter= 0
blinkFrames= 30 # number of idle calls between toggling visibility

# ifFrozen
frozen = False



# coordinate conversion
# GLUT gives mouse coords with y=0 at TOP.
# Our glOrtho puts y=0 at BOTTOM -> flip y.

def convertCoordinate(mx, my):
    
    ox = float(mx)
    oy = float(H - my)
    return ox, oy


def setup_projection():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, 0, 1)
    glMatrixMode(GL_MODELVIEW)


#boundaryBox
def drawBox():
    
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(BOX_X1, BOX_Y1);  glVertex2f(BOX_X2, BOX_Y1) # bottom
    glVertex2f(BOX_X2, BOX_Y1);  glVertex2f(BOX_X2, BOX_Y2)  # right
    glVertex2f(BOX_X2, BOX_Y2);  glVertex2f(BOX_X1, BOX_Y2) # top
    glVertex2f(BOX_X1, BOX_Y2);  glVertex2f(BOX_X1, BOX_Y1) # left
    glEnd()



# all spawned points
def drawPoints():
    
    if blinking and not blinkVisible:
        return   #invisible half of blink cycle

    glPointSize(8)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(p[4], p[5], p[6])
        glVertex2f(p[0], p[1])
    glEnd()



def display():
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    drawBox()
    drawPoints()

    glutSwapBuffers()


def animate():
    
    global blinkCounter, blinkVisible

    if frozen:
        
        glutPostRedisplay()
        return

    # moveAndBounce
    for p in points:
        p[0] += p[2] * speedMultiplier
        p[1] += p[3] * speedMultiplier

        # Bounce off box walls (flip sign of velocity component)
        if p[0] >= BOX_X2:
            p[0] = BOX_X2
            p[2] = -abs(p[2]) # now moves left
        elif p[0] <= BOX_X1:
            p[0] = BOX_X1
            p[2] =  abs(p[2]) #now moves right

        if p[1] >= BOX_Y2:
            p[1] = BOX_Y2
            p[3] = -abs(p[3]) #now moves down
        elif p[1] <= BOX_Y1:
            p[1] = BOX_Y1
            p[3] =  abs(p[3]) # now moves up

    # toggle visibility every blinkFrames idle calls
    if blinking:
        blinkCounter+= 1
        if blinkCounter>= blinkFrames:
            blinkVisible = not blinkVisible
            blinkCounter= 0

    glutPostRedisplay()



def mouseListener(button, state, mx, my):
    
    global blinking, blinkVisible

    # uif frozewn, nothing will work
    if frozen:
        return

    ox, oy = convertCoordinate(mx, my)

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        
        #even a click just outside the box still spawns a point
        ox = max(BOX_X1 + 1.0, min(BOX_X2 - 1.0, ox))
        oy = max(BOX_Y1 + 1.0, min(BOX_Y2 - 1.0, oy))

        # random diagonal direction
        dx = random.choice([-1, 1]) * random.uniform(1.0, 3.0)
        dy = random.choice([-1, 1]) * random.uniform(1.0, 3.0)

        #random bright colour
        r = random.uniform(0.3, 1.0)
        g = random.uniform(0.3, 1.0)
        b = random.uniform(0.3, 1.0)

        points.append([ox, oy, dx, dy, r, g, b])
        print(f"Point spawned at ({ox:.0f}, {oy:.0f})"
              f"direction=({dx:.2f}, {dy:.2f}) total={len(points)}")

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        blinking = not blinking
        
        if not blinking:
            blinkVisible = True   # show all points when blinking turns off
        print(f"Blinking: {blinking}")



def kbListener(key, x, y):
    
    global frozen
    if key == b' ':
        frozen = not frozen
        print(f"Frozen: {frozen}")

def arrowListener(key, x, y):
    global speedMultiplier

    if frozen:
        return #speed controls disabled if frozen

    if key == GLUT_KEY_UP:
        speedMultiplier *= 1.5
        print(f"Speed multiplier: x{speedMultiplier:.2f}")
    elif key == GLUT_KEY_DOWN:
        speedMultiplier = max(0.0225, speedMultiplier / 2.0)
        print(f"Speed multiplier: x{speedMultiplier:.4f}")


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Task 2")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(kbListener)
    glutSpecialFunc(arrowListener)

    glutMainLoop()


if __name__ == "__main__":
    main()