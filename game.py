import copy
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

waves = [
    [3, 9, 4000],
    [2, 4, 5000],
    [1, 10, 9000],
    [0, 5, 3000],
    [1, 20, 2500],
    [2, 10, 1500],
    [3, 25, 1000],
    [0, 0, 0]]

# global var
LEVEL = 1


class Game:
    def __init__(self, wind, mus_pause, level=1):
        global LEVEL
        # my event.type for discard
        self.timers = [NEW_WAVE, NEW_ENEMY]
        # base attributes
        self.wind = wind
        self.level = level
        self.paused = True
        LEVEL = self.level
        # 1600 900, 16/9
        self.width = 1280
        self.height = 720

        # load background, win and lose image
        self.backg = pygame.transform.scale(pygame.image.load("data/ui/bg_test5.png"),
                                            (self.width, self.height))
        self.win_img = pygame.transform.scale(pygame.image.load('data/ui/win_screen.png'),
                                              (1280, 720))
        self.lose_img = pygame.transform.scale(pygame.image.load('data/ui/lose.png'), (1280, 720))
        self.mus_icon = pygame.transform.scale(pygame.image.load("data/ui/mus_icon.jpg"), (50, 50))
        self.krest_icon = pygame.transform.scale(pygame.image.load("data/ui/krest.png"), (50, 50))

        self.clicks = []  # list of clicks for debugging
        self.circ = []  # path for enemy
        with open(os.path.join(f'levels/level{self.level}/path.txt')) as file:
            self.circ = eval(''.join(file.readlines()))
        # list for enemies, towers, and enemies to del
        self.enemies = []
        self.towers = []
        self.del_enemies = []
        self.animation_count = 0  # animation count
        # create music and game ui
        self.game_bar = GameBar()
        self.mus = GMusic(pause=mus_pause)
        self.mus.play_m('1lvl')
        # args for cor wave
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        # pause delay
        self.delay = 0
        # type of selected tower
        self.selected_tower = 0
        # gameplay attributes
        self.lives = 20
        self.money = 300
        self.running = True
        # copy the dict
        self.t_points = copy.deepcopy(LVL1_TOWERS)
        # par for win or lose
        self.wait = True
        # cor change wave
        self.ready_to_next_wave = False

    def run(self):
        # main cycle
        clock = pygame.time.Clock()
        self.group = Group(*self.current_wave)
        self.wind.blit(self.backg, (0, 0))
        pygame.display.update()
        while self.running:
            self.animation_count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.clicks)
                    sys.exit()
                pos = pygame.mouse.get_pos()
                # processing click mouse button
                if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                    if event.button == 1:
                        if pos[0] in range(30, 80) and pos[1] in range(600, 650):
                            if self.mus.is_paused:
                                self.mus.is_paused = False
                                self.mus.unpause_m()
                            else:
                                self.mus.is_paused = True
                                self.mus.pause_m()

                        elif self.game_bar.showing:
                            type_tower = self.game_bar.collide(*pos)
                            self.game_bar.showing = False
                            if type_tower:
                                self.selected_tower = type_tower
                                if self.selected_tower == 1 and self.money >= 50:
                                    tower = ArcherTower(*self.t_points[str(self.cur_pos)][0])
                                    self.money -= tower.price[tower.level]
                                    self.towers.append(tower)
                                    self.t_points[str(self.cur_pos)][1] = 1

                                elif self.selected_tower == 2 and self.money >= 75:
                                    tower = CrossbowTower(*self.t_points[str(self.cur_pos)][0])
                                    self.money -= tower.price[tower.level]
                                    self.towers.append(tower)
                                    self.t_points[str(self.cur_pos)][1] = 2

                                elif self.selected_tower == 3 and self.money >= 125:
                                    tower = PowerTower(*self.t_points[str(self.cur_pos)][0])
                                    self.money -= tower.price[tower.level]
                                    self.towers.append(tower)
                                    self.t_points[str(self.cur_pos)][1] = 3

                                elif self.selected_tower == 4 and self.money >= 150:
                                    tower = MagicTower(*self.t_points[str(self.cur_pos)][0])
                                    if self.money >= tower.price[tower.level]:
                                        self.money -= tower.price[tower.level]
                                        self.towers.append(tower)
                                        self.t_points[str(self.cur_pos)][1] = 4

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

                # add new enemy with cor pause delay
                if event.type == NEW_ENEMY and not self.paused:
                    t = self.group.delay
                    self.group.delay += self.delay
                    self.ready_to_next_wave = self.group.update(self.enemies)
                    self.group.delay = t
                    self.delay = 0

                # processing new wave
                if event.type == NEW_WAVE and not self.paused:
                    self.change_wave()

                # processing keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.clicks.clear()
                        if self.mus.is_paused:
                            self.mus.unpause_m()
                        else:
                            self.mus.pause_m()
                    elif event.key == pygame.K_PERIOD:
                        self.mus.next_track()
                    elif event.key == pygame.K_COMMA:
                        self.mus.prev_track()
                    elif event.key == pygame.K_LSHIFT:
                        self.paused = not self.paused
                    elif event.key == pygame.K_EQUALS:
                        self.mus.change_volume(self.mus.volume + 0.05)
                    elif event.key == pygame.K_MINUS:
                        self.mus.change_volume(self.mus.volume - 0.05)
                    elif event.key == pygame.K_ESCAPE:
                        # exit to main menu
                        towers_sprites.empty()
                        enemies_sprites.empty()
                        self.running = False
                        for timer in self.timers:
                            pygame.time.set_timer(timer, 0)
            # processing new wave
            if self.ready_to_next_wave and not self.enemies:
                self.change_wave()

            # processing pause the game
            if not self.paused:
                self.draw()
                self.delay = 0
            else:
                self.delay += 1000 // 120
            clock.tick(120)

    def draw(self):
        # main func for draw
        self.del_enemies = []
        # blit background and game ui
        self.wind.blit(self.backg, (0, 0))
        self.game_bar.draw(self.wind, self.lives, self.money)

        # animation for towers and enemies
        if self.animation_count % 6 == 0:
            enemies_sprites.update()
        if self.animation_count % 8 == 0:
            towers_sprites.update(self.enemies)

        enemies_sprites.draw(self.wind)

        for tower in self.towers:
            if tower.selected:
                tower.draw_radius(self.wind)
            # attack for towers
            self.money += tower.attack(self.enemies)

        towers_sprites.draw(self.wind)

        for enemy in self.enemies:
            # debug
            # pygame.draw.circle(self.wind, (0, 255, 0), (enemy.hit_box.x + enemy.hit_box.width
            # // 2, enemy.hit_box.y + enemy.hit_box.height // 2), 5)
            if enemy.new_move(self.wind):
                # processing reach point and lose
                self.lives -= 1
                if self.lives <= 0:
                    self.lose()
                self.del_enemies.append(enemy)
        # processing win
        if self.wave == len(waves) - 1 and not self.enemies:
            self.win()
        self.wind.blit(self.mus_icon, (30, 600))
        if self.mus.is_paused:
            self.wind.blit(self.krest_icon, (30, 600))
        # remove all dying enemies
        for enemy in self.del_enemies:
            enemies_sprites.remove(enemy)
            self.enemies.remove(enemy)
        # debug
        # for p in self.clicks:
        #     pygame.draw.circle(self.wind, (255, 0, 0), (p[0], p[1]), 5, 0)
        # for circ in self.circ:
        #     pygame.draw.circle(self.wind, (255, 0, 0), circ, 5)
        pygame.display.update()

    def win(self):
        # processing win
        self.wind.blit(self.win_img, (0, 0))
        pygame.display.update()
        # wait the mouse click
        while self.wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        towers_sprites.empty()
                        enemies_sprites.empty()
                        self.running = False
                        for timer in self.timers:
                            pygame.time.set_timer(timer, 0)
                        self.wait = False

    def lose(self):
        # processing lose
        self.wind.blit(self.lose_img, (0, 0))
        pygame.display.update()
        # wait the mouse click
        while self.wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        towers_sprites.empty()
                        enemies_sprites.empty()
                        self.running = False
                        for timer in self.timers:
                            pygame.time.set_timer(timer, 0)
                        self.wait = False

    def change_wave(self):
        # go to the next wave
        pygame.time.set_timer(NEW_WAVE, 0)
        self.wave += 1
        if self.wave + 1 < len(waves):
            self.current_wave = waves[self.wave][:]
            self.ready_to_next_wave = False
            self.group = Group(*self.current_wave)
        else:
            pygame.time.set_timer(NEW_WAVE, 0)
            pygame.time.set_timer(NEW_ENEMY, 0)
