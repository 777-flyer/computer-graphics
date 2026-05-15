from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

windowW = 1200
windowH = 800

arenaHalf = 600   # arena spans -600 to +600 on both axes
gridDivs = 12    # how many cells per row/col

camX = 0
camY = 1500
camZ = 800
camFov = 50
isFirstPerson = False

# pplayuer state [x, y, z, facinnbgAngle] 
playerData = [0, 0, 0, 0]
walkSpeed = 20
turnDeg = 10
deathTilt= 0  # so that 

# bullet >> [x, y, z, angle]
activeBullets = []
bulletSpeed = 20

# enemies each entry = [x, y, z] 
activeEnemies = []
maxEnemies = 5
chaseSpeed = 0.25
# game stats ot be shown - missed, todo 1
gameScore = 0
# print(gameScore)
# gamescore = 0
livesLeft = 5
shotsMissed = 0
isGameOver = False
# modes
cheatOn = False
# print(cheatOn)
gunFollowOn = False


# enemySpawning

def spawnEnemy():
    
    px = playerData[0]
    py = playerData[1]
    # print(px, py)
    # pz = playerData[2]
    # pr = playerData[3]
    
    while True:
        
        ex = random.uniform(-arenaHalf + 60, arenaHalf - 60)
        ey = random.uniform(-arenaHalf + 60, arenaHalf - 60)
        # print(ex, ey)
        
        if math.hypot(ex - px, ey - py) > 180:
            return [ex, ey, 40]


def fillUpEnemies():
    
    while len(activeEnemies) < maxEnemies:
        
        activeEnemies.append(spawnEnemy())


def restartGame():
    
    global playerData, activeBullets, activeEnemies
    global gameScore, livesLeft, shotsMissed, isGameOver
    global cheatOn, gunFollowOn, isFirstPerson, camFov, deathTilt
    
    playerData = [0, 0, 0, 0]
    
    activeBullets.clear()
    activeEnemies.clear()
    
    gameScore = 0
    livesLeft = 5
    shotsMissed = 0
    isGameOver = False
    cheatOn = False
    gunFollowOn = False
    isFirstPerson = False
    camFov = 50
    deathTilt = 0
    fillUpEnemies()


