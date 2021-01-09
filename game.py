import pygame
import os


#  [(856, 19), (820, 131), (670, 153), (439, 157), (342, 209),
#  (302, 266), (336, 321), (380, 389), (360, 455),
#  (403, 505), (471, 528), (557, 522), (619, 570), (634, 702)]

class Game:
    def __init__(self):
        self.width = 1280  # 1600 900, 16/9
        self.height = 720
        self.wind = pygame.display.set_mode((self.width, self.height))
        self.backg = pygame.image.load(os.path.join("data", "bg_test5.png"))
        self.backg = pygame.transform.scale(self.backg, (self.width, self.height))
        self.clicks = []  # delete
        pygame.mixer.music.load('data/music_test2.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)

    def run(self):
        run = True
        mpause = False
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
