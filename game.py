import pygame
import os


class Game:
    def __init__(self):
        self.width = 1100  # 1600 900, 16/9
        self.height = 620
        self.srf = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load(os.path.join("data", "background_test.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = []  # delete

    def run(self):
        run = True
        #clock = pygame.time.Clock()
        while run:
            #clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.clicks.clear()


            self.draw()

        pygame.quit()

    def draw(self):
        self.srf.blit(self.bg, (0, 0))
        for p in self.clicks:
            pygame.draw.circle(self.srf, (255, 0, 0), (p[0], p[1]), 5, 0)
        pygame.display.update()


pygame.init()
g = Game()
g.run()