import os

import pygame

DIR_LEVELS = 'levels'
enemies_sprites = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, level_path=1):
        super().__init__(enemies_sprites)
        self.max_health = 10
        self.health = 10
        self.frames = []
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        with open(os.path.join(f'{DIR_LEVELS}/level{level_path}/path.txt')) as file:
            self.path = eval(''.join(file.readlines()))
            self.path = list(map(lambda x: (x[0], x[1] - 50), self.path))
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.vel_x = 0
        self.vel_y = 0
        self.vel = 100 / 120
        self.money_for_kill = 40

        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.flipped = True

        self.delta_x = 0
        self.delta_y = 0
        self.min_x = 0
        self.min_y = 0

        self.x2 = self.x
        self.y2 = self.y

    def draw(self):
        pass

    def collide(self):
        pass

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            pygame.sprite.Sprite.kill(self)
            return True

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def new_move(self, wind):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width() - 20,
                                self.image.get_height())
        self.hit_box = pygame.Rect(self.x + self.delta_x, self.y + self.delta_y,
                                   self.image.get_width() - self.min_x,
                                   self.image.get_height() - self.min_y)
        # print(self.x, self.y, '    |    ', self.x2, self.y2)
        self.draw_health_bar(wind)
        if abs(self.x - self.x2) <= self.vel * 2 and abs(self.y - self.y2) <= self.vel * 2:
            return self.change_vel()

    def change_vel(self):
        f = False
        x1, y1 = self.path[min(self.path_pos, len(self.path) - 1)]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (609, 800)
        else:
            x2, y2 = self.path[self.path_pos + 1]
        if self.path_pos + 1 == len(self.path):
            f = True
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        self.vel_x = (x2 - x1) / (distance / self.vel)
        self.vel_y = (y2 - y1) / (distance / self.vel)
        if self.vel_x > 0 and not self.flipped:
            self.flipped = True
            for x, img in enumerate(self.frames):
                self.frames[x] = pygame.transform.flip(img, True, False)
        elif self.vel_x < 0 and self.flipped:
            self.flipped = False
            for x, img in enumerate(self.frames):
                self.frames[x] = pygame.transform.flip(img, True, False)
        self.x2 = x2
        self.y2 = y2
        self.path_pos += 1
        return f

    def draw_health_bar(self, wind):
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)
        pygame.draw.rect(wind, (255, 0, 0), (self.x + 15, self.y, length, 7), 0)
        pygame.draw.rect(wind, (0, 255, 0), (self.x + 15, self.y, health_bar, 7), 0)
        # pygame.draw.rect(wind, (255, 255, 255), self.hit_box, 5)


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
