import pygame
import os
import math

towers_sprites = pygame.sprite.Group()


def intersects(rect, r, center):
    circle_distance_x = abs(center[0] - rect.centerx)
    circle_distance_y = abs(center[1] - rect.centery)
    if circle_distance_x > rect.w / 2.0 + r or circle_distance_y > rect.h / 2.0 + r:
        return False
    if circle_distance_x <= rect.w / 2.0 or circle_distance_y <= rect.h / 2.0:
        return True
    corner_x = circle_distance_x - rect.w / 2.0
    corner_y = circle_distance_y - rect.h / 2.0
    corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
    return corner_distance_sq <= r ** 2.0


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(towers_sprites)
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 0
        self.selected = False
        self.main_img = None
        self.damage = 1
        self.range = 0
        self.archer_count = 0
        self.attack_imgs = []
        self.state = False

    def upgrade(self):
        pass

    def click(self):
        pass

    def attack(self, enemies):
        if self.state:
            enemy_closest = []
            for enemy in enemies:
                if intersects(enemy.hit_box, self.range, (self.x, self.y)):
                    self.state = True
                    if self.archer_count == len(self.attack_imgs) - 1:
                        if enemy.hit(self.damage):
                            enemies.remove(enemy)
                        enemy_closest.append(enemy)
                        self.archer_count = 0
            if not enemy_closest:
                self.state = False

    def update(self, enemies):
        for enemy in enemies:
            if intersects(enemy.hit_box, self.range, (self.x, self.y)):
                self.state = True
        if self.state:
            self.image = self.attack_imgs[self.archer_count]
            self.archer_count = (self.archer_count + 1) % len(self.attack_imgs)
        else:
            self.image = self.main_img

    def draw_radius(self, win):
        surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (128, 128, 128, 120), (self.range, self.range), self.range, 0)
        win.blit(surface, (self.x - self.range, self.y - self.range))


def load_image(name, colorkey=None):
    pygame.init()
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
