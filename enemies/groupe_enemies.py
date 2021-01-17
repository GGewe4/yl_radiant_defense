import pygame
from enemies.golem import Golem
from enemies.wraith import Wraith
from enemies.minotaur import Minotaur
from enemies.satyr import Satyr

NEW_ENEMY = pygame.USEREVENT + 1
NEW_WAVE = pygame.USEREVENT + 2

class Group:
    def __init__(self, type=0, count=1, delay=100):
        pygame.time.set_timer(NEW_ENEMY, 100)
        self.delay = delay
        self.enemies = []
        self.cur_enemy = 0
        self.count = count
        self.type = type

    def update(self, enemies):
        pygame.time.set_timer(NEW_ENEMY, self.delay)
        if self.cur_enemy < self.count:
            self.cur_enemy += 1
            if self.type == 0:
                enemies.append(Golem())
            if self.type == 1:
                enemies.append(Wraith())
            if self.type == 2:
                enemies.append(Minotaur())
            if self.type == 3:
                enemies.append(Satyr())
        if self.count == self.cur_enemy:
            pygame.time.set_timer(NEW_WAVE, 15000)
            self.cur_enemy = self.count + 1