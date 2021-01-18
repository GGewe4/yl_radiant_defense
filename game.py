import sys

import pygame
import time
import random
from audio import GMusic
# from enemies.minotaur import Minotaur
# from enemies.golem import Golem
# from enemies.wraith import Wraith
# from enemies.satyr import Satyr
from towers.tower import towers_sprites
from towers.magic_tower import MagicTower
from enemies.enemy import enemies_sprites
from enemies.groupe_enemies import NEW_ENEMY, Group, NEW_WAVE
from towers.archer_tower import ArcherTower
import os

#  [(856, 19), (820, 131), (670, 153), (439, 157), (342, 209),
#  (302, 266), (336, 321), (380, 389), (360, 455),
#  (403, 505), (471, 528), (557, 522), (619, 570), (634, 702)]

waves = [
    [0, 5, 3500],
    [1, 3, 4000],
    [2, 3, 2000],
    [0, 2, 3000]]


# [0, 50, 0, 1],
# [0, 100, 0],
# [20, 100, 0],
# [50, 100, 0],
# [100, 100, 0],
# [0, 0, 50, 3],
# [20, 0, 100],
# [20, 0, 150],
# [200, 100, 200],


class Game:
    def __init__(self, wind):
        self.wind = wind
        self.width = 1280  # 1600 900, 16/9
        self.height = 720
        self.backg = pygame.image.load("data/bg_test5.png")
        self.backg = pygame.transform.scale(self.backg, (self.width, self.height))
        self.clicks = []  # delete
        self.circ = []
        with open(os.path.join(f'levels/level{1}/path.txt')) as file:
            self.circ = eval(''.join(file.readlines()))
        self.enemies = []
        self.towers = []
        self.c = 0  # animation count

        self.mus = GMusic()
        self.mus.play_m('gelik')

        self.wave = 0
        self.current_wave = waves[self.wave][:]

    def run(self):
        run = True
        clock = pygame.time.Clock()
        group = Group(*self.current_wave)
        while run:
            self.c += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.towers.append(ArcherTower(*pos))
                        self.clicks.append(pos)
                    elif event.button == 3:
                        self.towers.append(MagicTower(*pos))
                        self.clicks.append(pos)

                if event.type == NEW_ENEMY:
                    group.update(self.enemies)

                if event.type == NEW_WAVE:
                    self.wave += 1
                    if self.wave < len(waves):
                        self.current_wave = waves[self.wave][:]
                        group = Group(*self.current_wave)

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
        print(self.clicks)

    def draw(self):
        self.wind.blit(self.backg, (0, 0))
        enemies_sprites.draw(self.wind)
        if self.c % 6 == 0:
            enemies_sprites.update()
        if self.c % 8 == 0:
            towers_sprites.update(self.enemies)
        for t in self.towers:
            t.draw_radius(self.wind)
            t.attack(self.enemies)
        towers_sprites.draw(self.wind)
        for em in self.enemies:
            # pygame.draw.circle(self.wind, (0, 255, 0), (em.hit_box.x + em.hit_box.width // 2,
            # em.hit_box.y + em.hit_box.height // 2), 5)
            em.new_move(self.wind)
        for p in self.clicks:
            pygame.draw.circle(self.wind, (255, 0, 0), (p[0], p[1]), 5, 0)
        pygame.display.update()
