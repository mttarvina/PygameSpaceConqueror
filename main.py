import pygame, sys
from menu import StartMenuObject


if __name__ == "__main__":
    pygame.init()

    # constants
    gameFPS = 60
    gameClock = pygame.time.Clock()
    screenSize = (1600, 900)

    # title and icon
    pygame.display.set_caption('Space Conqueror by Tarvs Hobbytronics')
    icon = pygame.image.load('logo.ico')
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode(screenSize)
    startMenu = StartMenuObject(screen, screenSize, gameClock, gameFPS)
    startMenu.run()
    