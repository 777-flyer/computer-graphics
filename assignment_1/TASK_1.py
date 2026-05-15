# Controls:
# lkeft  Arrow -> move rain to the left
# right Arrow -> move rain to the right
# 'd' key -> will become a day graduallyu
# 'n' key -> will get darker


import random
from OpenGL.GL import *  # mnain drawing functions are here
from OpenGL.GLUT import * # utils for OpenGL, like window or eventListeners
from OpenGL.GLU import *  # imported to use things like glOrtho
import math

# wwindow size
W, H = 900, 500

# here - y=0 => BOTTOM, y=H - TOP
horizon = 195   # y-value where sky meets ground

# rain params
numDrops  = 100
rainDropMove  = 0.5 # postive number means shifting right, left if its negative
rainSpeed = 3.5
drops = [[random.uniform(0, W), random.uniform(0, H)] for _ in range(numDrops)]

# DnN switcher - 0 means night, 1 means day
brightness = 0.0 # start at night

#starting from the bottom left corner

def setup_projection():
    
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, 0, 1)
    glMatrixMode(GL_MODELVIEW)


# util func for drawingg rectangle
# 2 triangles = 1 rectangle
def rectangleByTriangle(x1, y1, x2, y2):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1);  glVertex2f(x2, y1);  glVertex2f(x2, y2)
    glVertex2f(x1, y1);  glVertex2f(x2, y2);  glVertex2f(x1, y2)
    glEnd()


# to draw the sky
def skyDrawer():
    b = brightness
    glColor3f(b * 0.20, b * 0.50, b * 0.90)
    rectangleByTriangle(0, horizon, W, H)


# ground under the sky
def groundDrawer():
    b = brightness
    glColor3f(0.80 + b * 0.12, 0.40 + b * 0.06, 0.05)  # RGB's B is constant and rg get brigher a bit when Day comes
    rectangleByTriangle(0, 0, W, horizon)


# grasses **
def grass():
    b = brightness
    glColor3f(0.0, 0.55 + b * 0.25, 0.0)
    rectangleByTriangle(0, horizon, W, horizon + 18)


# trees using triangles
def trees(cx, base_y, half_w, height):
    glBegin(GL_TRIANGLES)
    glVertex2f(cx - half_w, base_y)  # bottomLeft
    glVertex2f(cx + half_w, base_y)#bottomRight
    glVertex2f(cx, base_y + height) #top
    glEnd()

# treeDrawer
def drawTrees():
    b = brightness
    glColor3f(0.0, 0.70 + b * 0.20, 0.0)

    base_y = horizon + 5   #trees on the grass

    # Left trees (house starts around x=275)
    left_trees = [
        # (center_x, half_width, height)
        (25, 30, 68),
        (70, 25, 62),
        (112, 30, 70),
        (155, 26, 60),
        (196, 28, 65),
        (237, 45, 58),
    ]

    #right trees (house ends at x=635)
    right_trees = [
        (650, 22, 55),
        (685, 20, 50),
        (718, 22, 58),
        (750, 20, 52),
        (782, 23, 60),
        (815, 21, 53),
        (845, 22, 57),
        (875, 20, 50),
    ]

    for (cx, hw, ht) in left_trees + right_trees:
        trees(cx, base_y, hw, ht)