def setupCamera():
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(camFov, windowW / windowH, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    px = playerData[0]
    py = playerData[1]
    pz = playerData[2]
    pr = playerData[3]
    
    radAngle = math.radians(pr)

    if not isFirstPerson:
        
        gluLookAt(camX, camY, camZ, 0, 0, 0, 0, 0, 1)
        
    else:
        
        eyeX = px + 30 * math.cos(radAngle)
        eyeY = py + 30 * math.sin(radAngle)
        eyeZ = pz + 88

        targetX = px + 110 * math.cos(radAngle)
        targetY = py + 110 * math.sin(radAngle)
        targetZ = pz + 65

        # In cheat mode >> V OFF >> overhead birdeye follow cam
        if cheatOn and not gunFollowOn:
            
            gluLookAt(px, py, pz + 380, px, py, pz,
                      math.cos(radAngle), math.sin(radAngle), 0)
        else:
            
            gluLookAt(eyeX, eyeY, eyeZ, targetX, targetY, targetZ, 0, 0, 1)


def drawScreenText(x, y, msg):
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, windowW, 0, windowH)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in msg:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# floor and walls
def drawArena():
    
    cellSize = (arenaHalf * 2) // gridDivs
    originX = -arenaHalf
    originY = -arenaHalf

    for row in range(gridDivs):
        
        for col in range(gridDivs):
            
            tileX = originX + col * cellSize
            tileY = originY + row * cellSize

            # alternating colours
            if (row + col) % 2 == 0:
                glColor3f(0.71, 0.60, 0.96)
            else:
                glColor3f(0.94, 0.94, 0.94)

            glBegin(GL_QUADS)
            glVertex3f(tileX, tileY, 0)
            glVertex3f(tileX + cellSize, tileY, 0)
            glVertex3f(tileX + cellSize, tileY + cellSize, 0)
            glVertex3f(tileX, tileY + cellSize, 0)
            glEnd()

    wallH = 100

    # southj wall
    glColor3f(0.0, 0.82, 0.82)
    glBegin(GL_QUADS)
    glVertex3f(originX,               originY, 0)
    glVertex3f(originX + arenaHalf*2, originY, 0)
    glVertex3f(originX + arenaHalf*2, originY, wallH)
    glVertex3f(originX,               originY, wallH)
    glEnd()

    # north wall green
    glColor3f(0.18, 0.76, 0.18)
    glBegin(GL_QUADS)
    glVertex3f(originX,               originY + arenaHalf*2, 0)
    glVertex3f(originX + arenaHalf*2, originY + arenaHalf*2, 0)
    glVertex3f(originX + arenaHalf*2, originY + arenaHalf*2, wallH)
    glVertex3f(originX,               originY + arenaHalf*2, wallH)
    glEnd()

    # West wall blue
    glColor3f(0.18, 0.38, 0.88)
    glBegin(GL_QUADS)
    glVertex3f(originX, originY,               0)
    glVertex3f(originX, originY + arenaHalf*2, 0)
    glVertex3f(originX, originY + arenaHalf*2, wallH)
    glVertex3f(originX, originY,               wallH)
    glEnd()

    # East wall oreange
    glColor3f(0.94, 0.52, 0.12)
    glBegin(GL_QUADS)
    glVertex3f(originX + arenaHalf*2, originY,               0)
    glVertex3f(originX + arenaHalf*2, originY + arenaHalf*2, 0)
    glVertex3f(originX + arenaHalf*2, originY + arenaHalf*2, wallH)
    glVertex3f(originX + arenaHalf*2, originY,               wallH)
    glEnd()


def drawPlayer():
    
    global deathTilt

    px = playerData[0]
    py = playerData[1]
    pz = playerData[2]
    pr = playerData[3]

    glPushMatrix()
    glTranslatef(px, py, pz)
    glRotatef(pr, 0, 0, 1)

    # ded bhai mor pls
    if isGameOver:
        if deathTilt < 90:
            deathTilt += 1
        glRotatef(deathTilt, 1, 0, 0)

    # pa 
    glColor3f(0.08, 0.16, 0.52)
    glPushMatrix()
    glTranslatef(-10, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 6, 28, 16, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 6, 28, 16, 8)
    glPopMatrix()

    #boy
    glColor3f(0.30, 0.40, 0.16)
    glPushMatrix()
    glTranslatef(0, 0, 50)
    glScalef(1.1, 1.6, 2.4)
    glutSolidCube(18)
    glPopMatrix()

    #matha
    glColor3f(0.91, 0.76, 0.60)
    glPushMatrix()
    glTranslatef(0, 0, 90)
    gluSphere(gluNewQuadric(), 12, 16, 12)
    glPopMatrix()

    # bamHaat
    glColor3f(0.91, 0.76, 0.60)
    glPushMatrix()
    glTranslatef(0, -13, 48)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 2, 55, 14, 8)
    glPopMatrix()

    # daanhaatr
    glPushMatrix()
    glTranslatef(0, 13, 48)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 2, 55, 14, 8)
    glPopMatrix()

    #gun
    glColor3f(0.22, 0.22, 0.22)
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 6, 2.5, 70, 14, 8)
    glPopMatrix()

    glPopMatrix()


# gulikoro
def fireBullet():
    
    px, py, pz, pr = playerData # unpacking 
    gunLength = 50
    rad = math.radians(pr)
    bx = px + gunLength * math.cos(rad)
    by = py + gunLength * math.sin(rad)
    activeBullets.append([bx, by, pz + 70, pr])



