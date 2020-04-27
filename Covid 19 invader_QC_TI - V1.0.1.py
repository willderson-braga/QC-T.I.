# PROJETO EM PYGAME GRUPO QC TI UNIVERSIDADE UNIGRANRIO SOB LICENÇA DO DESENVOLVEDOR  MARK VANSTONE (TECHNOVISUAL)
# ESTE PROJETO ESTA SENDO USADO PARA ESTUDO DA LINGUAGEM PYTHON SEM FINS LUCRATIVOS
# VERSAO 1.0

import pgzrun
from random import randint
import math
import pygame


DIFFICULTY = 1
player = Actor("player", (400, 550)) # Carregar na imagem da seringa


def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    player.image = player.images[math.floor(player.status/6)]
    player.draw()
    drawLasers()
    drawAliens()
    drawBases()
    screen.draw.text(str(score) , topright=(780, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=40)
    if player.status >= 30:
        screen.draw.text("O JOGO ACABOU\nPressione Enter para jogar de novo" , center=(400, 300), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)
    if len(aliens) == 0 :
        screen.draw.text("VOCÊ GANHOU !!!\nPressione Enter para jogar de novo. Não esqueça lave as mãos" , center=(400, 300), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=35)
        
def update(): # Pygame Zero update function
    global moveCounter,player
    if player.status < 30 and len(aliens) > 0:
        checkKeys()
        updateLasers()
        moveCounter += 1
        if moveCounter == moveDelay:
            moveCounter = 0
            updateAliens() 
        if player.status > 0: player.status += 1
    else:
        if keyboard.RETURN: init()

def drawAliens():
    for a in range(len(aliens)): aliens[a].draw()

def drawBases():
    for b in range(len(bases)): bases[b].drawClipped()

def drawLasers():
    for l in range(len(lasers)): lasers[l].draw()

def checkKeys():
    global player, lasers
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
    if keyboard.space:
        if player.laserActive == 1:
            player.laserActive = 0
            clock.schedule(makeLaserActive, 1.0)
            l = len(lasers)
            lasers.append(Actor("laser2", (player.x,player.y-32)))
            lasers[l].status = 0
            lasers[l].type = 1

def makeLaserActive():
    global player
    player.laserActive = 1
            
def checkBases():
    for b in range(len(bases)):
        if l < len(bases):
            if bases[b].height < 5:
                del bases[b]

def updateLasers():
    global lasers, aliens
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += (2*DIFFICULTY)
            checkLaserHit(l)
            if lasers[l].y > 600: lasers[l].status = 1
        if lasers[l].type == 1:
            lasers[l].y -= 5
            checkPlayerLaserHit(l)
            if lasers[l].y < 10: lasers[l].status = 1
    lasers = listCleanup(lasers)
    aliens = listCleanup(aliens)

def listCleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0: newList.append(l[i])
    return newList
    
def checkLaserHit(l):
    global player
    if player.collidepoint((lasers[l].x, lasers[l].y)):
        player.status = 1
        lasers[l].status = 1
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]):
            bases[b].height -= 10
            lasers[l].status = 1

def checkPlayerLaserHit(l):
    global score
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]): lasers[l].status = 1
    for a in range(len(aliens)):
        if aliens[a].collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            aliens[a].status = 1
            score += 1000
            
def updateAliens():
    global moveSequence, lasers, moveDelay
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30: movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 50 + (10 * DIFFICULTY)
        moveDelay -= 1
    if moveSequence >10 and moveSequence < 30: movex = 15
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            aliens[a].image = "alien1"
        else:
            aliens[a].image = "alien1b"
            if randint(0, 5) == 0:
                lasers.append(Actor("laser1", (aliens[a].x,aliens[a].y)))
                lasers[len(lasers)-1].status = 0
                lasers[len(lasers)-1].type = 0
        if aliens[a].y > player.y and player.status == 0:
            player.status = 1
    moveSequence +=1
    if moveSequence == 40: moveSequence = 0


def updateBoss():
    global boss, level, player, lasers
    if boss.active:
        boss.y += (0.3*level)
        if boss.direction == 0: boss.x -= (1* level)
        else: boss.x += (1* level)
        if boss.x < 100: boss.direction = 1
        if boss.x > 700: boss.direction = 0
        if boss.y > 500:
            sounds.explosion.play()
            player.status = 1
            boss.active = False
        if randint(0, 30) == 0:
            lasers.append(Actor("laser1", (boss.x,boss.y)))
            lasers[len(lasers)-1].status = 0
            lasers[len(lasers)-1].type = 0
    else:
        if randint(0, 800) == 0:
            boss.active = True
            boss.x = 800
            boss.y = 100
            boss.direction = 0

def init():
    global lasers, score, player, moveSequence, moveCounter, moveDelay
    initAliens()
    initBases()
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    lasers = []
    moveDelay = 30
    player.images = ["player","explosion1","explosion2","explosion3","explosion4","explosion5"]
    player.laserActive = 1

def initAliens():
    global aliens
    aliens = []
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80,100+(int(a/6)*64))))
        aliens[a].status = 0

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def collideLaser(self, other):
    return (
        self.x-20 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )

def initBases():
    global bases
    bases = []
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("base1", midbottom=(150+(b*200)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            bases[bc].collideLaser = collideLaser.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1

init()
pgzrun.go()
