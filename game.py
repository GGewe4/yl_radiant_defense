import os
import sys

import pygame

from audio import GMusic
from enemies.enemy import enemies_sprites
from enemies.groupe_enemies import NEW_ENEMY, Group, NEW_WAVE
from game_ui import GameBar
from levels_configs import LVL1_TOWERS
from towers.archer_tower import ArcherTower
from towers.crossbow import CrossbowTower
from towers.magic_tower import MagicTower
from towers.power import PowerTower
from towers.tower import towers_sprites

# from enemies.minotaur import Minotaur
# from enemies.golem import Golem
# from enemies.wraith import Wraith
# from enemies.satyr import Satyr


#  [(856, 19), (820, 131), (670, 153), (439, 157), (342, 209),
#  (302, 266), (336, 321), (380, 389), (360, 455),
#  (403, 505), (471, 528), (557, 522), (619, 570), (634, 702)]

waves = [
    [3, 5, 3500],
    [3, 3, 4000],
    [0, 0, 0]]
# [2, 3, 2000],
# [0, 10, 1000]]

LEVEL = 1


class Game:
    def __init__(self, wind, level=1):
        global LEVEL
        self.timers = [NEW_WAVE, NEW_ENEMY]
        self.wind = wind
        self.width = 1280  # 1600 900, 16/9
        self.height = 720
        self.backg = pygame.image.load("data/ui/bg_test5.png")
        self.win_img = pygame.transform.scale(pygame.image.load('data/ui/win_screen.png'),
                                              (1280, 720))
        self.lose_img = pygame.transform.scale(pygame.image.load('data/ui/lose.png'), (1280, 720))
        self.backg = pygame.transform.scale(self.backg, (self.width, self.height))
        self.clicks = []  # delete
        self.circ = []
        with open(os.path.join(f'levels/level{1}/path.txt')) as file:
            self.circ = eval(''.join(file.readlines()))
        self.enemies = []
        self.towers = []
        self.del_enemies = []
        self.c = 0  # animation count

        self.mus = GMusic()
        self.mus.play_m('1lvl')

        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.delay = 0
        self.selected_tower = 0

        self.level = level
        self.paused = True
        LEVEL = self.level

        self.lives = 1
        self.money = 5000

        self.game_bar = GameBar()
        self.running = True

        self.t_points = LVL1_TOWERS
        self.wait = True

    def run(self):
        clock = pygame.time.Clock()
        group = Group(*self.current_wave)
        self.wind.blit(self.backg, (0, 0))
        # self.game_bar.draw(self.wind)
        pygame.display.update()
        while self.running:
            self.c += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.clicks)
                    sys.exit()
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                    if event.button == 1:

                        if self.game_bar.showing:
                            type_tower = self.game_bar.collide(*pos)
                            if type_tower:
                                self.selected_tower = type_tower
                                self.game_bar.showing = False
                                if self.selected_tower == 1:
                                    tower = ArcherTower(*self.t_points[str(self.cur_pos)][0])
                                    if self.money >= tower.price[tower.level]:
                                        self.money -= tower.price[tower.level]
                                        self.towers.append(tower)
                                        self.t_points[str(self.cur_pos)][1] = 1
                                    else:
                                        towers_sprites.remove(tower)
                                    self.clicks.append(pos)
                                elif self.selected_tower == 2:
                                    tower = CrossbowTower(*self.t_points[str(self.cur_pos)][0])
                                    if self.money >= tower.price[tower.level]:
                                        self.money -= tower.price[tower.level]
                                        self.towers.append(tower)
                                        self.t_points[str(self.cur_pos)][1] = 1
                                    else:
                                        towers_sprites.remove(tower)
                                    self.clicks.append(pos)
                                elif self.selected_tower == 3:
                                    tower = PowerTower(*self.t_points[str(self.cur_pos)][0])
                                    if self.money >= tower.price[tower.level]:
                                        self.money -= tower.price[tower.level]
                                        self.towers.append(tower)
                                        self.t_points[str(self.cur_pos)][1] = 1
                                    else:
                                        towers_sprites.remove(tower)
                                    self.clicks.append(pos)
                                elif self.selected_tower == 4:
                                    tower = MagicTower(*self.t_points[str(self.cur_pos)][0])
                                    if self.money >= tower.price[tower.level]:
                                        self.money -= tower.price[tower.level]
                                        self.towers.append(tower)
                                        self.t_points[str(self.cur_pos)][1] = 1
                                    else:
                                        towers_sprites.remove(tower)
                            else:
                                self.game_bar.showing = False

                        else:
                            for tower in self.towers:
                                tower.selected = False

                            for p in range(1, 12):
                                x1, y1 = pos
                                x2, y2 = self.t_points[str(p)][0]
                                if x1 in range(x2 - 20, x2 + 20) and y1 in range(y2 - 20, y2 + 20):
                                    self.cur_pos = p
                                    if self.t_points[str(self.cur_pos)][1] == 0:
                                        self.game_bar.showing = True
                                        break

                            for tower in self.towers:
                                if tower.collide(self.wind, *pos):
                                    tower.selected = True
                                    break
                    self.clicks.append(pos)

                if event.type == NEW_ENEMY and not self.paused:
                    t = group.delay
                    group.delay += self.delay
                    group.update(self.enemies)
                    group.delay = t
                    self.delay = 0

                if event.type == NEW_WAVE and not self.paused:
                    self.wave += 1
                    if self.wave + 1 < len(waves):
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
                    elif event.key == pygame.K_LSHIFT:
                        self.paused = not self.paused

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.enemies = []
                        self.towers = []
                        towers_sprites.empty()
                        enemies_sprites.empty()
                        self.running = False
                        for timer in self.timers:
                            pygame.time.set_timer(timer, 0)
            if not self.paused:
                self.draw()
                self.delay = 0
            else:
                self.delay += 1000 // 120
            clock.tick(120)

    def draw(self):
        self.del_enemies = []
        self.wind.blit(self.backg, (0, 0))
        self.game_bar.draw(self.wind, self.lives, self.money)
        enemies_sprites.draw(self.wind)
        if self.c % 6 == 0:
            enemies_sprites.update()
        if self.c % 8 == 0:
            towers_sprites.update(self.enemies)
        for t in self.towers:
            t.collide(self.wind, 0, 0)
            if t.selected:
                t.draw_radius(self.wind)
            self.money += t.attack(self.enemies)
        towers_sprites.draw(self.wind)
        for en in self.enemies:
            # pygame.draw.circle(self.wind, (0, 255, 0), (en.hit_box.x + en.hit_box.width // 2,
            # en.hit_box.y + en.hit_box.height // 2), 5)
            if en.new_move(self.wind):
                self.lives -= 1
                if self.lives <= 0:
                    self.lose()
                #     self.run = False
                #     self.enemies = []
                #     self.towers = []
                #     towers_sprites.empty()
                #     enemies_sprites.empty()
                #     for timer in self.timers:
                #         pygame.time.set_timer(timer, 0)
                self.del_enemies.append(en)
        if self.wave == len(waves) - 1 and not self.enemies:
            self.win()
        for en in self.del_enemies:
            enemies_sprites.remove(en)
            self.enemies.remove(en)
        # for p in self.clicks:
        #     pygame.draw.circle(self.wind, (255, 0, 0), (p[0], p[1]), 5, 0)
        # for circ in self.circ:
        #     pygame.draw.circle(self.wind, (255, 0, 0), circ, 5)
        pygame.display.update()

    def win(self):
        self.wind.blit(self.win_img, (0, 0))
        pygame.display.update()
        while self.wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.wait = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.running = False
                        self.wait = False

    def lose(self):
        self.wind.blit(self.lose_img, (0, 0))
        pygame.display.update()
        while self.wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.wait = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.running = False
                        self.wait = False

