import pygame


class BombObject:
    idleSize = (60, 40)
    explodeSize = (200, 200)

    def __init__(self, _window, _index, _type):
        self.window = _window
        self.type = _type
        self.event = pygame.USEREVENT + _index
        self.idleAnimationCount = 10
        self.idleAnimationIndex = 0
        self.explodeAnimationCount = 9
        self.explodeAnimationIndex = 0
        self.active = False
        self.exploding = False
        self.loadImages()
        self.defineAttributes()


    def loadImages(self):
        self.imgDropped = []
        for i in range(self.idleAnimationCount):
            img = pygame.image.load('./assets/bomb/img/Bomb_{}_Idle_00{}.png'.format(self.type, i)).convert_alpha()
            self.imgDropped.append(pygame.transform.smoothscale(img, BombObject.idleSize))
        
        self.imgExplode = []
        for i in range(self.explodeAnimationCount):
            img = pygame.image.load('./assets/bomb/img/Bomb_{}_Explosion_00{}.png'.format(self.type, i)).convert_alpha()
            self.imgExplode.append(pygame.transform.smoothscale(img, BombObject.explodeSize))


    def defineAttributes(self):
        if self.type == 1:
            self.dropTimer = 2000
            self.explodeTimer = 500
            self.explodeDamage = 1
        elif self.type == 2:
            self.dropTimer = 2000
            self.explodeTimer = 500
            self.explodeDamage = 1
        elif self.type == 3:
            self.dropTimer = 2000
            self.explodeTimer = 500
            self.explodeDamage = 1


    def drop(self, _droppedLoc):
        self.active = True
        self.exploding = False
        self.location = (_droppedLoc[0], _droppedLoc[1])
        pygame.time.set_timer(self.event , self.dropTimer)                      # start the dropped timer here


    def updateStat(self):
        if self.active and not self.exploding:                                  # bomb will explode
            self.exploding = True
            pygame.time.set_timer(self.event, 0)
            pygame.time.set_timer(self.event, self.explodeTimer)                # start the explode timer here
            return
        if self.active and self.exploding:                                      # deactivate
            self.active = False
            self.exploding = False
            pygame.time.set_timer(self.event , 0)                               # disable timer event
            return


    def deactivate(self):
        self.active = False
        self.exploding = False
        pygame.time.set_timer(self.event , 0)                                   # disable timer event


    def render(self):
        if self.active:
            if self.exploding:
                if self.explodeAnimationIndex >= self.explodeAnimationCount:
                    self.explodeAnimationIndex = 0
                self.image = self.imgExplode[self.explodeAnimationIndex]
                self.explodeAnimationIndex += 1
            else:
                if self.idleAnimationIndex >= self.idleAnimationCount:
                    self.idleAnimationIndex = 0
                self.image = self.imgDropped[self.idleAnimationIndex]
                self.idleAnimationIndex += 1
            self.rect = self.image.get_rect(center=self.location)
            self.window.blit(self.image, self.rect)