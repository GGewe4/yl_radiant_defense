import pygame


class Group:

    def __init__(self, type='', count=1, level=1):
        self.enemies = []
        for i in range(count):
            self.enemies.append()