import pygame, sys
from game import GameObject


class StartMenuObject:
    def __init__(self, _window, _windowSize, _gameClk, _fps):
        self.window = _window
        self.windowSize = _windowSize
        self.gameClk = _gameClk
        self.fps = _fps
        self.active = False
            
    def run(self):
        self.active = True
        self.importElements()
        mousePressed = False
        startButtonClicked = False
        exitButtonClicked = False

        game = GameObject(self.window, self.windowSize, self.gameClk, self.fps)

        while self.active:
            self.mouseLoc = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseClick = pygame.mouse.get_pressed()
                    mousePressed = True
            
            if mousePressed and mouseClick[0]:
                exitButtonClicked = self.checkButtonToMouseCollision('exit')
                startButtonClicked = self.checkButtonToMouseCollision('start')
                mousePressed = False
            if exitButtonClicked:
                exitButtonClicked = False
                self.active = False
            if startButtonClicked:
                startButtonClicked = False        
                game.run(1, 1)
                del game
            
            self.renderUI()
            pygame.display.update()
            self.gameClk.tick(int(0.25*self.fps))
        sys.exit()

    def checkButtonToMouseCollision(self, _buttonToCheck):
        if _buttonToCheck == 'start':
            if self.startButtonRect.collidepoint(self.mouseLoc):
                return True
        elif _buttonToCheck == 'exit':
            if self.exitButtonRect.collidepoint(self.mouseLoc):
                return True
        return False
    
    def renderUI(self):
        self.window.blit(self.bgImage, self.bgRect)
        # pygame.draw.line(self.window, (0,0,0), (0.5*self.windowSize[0], 0), (0.5*self.windowSize[0], self.windowSize[1]), width=2)
        self.window.blit(self.titleText, (400, 200))
        self.window.blit(self.descText, (500, 300))
        self.window.blit(self.authorText, (670, 400))
        self.window.blit(self.startButton, self.startButtonRect)
        self.window.blit(self.exitButton, self.exitButtonRect)

    def importElements(self):
        # --- background
        img = pygame.image.load('./assets/gui/img/background.png').convert_alpha()
        self.bgImage = pygame.transform.smoothscale(img, self.windowSize)
        self.bgRect = self.bgImage.get_rect(center=(0.5*self.windowSize[0], 0.5*self.windowSize[1]))
        # --- text
        fontPath = './assets/font/zorque.ttf'
        titleFont = pygame.font.Font(fontPath, 84)
        self.titleText = titleFont.render('SPACE CONQUEROR', True, (0, 0, 0))
        descFont = pygame.font.Font(fontPath, 36)
        self.descText = descFont.render('[Sample Project Using Pygame]', True, (0, 0, 0))
        authorFont = pygame.font.Font(fontPath, 24)
        self.authorText = authorFont.render('by Tarvs\' Hobbytronics', True, (0, 0, 0))
        # --- playbutton
        img = pygame.image.load('./assets/gui/img/Main_Menu/Start_BTN.png').convert_alpha()
        self.startButton = pygame.transform.smoothscale(img, (300, 90))
        self.startButtonRect = self.startButton.get_rect(center=(0.5*self.windowSize[0], 600))
        # --- exit button
        img = pygame.image.load('./assets/gui/img/Main_Menu/Exit_BTN.png').convert_alpha()
        self.exitButton = pygame.transform.smoothscale(img, (300, 90))
        self.exitButtonRect = self.exitButton.get_rect(center=(0.5*self.windowSize[0], 700))