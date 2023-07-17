import pygame, sys
from level import levelObject
from elements_src.player import PlayerObject
from elements_src.bomb import BombObject
from elements_src.missile import MissileObject
from elements_src.meteor import MeteorObject
import random


class GameObject:
    def __init__(self, _window, _windowSize, _gameClk, _fps):
        """Initialize default GameObject parameters

        Args:
            _window (surface): Main screen surface
            _windowSize (tuple): (x, y) -> Main screen default size
            _gameClk (clock): Pygame clock object
            _fps (int): Default screen refresh value
        """
        self.window = _window
        self.windowSize = _windowSize
        self.gameClk = _gameClk
        self.fps = _fps
        self.active = False


    def run(self, _levelNum, _playerType):

        self.active = True
        self.timerSeconds = 0
        self.timerMinutes = 3
        self.pause = False
        self.gameOver = False

        self.gameLevel = levelObject(_levelNum)

        self.loadGUIElements()
        self.loadGameElements(_playerType)
        heaveMotion = None
        rotateMotion = None
        bombDropped = False
        bombChangedStat = False
        bombToUpdate = 0
        missileFired = False
        missileExpired = False
        missileToRemove = []
        spawnMeteor = False

        gameTimerTick = False
        pygame.time.set_timer(self.meteorSpawnEvent , self.meteorSpawnTimer*1000)        
        pygame.time.set_timer(self.gameTimerEvent , 1000)
        
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and not bombDropped:
                        bombDropped = True
                    if event.key == pygame.K_LSHIFT and not missileFired:
                        missileFired = True
                    if event.key == pygame.K_UP:
                        heaveMotion = '+'
                    if event.key == pygame.K_RIGHT:
                        rotateMotion = '>'
                    if event.key == pygame.K_LEFT:
                        rotateMotion = '<'
                    if event.key == pygame.K_DOWN:
                        heaveMotion = '-'
                    if event.key == pygame.K_ESCAPE:
                        self.active = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        heaveMotion = ''
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        rotateMotion = ''
                for i in range(self.player.maxBombs):
                    if event.type == pygame.USEREVENT + i:
                        bombChangedStat = True
                        bombToUpdate = i
                        break
                for i in range(self.player.maxMissiles):
                    if event.type == pygame.USEREVENT + 10 + i:
                        missileExpired = True
                        missileToRemove.append(i)
                if event.type == self.meteorSpawnEvent:
                    spawnMeteor = True
                if event.type == self.gameTimerEvent:
                    gameTimerTick = True

            self.renderGUIElements()

            if gameTimerTick:
                self.updateGameTimer()
                gameTimerTick = False

            if not self.gameOver:
                if spawnMeteor:
                    self.spawnMeteors()
                    spawnMeteor = False
                if bombChangedStat:
                    self.bombs[bombToUpdate].updateStat()
                    bombChangedStat = False
                if bombDropped:
                    self.dropABomb()
                    bombDropped = False
                if missileExpired:
                    for i in missileToRemove:
                        self.missiles[i].deactivate()
                    missileToRemove.clear()
                    missileExpired = False
                if missileFired:
                    self.fireAMissile()
                    missileFired = False

                self.trackAllMissiles()
                self.trackAllMeteors()
                if heaveMotion:
                    self.movePlayer(heaveMotion)
                if rotateMotion:
                    self.movePlayer(rotateMotion)

                self.renderAllMeteors()
                self.renderAllBombs()
                self.renderAllMissiles()
                self.player.render()

                self.checkMeteorToBombCollision()
                self.checkMeteorToMissileCollision()
                self.checkPlayerToMeteorCollision()
                self.checkPlayerToExplosionCollision()

            self.renderFPS()
            self.renderLevelInfo()
            self.renderGameTimer()
            self.renderPlayerHPBar()
            self.renderPlayerScore()

            if self.gameOver:
                self.renderGameOverScreen()

            pygame.display.update()
            if self.pause or self.gameOver:
                self.gameClk.tick(int(0.25*self.fps))
            else:
                self.gameClk.tick(self.fps)

        self.deactivateElements()        


    def loadGameElements(self, _playerType):
        self.player = PlayerObject(self.window, self.windowSize, _playerType)
        self.bombs = []
        for index in range(self.player.maxBombs):
            self.bombs.append(BombObject(self.window, index, self.player.bombType))
        self.bombIndex = 0
        self.missiles = []
        for index in range(self.player.maxMissiles):
            self.missiles.append(MissileObject(self.window, self.windowSize, index, self.player.missileType))
        self.meteors = []
        for index in range(self.gameLevel.maxNumberOfMeteor):
            self.meteors.append(MeteorObject(self.window, self.windowSize, self.gameLevel.typesOfMeteor))
        self.meteorsToSpawn = 1                                                 # default number of meteors to spawn at first time
        self.meteorSpawnTimer = 5                                               # default spawn timer for first meteor spawn
        self.meteorSpawnEvent = pygame.USEREVENT + 21
        self.gameTimerEvent = pygame.USEREVENT + 22


    def updateGameTimer(self):
        if not self.gameOver:
            if self.timerSeconds <= 0:
                self.timerMinutes -= 1
                self.timerSeconds = 60
            self.timerSeconds -= 1
            if self.timerMinutes == 0 and self.timerSeconds == 0:
                self.gameOver = True


    def movePlayer(self, _playerMotion):
        """Moves the player according to button press

        Args:
            _playerMotion (char): indicates player movement based on pressed button
        """
        if _playerMotion == '+' or _playerMotion == '-':
            self.player.move(_playerMotion)
        if _playerMotion == '<' or _playerMotion == '>':
            self.player.turn(_playerMotion)
    

    def dropABomb(self):
        """Activates a bomb, specifies drop location, start bomb timer
        """
        if not self.bombs[self.bombIndex].active:
            self.bombs[self.bombIndex].drop(self.player.location)
            self.bombIndex += 1                                              
        if self.bombIndex >= self.player.maxBombs:
            self.bombIndex = 0


    def fireAMissile(self):
        """Activates a missile, specify starting location
        """
        for index in range(self.player.maxMissiles):
            if not self.missiles[index].active:
                self.missiles[index].fire(self.player.location, self.player.angle)
                break                                   


    def renderAllBombs(self):
        """Render all active bombs in the play area
        """
        for bomb in self.bombs:
            bomb.render()


    def trackAllMissiles(self):
        """Update the location of all active missiles in the play area
        """
        for missile in self.missiles:
            missile.updateLoc()        


    def renderAllMissiles(self):
        """Render all active missiles in the play area
        """
        for missile in self.missiles:
            missile.render()


    def spawnMeteors(self):
        """Spawn a random number of meteors from random locations in the play area
        """
        for i in range(self.meteorsToSpawn):
            for index in range(self.gameLevel.maxNumberOfMeteor):
                if not self.meteors[index].active:
                    self.meteors[index].spawn()
                    break
        self.meteorsToSpawn = random.randint(1, self.gameLevel.maxNumberOfMeteor)
        self.meteorSpawnTimer = random.randint(self.gameLevel.meteorSpawnTimeRange[0], self.gameLevel.meteorSpawnTimeRange[1])
        pygame.time.set_timer(self.meteorSpawnEvent , self.meteorSpawnTimer*1000)    


    def trackAllMeteors(self):
        """Update the location of all active meteors in the play area
        """
        for meteor in self.meteors:
            meteor.updateLoc()

    
    def renderAllMeteors(self):
        """Render all active meteors in the play area
        """
        for meteor in self.meteors:
            meteor.render()
    

    def checkMeteorToBombCollision(self):
        """Check if an active meteor collides with an active bomb in the play area
        """
        for bomb in self.bombs:
            for meteor in self.meteors:
                if bomb.exploding and meteor.active:
                    if bomb.rect.collidepoint(meteor.location):
                        meteor.deactivate()
                        self.player.regenerate(meteor.hpGrant)
                        self.player.updateScore(meteor.valuePoint)


    def checkMeteorToMissileCollision(self):
        """Check if an active meateor collides with an active missile in the play area
        """
        for missile in self.missiles:
            for meteor in self.meteors:
                if missile.active and meteor.active:
                    if missile.rect.collidepoint(meteor.location):
                        meteor.deactivate()
                        missile.explode()
                        self.player.regenerate(meteor.hpGrant)
                        self.player.updateScore(meteor.valuePoint)


    def checkPlayerToMeteorCollision(self):
        for meteor in self.meteors:
            if meteor.active:
                if meteor.rect.colliderect(self.player.rect):
                    self.player.takeDamage(meteor.collisionDamage)
        if self.player.lifePoints <= 0:
            self.gameOver = True


    def checkPlayerToExplosionCollision(self):
        for bomb in self.bombs:
            if bomb.exploding:
                if bomb.rect.collidepoint(self.player.location):
                    self.player.takeDamage(bomb.explodeDamage) 
        for missile in self.missiles:
            if missile.exploding:
                if missile.rect.collidepoint(self.player.location):
                    self.player.takeDamage(missile.explodeDamage) 
        if self.player.lifePoints <= 0:
            self.gameOver = True


    def deactivateElements(self):
        """Deactivate all meteor/missile/bomb objects. Clear lists
        """
        pygame.time.set_timer(self.meteorSpawnEvent, 0)
        for meteor in self.meteors:
            meteor.deactivate()
        self.meteors.clear()
        for bomb in self.bombs:
            bomb.deactivate()
        self.bombs.clear()
        self.bombIndex = 0
        for missile in self.missiles:
            missile.deactivate()
        self.missiles.clear()


    def renderGameTimer(self):
        strBuf = ''
        if self.timerMinutes < 10:
            strBuf = strBuf + '0' + '{}'.format(self.timerMinutes)
        else:
            strBuf = strBuf + '{}'.format(self.timerMinutes)
        strBuf = strBuf + ':'
        if self.timerSeconds < 10:
            strBuf = strBuf + '0' + '{}'.format(self.timerSeconds)
        else:
            strBuf = strBuf + '{}'.format(self.timerSeconds)
        timerText = self.timerFont.render(strBuf, True, (0, 0, 0))
        self.window.blit(timerText, (700, 20))


    def renderFPS(self):
        fpsFont = pygame.font.Font(self.fontPath, 20)  
        fpsText = fpsFont.render('FPS: {}'.format(int(self.gameClk.get_fps())), True, (0, 0, 0))
        self.window.blit(fpsText, (self.windowSize[0]-125, self.windowSize[1]-125))


    def renderLevelInfo(self):
        levelFont = pygame.font.Font(self.fontPath, 64)
        levelText = levelFont.render('Level: {}'.format(self.gameLevel.levelNum), True, (0, 0, 0))
        self.window.blit(levelText, (50, 20))


    def renderPlayerScore(self):
        scoreText = self.scoreFont.render('Score: {}'.format(self.player.score), True, (0, 0, 0))
        self.window.blit(scoreText, (1275, self.windowSize[1]-62.5))


    def renderPlayerHPBar(self):
        """Render HP bar at the leftmost bottom box with text overlay
        """
        if not self.gameOver:
            if 0.75*self.player.maxLifePoints < self.player.lifePoints <= self.player.maxLifePoints:
                color = (0, 255, 0)
            elif 0.5*self.player.maxLifePoints < self.player.lifePoints <= 0.75*self.player.maxLifePoints:
                color = (255, 255, 0)
            elif 0.25*self.player.maxLifePoints < self.player.lifePoints <= 0.5*self.player.maxLifePoints:
                color = (255, 165, 0)
            else:
                color = (255, 0, 0)
            lineLength = self.player.lifePoints*300/1000
            pygame.draw.line(self.window, color, (49, self.windowSize[1]-45), (49+lineLength, self.windowSize[1]-45), width=60)
        hpText = self.hpFont.render('HP: {}'.format(self.player.lifePoints), True, (0, 0, 0))
        self.window.blit(hpText, (100, self.windowSize[1]-62.5))


    def renderGUIElements(self):
        """Render GUI elements
        """
        self.window.fill((255, 255, 255))
        self.bgImage.set_alpha(150)
        self.window.blit(self.bgImage, self.bgRect)
        self.window.blit(self.exitButtonImg, self.exitButtonRect)
        self.window.blit(self.infoButtonImg, self.infoButtonRect)
        self.window.blit(self.settingsButtonImg, self.settingsButtonRect)
        self.window.blit(self.pauseButtonImg, self.pauseButtonRect)
        self.window.blit(self.playButtonImg, self.playButtonRect)
        for i in range(5):
            self.window.blit(self.botBoxImg, self.botBoxRect[i])
        pygame.draw.line(self.window, (0, 0, 0), (0, 100), (self.windowSize[0], 100), width=2)
        pygame.draw.line(self.window, (0, 0, 0), (0, self.windowSize[1]-100), (self.windowSize[0], self.windowSize[1]-100), width=2)


    def renderGameOverScreen(self):
        self.window.blit(self.gameOverText, (550, 250))
        self.window.blit(self.replayButtonImg, self.replayButtonRect)


    def loadGUIElements(self):
        """Load all elements of the GUI
        """
        self.fontPath = './assets/font/zorque.ttf'
        self.timerFont = pygame.font.Font(self.fontPath, 64)
        self.scoreFont = pygame.font.Font(self.fontPath, 32)
        self.hpFont = pygame.font.Font(self.fontPath, 32)
        
        # --- background
        img = pygame.image.load('./assets/gui/img/background.png').convert_alpha()
        self.bgImage = pygame.transform.smoothscale(img, self.windowSize)
        self.bgRect = self.bgImage.get_rect(center=(0.5*self.windowSize[0], 0.5*self.windowSize[1]))

        buttonSize = (80, 80)
        # --- exit button
        img = pygame.image.load('./assets/gui/img/BTNs/Close_BTN.png').convert_alpha()
        self.exitButtonImg = pygame.transform.smoothscale(img, buttonSize)
        self.exitButtonRect = self.exitButtonImg.get_rect(center=(self.windowSize[0]-(1*0.5*buttonSize[0]), 0.5*buttonSize[1]+10))
        # --- info button
        img = pygame.image.load('./assets/gui/img/BTNs/Info_BTN.png').convert_alpha()
        self.infoButtonImg = pygame.transform.smoothscale(img, buttonSize)
        self.infoButtonRect = self.infoButtonImg.get_rect(center=(self.windowSize[0]-(3*0.5*buttonSize[0]), 0.5*buttonSize[1]+10))
        # --- settings button
        img = pygame.image.load('./assets/gui/img/BTNs/Settings_BTN.png').convert_alpha()
        self.settingsButtonImg = pygame.transform.smoothscale(img, buttonSize)
        self.settingsButtonRect = self.settingsButtonImg.get_rect(center=(self.windowSize[0]-(5*0.5*buttonSize[0]), 0.5*buttonSize[1]+10))
        # --- pause button
        img = pygame.image.load('./assets/gui/img/BTNs/Pause_BTN.png').convert_alpha()
        self.pauseButtonImg = pygame.transform.smoothscale(img, buttonSize)
        self.pauseButtonRect = self.pauseButtonImg.get_rect(center=(self.windowSize[0]-(7*0.5*buttonSize[0]), 0.5*buttonSize[1]+10))
        # --- play button
        img = pygame.image.load('./assets/gui/img/BTNs/Play_BTN.png').convert_alpha()
        self.playButtonImg = pygame.transform.smoothscale(img, buttonSize)
        self.playButtonRect = self.playButtonImg.get_rect(center=(self.windowSize[0]-(9*0.5*buttonSize[0]), 0.5*buttonSize[1]+10))

        boxSize = (350, 80)
        img = pygame.image.load('./assets/gui/img/Level_Menu/Table.png').convert_alpha()
        self.botBoxImg = pygame.transform.smoothscale(img, boxSize)
        self.botBoxImg.set_alpha(200)
        self.botBoxRect = []
        for i in range(5):
            self.botBoxRect.append(self.botBoxImg.get_rect(center=(((2*i)-1)*0.125*self.windowSize[0], self.windowSize[1]-(0.5*boxSize[1]))))

        self.gameOverFont = pygame.font.Font(self.fontPath, 84)
        self.gameOverText = self.gameOverFont.render('GAME OVER', True, (0, 0, 0))
        
        # --- replaybutton
        img = pygame.image.load('./assets/gui/img/BTNs/Replay_BTN.png').convert_alpha()
        self.replayButtonImg = pygame.transform.smoothscale(img, (200, 200))
        self.replayButtonRect = self.replayButtonImg.get_rect(center=(0.5*self.windowSize[0], 600))
