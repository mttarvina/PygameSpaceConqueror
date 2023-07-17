import pygame
import math


class MissileObject:

    idleSize = (27, 100)
    explodeSize = (150, 150)

    def __init__(self, _window, _windowSize, _index, _type):
        self.window = _window
        self.windowSize = _windowSize
        self.type = _type
        self.explodeTimer = 100
        self.explodeEvent = pygame.USEREVENT + 10 + _index
        self.fireFXCount = 10
        self.fireFXIndex = 0
        self.explodeFXCount = 9
        self.explodeFXIndex = 0
        self.active = False
        self.exploding = False
        self.loadImages()
        self.defineAttributes()


    def loadImages(self):
        self.imgFired = []
        for i in range(self.fireFXCount):
            img = pygame.image.load('./assets/missile/img/Missile_{}_Flying_00{}.png'.format(self.type, i)).convert_alpha()
            self.imgFired.append(pygame.transform.smoothscale(img, MissileObject.idleSize))

        self.imgExplode = []
        for i in range(self.explodeFXCount):
            img = pygame.image.load('./assets/missile/img/Missile_{}_Explosion_00{}.png'.format(self.type, i)).convert_alpha()
            self.imgExplode.append(pygame.transform.smoothscale(img, MissileObject.explodeSize))


    def defineAttributes(self):
        if self.type == 1:
            self.moveSpeed = 2
            self.explodeDamage = 1
        elif self.type == 2:
            self.moveSpeed = 3
            self.explodeDamage = 1
        elif self.type == 3:
            self.moveSpeed = 5
            self.explodeDamage = 1


    def fire(self, _playerLoc, _playerAngle):
        self.active = True
        self.exploding = False
        self.angle = _playerAngle
        self.location = [_playerLoc[0], _playerLoc[1]]


    def updateLoc(self):
        if self.active and not self.exploding:
            deltaX = self.moveSpeed * math.sin(math.radians(self.angle))        # the x-axis (0 degress) is vertical here in pygame
            deltaY = self.moveSpeed * math.cos(math.radians(self.angle))        # the y-axis (90 degress) is horizontal here in pygame
            self.location[0] = self.location[0] - deltaX
            self.location[1] = self.location[1] - deltaY
            if self.location[0] < 0 or self.location[0] > self.windowSize[0] or self.location[1] < 100 or self.location[1] > self.windowSize[1]-100:
                self.deactivate()


    def explode(self):
        if self.active:
            self.exploding = True
            pygame.time.set_timer(self.explodeEvent , self.explodeTimer)        # start the explode timer here


    def deactivate(self):
        self.active = False
        self.exploding = False
        pygame.time.set_timer(self.explodeEvent, 0)                             # disable explode event timer


    def render(self):
        if self.active:
            if self.exploding:
                if self.explodeFXIndex >= self.explodeFXCount:
                    self.explodeFXIndex = 0
                self.image = self.imgExplode[self.explodeFXIndex]
                self.explodeFXIndex += 1
            else:
                if self.fireFXIndex >= self.fireFXCount:
                    self.fireFXIndex = 0
                self.image = self.imgFired[self.fireFXIndex]
                self.fireFXIndex += 1
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center=(self.location[0], self.location[1]))
            self.window.blit(self.image, self.rect)