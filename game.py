import pygame
from audio import GMusic
from enemies.minotaur import Minotaur
from enemies.golem import Golem
from enemies.wraith import Wraith
from enemies.satyr import Satyr
from enemies.enemy import all_sprites
import os

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
        self.circ = []
        with open(os.path.join(f'levels/level{1}/path.txt')) as file:
            self.circ = eval(''.join(file.readlines()))
        self.enemies = [Golem(), Wraith()]

        self.mus = GMusic()
        self.mus.play_m('gelik')

    def run(self):
        run = True
        clock = pygame.time.Clock()
        self.c = 0
        while run:
            self.c += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.clicks.clear()
                        if self.mus.is_paused:
                            self.mus.unpause_m()
                        else:
                            self.mus.pause_m()
                    elif event.key == pygame.K_g:
                        self.mus.play_m('gelik')
                    elif event.key == pygame.K_m:
                        self.mus.play_m('zihte')
            self.draw()
            clock.tick(120)
        pygame.quit()
        print(self.clicks)

    def draw(self):
        self.wind.blit(self.backg, (0, 0))
        for p in self.clicks:
            pygame.draw.circle(self.wind, (255, 0, 0), (p[0], p[1]), 5, 0)
        for em in self.enemies:
            em.new_move(self.wind)
        all_sprites.draw(self.wind)
        if self.c % 6 == 0:
            all_sprites.update()
        pygame.display.update()


pygame.init()
g = Game()
g.run()
