import pygame

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Radiant Defense')
    from main_menu import MainMenu

    mainMenu = MainMenu(win)
    mainMenu.run()
