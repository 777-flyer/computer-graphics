# ----------------------------------------------------------------
# 423 Assignment 2
# ----------------------------------------------------------------

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700

# for diamond
DIAMOND_HALF_W = 12 # halfwidth of diamond shape
DIAMOND_HALF_H = 20 # half height
BASE_SPEED = 90.0  # starting falling speed in pixels/second

# catcher
CATCHER_Y = -310   # vertifally fixed
CATCHER_TOP_HALF_W = 50 # wider side, TE half width
CATCHER_BOT_HALF_W = 32  # BE half width
CATCHER_RIM_H = 14   # height of the catcher shape
CATCHER_STEP = 8  #pixels moved per arrow key press

# buttons
BTN_Y = 300
BTN_LEFT_X = -190    # rleft arrow [we can restart using this]
BTN_MID_X = 0 # pause/play
BTN_RIGHT_X = 190 # --> X
BTN_RADIUS = 28    # click detection radius

# glibals
score = 0
game_over = False
paused = False
cheat_mode = False
#--- for diamond
diamond_x = 0.0
diamond_y = 0.0
diamond_color = (1.0, 1.0, 0.0)
diamond_speed = BASE_SPEED
#--- for catchser
catcher_x = 0.0
catcher_color = (1.0, 1.0, 1.0) # white normally, red on game-over

last_time = 0.0


# mid point line drawing algo
def find_zone(x1, y1, x2, y2):
    
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy): 
        
          
        # |slope| <= 1  →  zones 0, 3, 4, 7
        if dx >= 0 and dy >= 0: 
            return 0
        elif dx < 0 and dy >= 0: 
            return 3
        elif dx < 0 and dy < 0: 
            return 4
        else: 
            return 7   # dx>=0, dy<0
    
    
    else:      
                             
        # |slope| > 1  →  zones 1, 2, 5, 6
        
        if dx>= 0 and dy>= 0: 
            return 1
        elif dx < 0 and dy>= 0: 
            return 2
        
        elif dx < 0 and dy < 0: 
            return 5
        else: 
            return 6   # dx>=0, dy<0


def to_zone0(x, y, zone):
    
    if zone == 0: 
        return x, y
    if zone == 1: 
        return y, x
    if zone == 2: 
        return y, -x
    if zone == 3: 
        return -x, y
    if zone == 4: 
        return -x, -y
    if zone == 5: 
        return -y, -x
    if zone == 6: 
        return -y,  x
    if zone == 7: 
        return x, -y


def from_zone0(x, y, zone):
    
    if zone == 0: 
        return x,  y
    if zone == 1: 
        return y, x
    if zone == 2: 
        return -y, x
    if zone == 3: 
        return -x, y
    if zone == 4: 
        return -x, -y
    if zone == 5: 
        return -y, -x
    if zone == 6: 
        return y, -x
    if zone == 7: 
        return x, -y


def _midpoint_zone0(x1, y1, x2, y2, zone):
    
    # glBegin(GL_POINTS) ./ glEnd()
    # works for z0 --> (dx>0, dy>=0, dx>=dy)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx # initial decision
    incE = 2 * dy #incr : E
    incNE = 2 * (dy - dx) # incr when we go NE
    y = y1

    for x in range(x1, x2 + 1):

        rx, ry = from_zone0(x, y, zone) # before drawing, we convert it back to originsl zons
        glVertex2f(rx, ry)

        if d > 0: #midpoint is below line → go NE
            d += incNE
            y += 1

        else: # midpoint is above line → go E
            d += incE


def draw_line(x1, y1, x2, y2):
    

    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    # case: single point

    if x1 == x2 and y1 == y2:

        glBegin(GL_POINTS)
        glVertex2f(x1, y1)
        glEnd()
        return

    # 1 : find zone
    zone = find_zone(x1, y1, x2, y2)

    # 2 : convert both endpoints to Zone 0
    tx1, ty1 = to_zone0(x1, y1, zone)
    tx2, ty2 = to_zone0(x2, y2, zone)

    # 3 : ensure left to right for z0 algo
    if tx1 > tx2:
        tx1, ty1, tx2, ty2 = tx2, ty2, tx1, ty1

    # 4 : Z0 midpoint algo(converts back inside)
    glBegin(GL_POINTS)
    _midpoint_zone0(tx1, ty1, tx2, ty2, zone)
    glEnd()



