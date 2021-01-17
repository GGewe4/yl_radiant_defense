import pygame
from game import Game


class MainMenu:
    def __init__(self, wind):
        self.width = 1280
        self.height = 720
        self.bgr = pygame.image.load("data/menu_test.png")
        self.bgr = pygame.transform.scale(self.bgr, (self.width, self.height))
        self.wind = wind

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game = Game(self.wind)
                        game.run()
                        del game
            self.draw()

        pygame.quit()

    def draw(self):
        self.wind.blit(self.bgr, (0, 0))
        pygame.display.update()