# everything about house
def house():
    
    b = brightness
    CX = 455 # horizontal centre of house
    wallLeft = 275 #wall left edge
    wallRight = 635 #wall right edge
    wallBottom = horizon + 3 # wall bottom (bit upper of grassses)
    wallTop = wallBottom + 105 #wall top

    # walls
    wall_v = 0.85 + b * 0.10
    glColor3f(wall_v, wall_v, wall_v * 0.50)
    rectangleByTriangle(wallLeft, wallBottom, wallRight, wallTop)

    # Roof 
    RX1 = wallLeft - 45
    RX2 = wallRight + 45
    roofStarts = wallTop
    roofTop = roofStarts + 75
    glColor3f(0.40, 0.10, 0.70)
    glBegin(GL_TRIANGLES)
    glVertex2f(RX1, roofStarts)
    glVertex2f(RX2, roofStarts)
    glVertex2f(CX, roofTop)
    glEnd()

    # door
    doorLeft = CX - 27
    doorRight = CX + 27 
    doorX = wallBottom
    doorTop = wallBottom + 68
    glColor3f(0.15, 0.50, 0.95)
    rectangleByTriangle(doorLeft, doorX, doorRight, doorTop)

    # doorLocker
    glColor3f(0,0,0)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(doorLeft + 10, doorX + 35)
    glEnd()

    # left window
    leftWindowLeft = wallLeft + 30
    leftWindowRight = wallLeft + 100
    leftWindowDown = wallBottom + 28
    leftWindowUp = wallTop - 15
    glColor3f(0.10, 0.50, 0.60)
    rectangleByTriangle(leftWindowLeft, leftWindowDown, leftWindowRight, leftWindowUp)
        
    #dividers
    WinMidXL = (leftWindowLeft + leftWindowRight)/ 2
    WinMidYL = (leftWindowDown + leftWindowUp) / 2
    glColor3f(0.90, 0.90, 0.90)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(WinMidXL, leftWindowDown); glVertex2f(WinMidXL, leftWindowUp)
    glVertex2f(leftWindowLeft, WinMidYL); glVertex2f(leftWindowRight, WinMidYL)
    glEnd()

    # Right window
    rightWindowLeft = wallRight - 100
    rightWindowRight = wallRight - 30
    glColor3f(0.10, 0.50, 0.80)
    rectangleByTriangle(rightWindowLeft, leftWindowDown, rightWindowRight, leftWindowUp)
    WinMidXR = (rightWindowLeft + rightWindowRight) / 2
    WinMidYR = (leftWindowDown + leftWindowUp)/ 2
    glColor3f(0.92, 0.92, 0.95)
    glBegin(GL_LINES)
    glVertex2f(WinMidXR, leftWindowDown);   glVertex2f(WinMidXR, leftWindowUp)
    glVertex2f(rightWindowLeft, WinMidYR);  glVertex2f(rightWindowRight, WinMidYR)
    glEnd()

# rains
def rainGenerator():
    
    rainDropLen = 20
    b = brightness
    
    if b < 0.4:
        
        glColor3f(0.35, 0.55, 0.95)   #for darker sky
        
    else:
        
        glColor3f(0.20, 0.30, 0.80)   #deeper when sky is bright

    glLineWidth(1)
    glBegin(GL_LINES)
    
    for drop in drops:
        x, y = drop
        # Current tip of raindrop
        glVertex2f(x, y) # tip
        glVertex2f(x - rainDropMove * 10, y + rainDropLen) # where it is coming from
        
    glEnd()


# display callback
def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    skyDrawer()
    groundDrawer()
    grass()
    drawTrees()
    house()
    rainGenerator()

    glutSwapBuffers()



# animation callback
def animate():
    
    for drop in drops:
        drop[0] += rainDropMove
        drop[1] -= rainSpeed

        if drop[1] < -10:
            
            drop[1] = H + 10
            drop[0] = random.uniform(0, W)
            
        if drop[0] > W + 20:
            drop[0] = -20
            
        elif drop[0] < -20:
            drop[0] = W + 20

    glutPostRedisplay()



# Arrow keys = rain move
def keyListener(key, x, y):
    
    global rainDropMove
    
    if key == GLUT_KEY_LEFT:
        rainDropMove -= 0.4
        print(f"Rain moving: {rainDropMove:.1f}  (leaning left)")
        
    elif key == GLUT_KEY_RIGHT:
        rainDropMove += 0.4
        print(f"Rain moving: {rainDropMove:.1f}  (leaning right)")
        
    glutPostRedisplay()



# d/n keys = day/night
def dnListener(key, x, y):
    
    global brightness
    
    if key == b'd':
        brightness = min(1.0, brightness + 0.05)
        print(f"Brightness {brightness:.2f} -- DAY")
        
    elif key == b'n':
        brightness = max(0.0, brightness - 0.05)
        print(f"Brightness {brightness:.2f} = Night")
        
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Task 1")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(dnListener)
    glutSpecialFunc(keyListener)

    glutMainLoop()


if __name__ == "__main__":
    main()