def draw_diamond(cx, cy, color):

    glColor3f(*color)
    glPointSize(2)
    hw = DIAMOND_HALF_W
    hh = DIAMOND_HALF_H
    draw_line(cx, cy + hh, cx + hw, cy) # top→ right
    draw_line(cx + hw, cy, cx, cy - hh)  # right → bottom
    draw_line(cx, cy - hh, cx - hw, cy) # bottom→ left
    draw_line(cx - hw, cy, cx, cy + hh) # left→ top


def draw_catcher(cx, cy, color):

    glColor3f(*color)
    glPointSize(2)
    tw = CATCHER_TOP_HALF_W
    bw = CATCHER_BOT_HALF_W
    h  = CATCHER_RIM_H
    # Four corners
    tl = (cx - tw, cy + h) # topleft
    tr = (cx + tw, cy + h) # topright
    br = (cx + bw, cy) # bottomright
    bl = (cx - bw, cy) # bottomleft
    draw_line(*tl, *tr) # top edge
    draw_line(*tr, *br) # right side
    draw_line(*br, *bl) # bottom edge
    draw_line(*bl, *tl) # left side


def draw_restart_button(cx, cy):

    glColor3f(0.0, 0.9, 0.9)
    glPointSize(2)
    s = 18 # arrowhead size
    draw_line(cx + s, cy + s, cx - s, cy) # upper of arrow
    draw_line(cx - s, cy, cx + s, cy - s)   # lower of arrow
    draw_line(cx - s, cy, cx + s, cy) # ------ >>


def draw_pause_button(cx, cy):

    glColor3f(1.0, 0.75, 0.0) 
    glPointSize(2)
    bh = 20 # bar half height
    g = 8    # gap from c
    draw_line(cx - g, cy - bh, cx - g, cy + bh) #left bar
    draw_line(cx + g, cy - bh, cx + g, cy + bh) #ight bar


def draw_play_button(cx, cy):

    glColor3f(1.0, 0.75, 0.0)  
    glPointSize(2)
    
    s = 20

    tlx, tly = cx - s, cy + s
    blx, bly = cx - s, cy - s
    rx, ry  = cx + s, cy
    draw_line(tlx, tly, rx, ry ) #top left  -> right tip
    draw_line(rx, ry, blx, bly) # right tip -> bottom left
    draw_line(blx, bly, tlx, tly) # bottom left -> top left 


def draw_close_button(cx, cy):

    glColor3f(1.0, 0.0, 0.0)   
    glPointSize(2)
    
    s = 20
    
    draw_line(cx - s, cy - s, cx + s, cy + s) # \ line
    draw_line(cx - s, cy + s, cx + s, cy - s)  # / line



