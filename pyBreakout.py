#!/usr/bin/env python3

import pygame, sys, time
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
from pygame.math import Vector2
from random import randint

ballradius = 5

# Fenstergröße
windowWidth = 640
windowHeight = 480

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

sounds = {'wand': pygame.mixer.Sound('Musik/Wallhit.aiff'),
          'block': pygame.mixer.Sound('Musik/blockhit.wav'),
          'win': pygame.mixer.Sound('Musik/win.aiff'),
          'ball weg': pygame.mixer.Sound('Musik/ballweg.wav'),
          'death': pygame.mixer.Sound('Musik/death.aiff')}


class Spiel(object):
    def __init__(self, breite=640, hoehe=480, title='Spiel'):
        pygame.init()
        self.screen = pygame.display.set_mode((breite, hoehe))
        pygame.display.set_caption(title)

    def clearScreen(self):
        spiel.screen.fill((0,0,0))

    def updateScreen(self):
        pygame.display.update()


class Ball(object):
    def __init__(self, surface, posx=0, posy=0, radius=5, color=(255,255,255)):
        self.surface = surface
        self.x = posx
        self.y = posy
        self.radius = radius
        self.color = color
        self.v = Vector2(0, 0)
        

    def draw(self):
        pygame.draw.circle(self.surface, self.color, 
            (int(self.x), int(self.y)), self.radius)

    def setSchlaeger(self, schlaeger):
        self.schlaeger = schlaeger
        
    def setZiele(self, ziele):
        self.ziele = ziele

    def collidesWithZiel(self):
        for ziel in self.ziele:
            
            Abstandx = 10000
            Abstandy = 10000
            
            # Wenn Ball zwischen linkem und rechtem Rand des Ziels:
            if ziel.x <= self.x and ziel.x + ziel.width >= self.x:
               Abstandx=0
            elif self.x < ziel.x:
               Abstandx= ziel.x-(self.x + self.radius)
            elif self.x > ziel.x + ziel.width:
               Abstandx= self.x -self.radius - (ziel.x + ziel.width)

            if ziel.y <= self.y and ziel.y + ziel.height >= self.y:
               Abstandy = 0
            elif self.y < ziel.y:
               Abstandy = ziel.y-(self.y + self.radius)
            elif self.y > ziel.y + ziel.height:
               Abstandy = self.y -self.radius - (ziel.y + ziel.height)
               
            if Abstandx <= 0 and Abstandy <= 0:
                if Abstandx > Abstandy:
                    return(ziel, 'y')
                else:
                    return(ziel, 'x')
        
        return False


    def move(self):
        self.x += self.v.x
        if self.x > self.surface.get_width() or self.x < 0:
            sounds['wand'].play()
            self.v.x = -self.v.x
            

        self.y += self.v.y
        if self.y < 0:
            sounds['wand'].play()
            self.v.y = -self.v.y
            
        # Abprallen vom Schlaeger
        if self.y + self.radius > schlaeger.y and self.x > schlaeger.x and self.x < schlaeger.x + schlaeger.width:
            eWinkel = self.v.angle_to(Vector2(-1, 0))
            if eWinkel <180:
                print (eWinkel)
                sounds['wand'].play()
                ((self.x - schlaeger.x) / schlaeger.width) * 90
                abpWinkel = ((self.x - schlaeger.x) / schlaeger.width) * 90 - 45
                aWinkel = (2 * eWinkel + 2 * abpWinkel)
                if aWinkel < 210:
                    aWinkel = 210
                elif aWinkel > 330:
                    aWinkel = 330
                self.v.rotate_ip(aWinkel)
                self.y = schlaeger.y - self.radius

        # An Blocks abprallen
        getroffen = self.collidesWithZiel()
        if getroffen != False:
            if getroffen[1]=='x':
                self.v.x = -self.v.x
                if self.v.x < 0:
                    self.x = getroffen[0].x - self.radius
                elif self.v.x > 0:
                    self.x = getroffen[0].x + getroffen[0].width + self.radius
                sounds['block'].play()
                
            elif getroffen[1]=='y':
                self.v.y = -self.v.y
                if self.v.y < 0:
                    self.y = getroffen[0].y - self.radius
                elif self.v.y > 0:
                    self.y = getroffen[0].y + getroffen[0].height + self.radius
                sounds['block'].play()
                
            self.ziele.remove(getroffen[0])
      

    def moveTo(self, posx, posy):
        self.x = posx
        self.y = posy


class Schlaeger(object):
    def __init__(self, surface, posx=0, posy=0, width=0, height=0, v=0, color=(255,255,255)):
        self.surface = surface
        self.x = posx
        self.y = posy
        self.width = width
        self.height = height
        self.v = v              # Geschwindigkeit
        self.color = color

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.x < self.surface.get_width() - self.width and self.v > 0 or self.x > 0 and self.v < 0:
            self.x += self.v

class Ziel(object):
    def __init__(self, surface, posx=0, posy=0, height=10, width=50, color=(255, 255, 255)):
        self.surface = surface
        self.x = posx
        self.y = posy
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(self.surface, self.color, 
            (self.x, self.y, self.width, self.height ))





def quitGame():
    pygame.quit()
    sys.exit()


#
# Hauptprogramm
#
clock = pygame.time.Clock()
ziele = []
hasMusic = False

spiel = Spiel(windowWidth, windowHeight)

for line in range(3):
    for spalte in range(2):
        ziele.append(Ziel(spiel.screen, 80 + spalte * 70 * randint(1,3)**-1, 75 + line * 15 * randint (2,7)))
    
ball = Ball(spiel.screen, windowWidth / 8, windowHeight / 7, ballradius)
ball.v.x = 3
ball.v.y = 4

schlaeger = Schlaeger(spiel.screen, int((windowWidth - 200)/2), windowHeight - 20, 200, 7, 0, (255, 0, 0))
ball.setSchlaeger(schlaeger)
ball.setZiele(ziele)

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 40)
pygame.mixer.init()

try:
    pygame.mixer.music.load('Musik/Backgroundsound.mp3')
    hasMusic = True
except:
    hasMusic = False

if hasMusic:
    pygame.mixer.music.play(-1)
    
#print (schlaeger.width)

while ball.y < windowHeight and len(ball.ziele) > 0:
    clock.tick(60)          # Framerate 60 Bilder / Sekunde
    spiel.clearScreen()
    ball.move()
    ball.draw()
    schlaeger.move()
    schlaeger.draw()
    for ziel in ziele:
        ziel.draw()
    spiel.updateScreen()
    #ball.v.y += 0.05
    
    # Bearbeitung von zwischenzeitlich aufgetretenen Events
    # (Ereignissen) wie z.B. gedrückten Tasten
    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            elif event.key == pygame.K_LEFT:
                schlaeger.v = -10
            elif event.key == pygame.K_RIGHT:
                schlaeger.v = 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                schlaeger.v = 0

if hasMusic:
    pygame.mixer.music.pause()

if len(ball.ziele)>0:
    textsurface = myfont.render('Game over', False, (250, 100, 182))
    spiel.screen.blit(textsurface,(235,190))
    pygame.display.update()
    pygame.time.delay(1000)
    sounds['ball weg'].play()
    sounds['death'].play()

if len(ball.ziele)==0:
    textsurface = myfont.render('you win', False, (250, 100, 182))
    spiel.screen.blit(textsurface,(235,190))
    pygame.display.update()
    sounds['win'].play()    
    
time.sleep(7)
quitGame()
