import pygame
from audio import GMusic

#  [(856, 19), (820, 131), (670, 153), (439, 157), (342, 209),
#  (302, 266), (336, 321), (380, 389), (360, 455),
#  (403, 505), (471, 528), (557, 522), (619, 570), (634, 702)]


class Game:
    def __init__(self):
        self.width = 1280  # 1600 900, 16/9
        self.height = 720
        self.wind = pygame.display.set_mode((self.width, self.height))
        self.backg = pygame.image.load("data/bg_test5.png")
        self.backg = pygame.transform.scale(self.backg, (self.width, self.height))
        self.clicks = []  # delete

        self.ad = GMusic()
        self.ad.play_m('gelik')

    def run(self):        
        run = True
        # clock = pygame.time.Clock()
        while run:
            # clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.clicks.clear()
                        if self.ad.is_paused:
                            self.ad.unpause_m()
                        else:
                            self.ad.pause_m()
                    elif event.key == pygame.K_g:
                        self.ad.play_m('gelik')
                    elif event.key == pygame.K_m:
                        self.ad.play_m('zihte')

            self.draw()

        pygame.quit()

    def draw(self):
        self.wind.blit(self.backg, (0, 0))
        for p in self.clicks:
            pygame.draw.circle(self.wind, (255, 0, 0), (p[0], p[1]), 5, 0)
        pygame.display.update()


pygame.init()
g = Game()
g.run()
