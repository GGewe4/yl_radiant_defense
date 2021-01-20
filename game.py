import os
import sys

import pygame

from audio import GMusic
from enemies.enemy import enemies_sprites
from enemies.groupe_enemies import NEW_ENEMY, Group, NEW_WAVE
from game_menu import GameBar
from towers.archer_tower import ArcherTower
from towers.crossbow import CrossbowTower
from towers.magic_tower import MagicTower
from towers.power import PowerTower
from towers.tower import towers_sprites

from levels_configs import LVL1_TOWERS

PAUSE_TIME = pygame.USEREVENT + 3
# from enemies.minotaur import Minotaur
# from enemies.golem import Golem
# from enemies.wraith import Wraith
# from enemies.satyr import Satyr


#  [(856, 19), (820, 131), (670, 153), (439, 157), (342, 209),
#  (302, 266), (336, 321), (380, 389), (360, 455),
#  (403, 505), (471, 528), (557, 522), (619, 570), (634, 702)]

waves = [
    [0, 5, 3500],
    [1, 3, 4000],
    [2, 3, 2000],
    [0, 10, 1000]]

# [0, 50, 0, 1],
# [0, 100, 0],
# [20, 100, 0],
# [50, 100, 0],
# [100, 100, 0],
# [0, 0, 50, 3],
# [20, 0, 100],
# [20, 0, 150],
# [200, 100, 200],

LEVEL = 1


class Game:
    def __init__(self, wind, level=1):
        global LEVEL
        self.timers = [NEW_WAVE, NEW_ENEMY]
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
        self.del_enemies = []
        self.c = 0  # animation count

        self.mus = GMusic()
        self.mus.play_m('gelik')

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
        self.select = False

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
                        if not self.game_bar.showing:
                            for p in range(1, 12):
                                x1, y1 = pos
                                x2, y2 = self.t_points[str(p)][0]
                                if x1 in range(x2 - 20, x2 + 20) and y1 in range(y2 - 20, y2 + 20):
                                    self.cur_pos = p
                                    if self.t_points[str(self.cur_pos)][1] == 0:
                                        self.game_bar.showing = True
                                        break
                                    else:
                                        self.select = True
                                    break
                                else:
                                    for tower in self.towers:
                                        tower.selected = False
                                    self.cur_pos = 0
                        elif self.game_bar.showing:
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
                                    self.clicks.append(pos)
                            else:
                                self.game_bar.showing = False
                        elif self.select and not self.game_bar.showing:
                            for tower in self.towers:
                                if tower.collide(*pos, self.wind):
                                    tower.selected = True
                if event.type == NEW_ENEMY and not self.paused:
                    t = group.delay
                    group.delay += self.delay
                    group.update(self.enemies)
                    group.delay = t
                    self.delay = 0

                if event.type == NEW_WAVE and not self.paused:
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
            print(self.money, self.lives)

    def draw(self):
        self.del_enemies = []
        self.wind.blit(self.backg, (0, 0))
        self.game_bar.draw(self.wind)
        enemies_sprites.draw(self.wind)
        if self.c % 6 == 0:
            enemies_sprites.update()
        if self.c % 8 == 0:
            towers_sprites.update(self.enemies)
        for t in self.towers:
            # t.draw_radius(self.wind)
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
                    self.paused = True
                #     self.run = False
                #     self.enemies = []
                #     self.towers = []
                #     towers_sprites.empty()
                #     enemies_sprites.empty()
                #     for timer in self.timers:
                #         pygame.time.set_timer(timer, 0)
                self.del_enemies.append(en)
        for en in self.del_enemies:
            enemies_sprites.remove(en)
            self.enemies.remove(en)
        # for p in self.clicks:
        #     pygame.draw.circle(self.wind, (255, 0, 0), (p[0], p[1]), 5, 0)
        pygame.display.update()
