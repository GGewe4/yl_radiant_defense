import pygame
from main_menu import MainMenu

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((1280, 720))
    mainMenu = MainMenu(win)
    mainMenu.run()