import pygame

from enemies.golem import Golem
from enemies.minotaur import Minotaur
from enemies.satyr import Satyr
from enemies.wraith import Wraith

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
        from game import LEVEL
        pygame.time.set_timer(NEW_ENEMY, self.delay)
        if self.cur_enemy < self.count:
            if self.type == 0:
                enemies.append(Golem(LEVEL))
            if self.type == 1:
                enemies.append(Wraith(LEVEL))
            if self.type == 2:
                enemies.append(Minotaur(LEVEL))
            if self.type == 3:
                enemies.append(Satyr(LEVEL))
        self.cur_enemy += 1
        if self.count == self.cur_enemy:
            pygame.time.set_timer(NEW_WAVE, 15000)
            pygame.time.set_timer(NEW_ENEMY, 0)
            return True
        return False


