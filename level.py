import pygame


class levelObject:
    def __init__(self, _levelNum):
        self.levelNum = _levelNum
        self.defineLevelParameters()
    
    def defineLevelParameters(self):
        if self.levelNum == 1:
            self.maxNumberOfMeteor = 8
            self.typesOfMeteor = 3
            self.meteorSpawnTimeRange = (5, 10)
            self.maxNumberOfEnemy = 5
            self.typesOfEnemy = 3
            self.enemySpawnTimeRange = (3, 8)