def updateBullets():
    
    global shotsMissed, isGameOver, gameScore

    keptBullets = []
    
    for bullet in activeBullets:
        
        bx, by, bz, angle = bullet
        rad = math.radians(angle)

        bx += bulletSpeed * math.cos(rad)
        by += bulletSpeed * math.sin(rad)
        bullet[0] = bx
        bullet[1] = by

        # missed if bullet goes out of arena bounds
        if abs(bx) > arenaHalf or abs(by) > arenaHalf:
            
            shotsMissed += 1
            
            if shotsMissed >= 10:
                
                isGameOver = True
                
            continue

        # enemy ke hit korse kina
        gotHit = False
        for i in range(len(activeEnemies)):
            
            dist = math.hypot(bx - activeEnemies[i][0], by - activeEnemies[i][1])
            
            if dist < 32:
                
                activeEnemies[i] = spawnEnemy()
                gameScore += 1
                gotHit = True
                
                break

        if gotHit:
            
            continue

        # bullet drawer
        glPushMatrix()
        glTranslatef(bx, by, bz)
        glRotatef(angle, 0, 0, 1)
        glColor3f(0.95, 0.88, 0.1)
        glutSolidCube(10)
        glPopMatrix()

        keptBullets.append(bullet)

    activeBullets.clear()
    for i in keptBullets:
        activeBullets.append(i)
        # print(activeBullets)


# moiing enemies and pulses
def updateEnemies():
    
    global livesLeft
    fillUpEnemies()

    toRemove = []
    elapsedSec = glutGet(GLUT_ELAPSED_TIME) / 1000.0

    for enemy in activeEnemies:
        
        ex, ey, ez = enemy
        px, py = playerData[0], playerData[1]

        dist = math.hypot(px - ex, py - ey)
        # print(dist)

        if dist > 48:
            
            enemy[0] += chaseSpeed * (px - ex) / dist
            enemy[1] += chaseSpeed * (py - ey) / dist
            
        else:
            
            toRemove.append(enemy)
            livesLeft = max(0, livesLeft - 1)

        # Pulsing scale
        pulse = 2.4 + 0.35 * math.sin(2 * math.pi * elapsedSec + ex * 0.01)

        glPushMatrix()
        glTranslatef(enemy[0], enemy[1], ez)
        glScalef(pulse, pulse, pulse)

        # body
        glColor3f(0.92, 0.42, 0.08)
        glutSolidSphere(15, 16, 12)

        #Head 
        glColor3f(0.18, 0.08, 0.02)
        glTranslatef(0, 0, 22)
        glutSolidSphere(9, 16, 12)

        glPopMatrix()

    for dead in toRemove:
        
        if dead in activeEnemies:
            
            activeEnemies.remove(dead)


def runCheatMode():
    
    if not cheatOn or isGameOver:
        
        return

    playerData[3] = (playerData[3] + 1) % 360
    
    rad = math.radians(playerData[3])

    gunTipX = playerData[0] + 50 * math.cos(rad)
    gunTipY = playerData[1] + 50 * math.sin(rad)

    for enemy in activeEnemies:
        
        distToEnemy = math.hypot(enemy[0] - gunTipX, enemy[1] - gunTipY)
        predX = gunTipX + distToEnemy * math.cos(rad)
        predY = gunTipY + distToEnemy * math.sin(rad)

        if abs(predX - enemy[0]) <= 12 and abs(predY - enemy[1]) <= 12:
            
            if len(activeBullets) == 0: 
                
                fireBullet()
                
            break


