import pygame
import math
import random


class MeteorObject:
    def __init__(self, _window, _windowSize, _numberOfTypes):
        self.window = _window
        self.windowSize = _windowSize
        self.type = random.randint(1, _numberOfTypes)
        self.dir = random.choice(['L', 'R', 'T', 'B'])
        self.angle = 0
        self.active = False
        self.loadImages()
        self.defineAttributes()


    def loadImages(self):
        img = pygame.image.load('./assets/meteor/img/Meteor_0{}.png'.format(self.type)).convert_alpha()
        rect = img.get_rect()
        minDimension = min(rect.size)
        scalefactor = minDimension/30
        self.imgRef = pygame.transform.smoothscale(img, (int(rect.size[0]/scalefactor), int(rect.size[1]/scalefactor)))
        self.image = self.imgRef.copy()
        self.rect = self.image.get_rect()
        self.maxSizeDimension = max(self.rect.size)


    def defineAttributes(self):
        if self.type == 1:
            self.moveSpeed = 0.5
            self.angularSpeed = 1
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 2:
            self.moveSpeed = 0.5
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 3:
            self.moveSpeed = 1
            self.angularSpeed = 2
            self.valuePoint = 2
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 4:
            self.moveSpeed = 2
            self.angularSpeed = 1
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 5:
            self.moveSpeed = 2
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 6:
            self.moveSpeed = 2
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 7:
            self.moveSpeed = 2
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 8:
            self.moveSpeed = 2
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 9:
            self.moveSpeed = 2
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
        elif self.type == 10:
            self.moveSpeed = 2
            self.angularSpeed = 2
            self.valuePoint = 1
            self.hpGrant = 5
            self.collisionDamage = 0.5
    

    def defineStartPoint(self):
        if self.dir == 'L':
            self.location = [self.windowSize[0], random.randint(125, self.windowSize[1]-125)]
        elif self.dir == 'R':
            self.location = [0, random.randint(125, self.windowSize[1]-125)]
        elif self.dir == 'T':
            self.location = [random.randint(25, self.windowSize[0]-25), self.windowSize[1]-100]
        elif self.dir == 'B':
            self.location = [random.randint(25, self.windowSize[0]-25), 100]


    def spawn(self):
        self.active = True
        self.dir = random.choice(['L', 'R', 'T', 'B'])
        self.defineStartPoint()


    def updateLoc(self):
        if self.active:
            # rotate the image first
            self.angle += self.angularSpeed
            if self.angle > 360:
                self.angle = self.angle - 360 
            self.image = pygame.transform.rotate(self.imgRef, self.angle)

            # move object
            if self.dir == 'L':
                self.location[0] -= self.moveSpeed
            elif self.dir == 'R':
                self.location[0] += self.moveSpeed
            if self.dir == 'T':
                self.location[1] -= self.moveSpeed
            elif self.dir == 'B':
                self.location[1] += self.moveSpeed

            # check if outside of playarea
            if self.location[0] < 0 or self.location[0] > self.windowSize[0] or self.location[1] < 100 or self.location[1] > self.windowSize[1]-100:
                self.deactivate()


    def deactivate(self):
        self.active = False


    def render(self):
        if self.active:
            self.rect = self.image.get_rect(center=(self.location[0], self.location[1]))
            self.window.blit(self.image, self.rect)