def setup_projection():

    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -350, 350, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def convert_coordinate(x, y):

    a = x - (WINDOW_WIDTH  / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b



def random_bright_color():

    palette = [(1.0, 1.0, 0.0),(0.0, 1.0, 1.0),   (1.0, 0.0, 1.0),  (1.0, 0.5, 0.0), (0.4, 1.0, 0.0),  (0.8, 0.0, 1.0), (1.0, 0.0, 0.4), (0.0, 0.8, 1.0),]
    
    return random.choice(palette)


def spawn_diamond():

    global diamond_x, diamond_y, diamond_color
    
    diamond_x = float(random.randint(-210, 210))
    diamond_y = 280.0
    diamond_color = random_bright_color()


def reset_game():

    global score, game_over, paused, cheat_mode
    global diamond_speed, catcher_x, catcher_color, last_time
    
    score = 0
    
    game_over = False
    paused = False
    cheat_mode = False
    
    diamond_speed = BASE_SPEED
    
    catcher_x = 0.0
    catcher_color = (1.0, 1.0, 1.0)
    
    spawn_diamond()
    
    last_time = time.time()


def aabb_collision():
   
    # dm bounding box
    d_l = diamond_x - DIAMOND_HALF_W
    d_r = diamond_x + DIAMOND_HALF_W
    d_b = diamond_y - DIAMOND_HALF_H
    d_t = diamond_y + DIAMOND_HALF_H

    # catching bounding box
    c_l = catcher_x - CATCHER_TOP_HALF_W
    c_r = catcher_x + CATCHER_TOP_HALF_W
    c_b = CATCHER_Y
    c_t = CATCHER_Y + CATCHER_RIM_H

    return (d_l < c_r and d_r > c_l and
            d_b < c_t and d_t > c_b)


def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    # btns
    draw_restart_button(BTN_LEFT_X, BTN_Y)
    
    if paused or game_over:
        
        draw_play_button(BTN_MID_X, BTN_Y) 
        
    else:
        
        draw_pause_button(BTN_MID_X, BTN_Y)   
        
    draw_close_button(BTN_RIGHT_X, BTN_Y)

    if not game_over:
        
        draw_diamond(int(diamond_x), int(diamond_y), diamond_color)

    # catcher
    draw_catcher(int(catcher_x), CATCHER_Y, catcher_color)

    glutSwapBuffers() 


def animate():
    
    global diamond_y, diamond_x, score, game_over
    global diamond_speed, catcher_x, catcher_color, last_time

    current_time = time.time()
    # timeCatcher = time.time()
    dt = current_time - last_time
    dt = min(dt, 0.05) # cap to 50 ms to avoid big jumps on first frame
    last_time = current_time

    if game_over or paused:
        
        glutPostRedisplay()
        return

    if cheat_mode:
        diff = diamond_x - catcher_x
        step = min(abs(diff), 7.0) # smooth teleport
        
        if diff > 0: 
            catcher_x += step
            
        elif diff < 0: 
            catcher_x -= step

    # mv diamond down
    diamond_y -= diamond_speed * dt

     # checking if we can catch it or not
    if aabb_collision():
        
        score += 1
        diamond_speed += 8.0 
        print(f"Score: {score}")
        spawn_diamond()


    if diamond_y + DIAMOND_HALF_H < -350:
        game_over = True
        catcher_color = (1.0, 0.0, 0.0)
        print(f"Game Over! Score: {score}")

    glutPostRedisplay()


def keyboard_listener(key, x, y):

    global cheat_mode
    
    if key == b'c' and not game_over:
        
        cheat_mode = not cheat_mode
        state = "ON" if cheat_mode else "OFF"
        
        print(f"Cheat Mode: {state}")
        
    glutPostRedisplay()


def special_key_listener(key, x, y):

    global catcher_x
    
    if game_over or paused:
        return
    
    max_reach = 250 - CATCHER_TOP_HALF_W
    
    if key == GLUT_KEY_LEFT:
        
        catcher_x = max(catcher_x - CATCHER_STEP, -max_reach)
        
    elif key == GLUT_KEY_RIGHT:
        
        catcher_x = min(catcher_x + CATCHER_STEP,  max_reach)
        
    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    
    global paused
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        mx, my = convert_coordinate(x, y)

        if abs(mx - BTN_LEFT_X) < BTN_RADIUS and abs(my - BTN_Y) < BTN_RADIUS:
            
            print("Starting over!")
            reset_game()

        elif abs(mx - BTN_MID_X) < BTN_RADIUS and abs(my - BTN_Y) < BTN_RADIUS:
            
            if not game_over:
                
                paused = not paused

        # (X)
        elif abs(mx - BTN_RIGHT_X) < BTN_RADIUS and abs(my - BTN_Y) < BTN_RADIUS:
            
            
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()

    glutPostRedisplay()


def main():
    
    reset_game()
    
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


if __name__ == "__main__":
    main()