def showScreen():
    global isGameOver, isFirstPerson, camFov

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, windowW, windowH)

    setupCamera()
    drawArena()
    drawPlayer()

    if not isGameOver:
        
        updateEnemies()
        updateBullets()
        runCheatMode()

        if livesLeft <= 0 or shotsMissed >= 10:
            
            isGameOver = True
            isFirstPerson = False
            camFov = 50

    #HUD
    topLine = windowH - 30
    
    if not isGameOver:
        
        drawScreenText(10, topLine, f"Player Life Remaining: {livesLeft}")
        drawScreenText(10, topLine - 28, f"Game Score: {gameScore}")
        drawScreenText(10, topLine - 56, f"Player Bullet Missed: {shotsMissed}")
        
        if cheatOn:
            
            drawScreenText(10, topLine - 84, "CHEAT MODE ACTIVE")
            
    else:
        
        drawScreenText(10, topLine, f"GAME OVER  |  Final Score: {gameScore}")
        drawScreenText(10, topLine - 28, 'Press R to Restart')

    glutSwapBuffers()


def idleCallback():
    
    glutPostRedisplay()


def keyboardListener(key, x, y):
    
    global cheatOn, gunFollowOn, isGameOver

    if key.lower() == b'r':
        restartGame()
        return

    if isGameOver:
        return

    px, py, pz, pr = playerData
    rad = math.radians(pr)
    lo = -arenaHalf
    hi = arenaHalf

    if key.lower() == b'w':
        
        if cheatOn:
            
            newY = py - walkSpeed
            
            if lo <= newY <= hi:
                
                playerData[1] = newY
                
        else:
            
            newX = px + walkSpeed * math.cos(rad)
            newY = py + walkSpeed * math.sin(rad)
            
            if lo <= newX <= hi:
                playerData[0] = newX
            if lo <= newY <= hi:
                playerData[1] = newY
                

    elif key.lower() == b's':
        
        if cheatOn:
            
            newY = py + walkSpeed
            
            if lo <= newY <= hi:
                playerData[1] = newY
                
        else:
            
            newX = px - walkSpeed * math.cos(rad)
            newY = py - walkSpeed * math.sin(rad)
            
            if lo <= newX <= hi:
                playerData[0] = newX
            if lo <= newY <= hi:
                playerData[1] = newY

    elif key.lower() == b'a':
        
        if cheatOn:
            
            newX = px + walkSpeed
            
            if lo <= newX <= hi:
                playerData[0] = newX
                
        else:
            
            playerData[3] = (pr + turnDeg) % 360

    elif key.lower() == b'd':
        
        if cheatOn:
            
            newX = px - walkSpeed
            
            if lo <= newX <= hi:
                playerData[0] = newX
                
        else:
            playerData[3] = (pr - turnDeg) % 360

    elif key == b'c':
        
        cheatOn = not cheatOn

    elif key == b'v':
        gunFollowOn = not gunFollowOn

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global camX, camY, camZ

    if isFirstPerson:
        return

    step = 5
    orbitRad = math.radians(step / 2)

    if key == GLUT_KEY_UP:
        
        camZ += step
        
    elif key == GLUT_KEY_DOWN:
        camZ -= step
        
    elif key == GLUT_KEY_LEFT:
        
        nx = camX * math.cos(orbitRad) - camY * math.sin(orbitRad)
        ny = camX * math.sin(orbitRad) + camY * math.cos(orbitRad)
        camX, camY = nx, ny
        
    elif key == GLUT_KEY_RIGHT:
        
        nx = camX * math.cos(-orbitRad) - camY * math.sin(-orbitRad)
        ny = camX * math.sin(-orbitRad) + camY * math.cos(-orbitRad)
        
        camX, camY = nx, ny

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    
    global isFirstPerson, camFov

    if state != GLUT_DOWN:
        return

    if button == GLUT_LEFT_BUTTON and not isGameOver:
        fireBullet()

    elif button == GLUT_RIGHT_BUTTON and not isGameOver:
        
        isFirstPerson = not isFirstPerson
        camFov = 80 if isFirstPerson else 50


def main():
    
    fillUpEnemies()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(windowW, windowH)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy >> CSE423 Lab 3")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idleCallback)

    glutMainLoop()


if __name__ == "__main__":
    main()