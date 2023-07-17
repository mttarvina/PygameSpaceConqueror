import pygame
import math


class PlayerObject:
    size = (75, 75)

    def __init__(self, _window, _windowSize, _type):
        self.window = _window
        self.windowSize = _windowSize
        self.type = _type
        self.location = [0.5*_windowSize[0], 0.5*_windowSize[1]]
        self.angle = 0
        self.score = 0
        self.loadImages()
        self.defineAttributes()
        self.maxLifePoints = self.lifePoints


    def loadImages(self):
        img = pygame.image.load('./assets/player/img/spaceShips_00{}.png'.format(self.type)).convert_alpha()
        self.imgRef = pygame.transform.smoothscale(img, PlayerObject.size)
        self.image = self.imgRef.copy()
        self.rect = self.image.get_rect(center=(self.location[0], self.location[1]))
        self.maxSizeDimension = max(PlayerObject.size)


    def defineAttributes(self):
        if self.type == 1:
            self.moveSpeed = 3
            self.angularSpeed = 1.5
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 2
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 2:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 3:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 4:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 5:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 6:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 7:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 8:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5
        elif self.type == 9:
            self.moveSpeed = 5
            self.angularSpeed = 2
            self.lifePoints = 1000
            self.bombType = 3
            self.maxBombs = 5
            self.missileType = 1
            self.maxMissiles = 5


    def takeDamage(self, damage):
        self.lifePoints -= damage


    def regenerate(self, hpVal):
        self.lifePoints += hpVal
        if self.lifePoints > self.maxLifePoints:
            self.lifePoints = self.maxLifePoints


    def updateScore(self, awardPoints):
        self.score += awardPoints


    def turn(self, _rotateDir):
        if _rotateDir == '<':
            self.angle += self.angularSpeed
        elif _rotateDir == '>':
            self.angle -= self.angularSpeed
        if self.angle > 360:
            self.angle = self.angle - 360 
        self.image = pygame.transform.rotate(self.imgRef, self.angle)


    def move(self, _heaveDir):
        if _heaveDir == '+':
            angleTemp = self.angle
        elif _heaveDir == '-':
            if self.angle < 180:
                angleTemp = 180 + self.angle
            else:
                angleTemp = self.angle - 180
        deltaX = self.moveSpeed * math.sin(math.radians(angleTemp))                # the x-axis (0 degress) is vertical here in pygame
        deltaY = self.moveSpeed * math.cos(math.radians(angleTemp))                # the y-axis (90 degress) is horizontal here in pygame
        self.location[0] = self.location[0] - deltaX
        self.location[1] = self.location[1] - deltaY

        if self.location[0] <= self.maxSizeDimension*0.5: 
            self.location[0] = self.maxSizeDimension*0.5
        if self.location[0] >= self.windowSize[0] - (self.maxSizeDimension*0.5):
            self.location[0] = self.windowSize[0] - (self.maxSizeDimension*0.5)
        if self.location[1] <= 100 + (0.5*self.maxSizeDimension): 
            self.location[1] = 100 + (0.5*self.maxSizeDimension)
        if self.location[1] >= self.windowSize[1] - (0.5*self.maxSizeDimension+100):
            self.location[1] = self.windowSize[1] - (0.5*self.maxSizeDimension+100)


    def render(self):
        self.rect = self.image.get_rect(center=(self.location[0], self.location[1]))
        self.window.blit(self.image, self.rect)