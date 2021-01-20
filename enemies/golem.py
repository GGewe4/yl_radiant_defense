import pygame

from enemies.enemy import Enemy, load_image


class Golem(Enemy):
    imgs = []
    for x in range(18):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        imgs.append(pygame.transform.scale(load_image(
            f"data/enemies/golem/Walking/Golem_01_Walking_0" + add_str + ".png"), (80, 65)))

    def __init__(self, level_path=1):
        super().__init__(level_path)
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        self.frames = Golem.imgs[:]
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(self.x, self.y)
        self.hit_box = pygame.Rect(self.x, self.y, *self.image.get_size())
        self.change_vel()

        self.delta_x = 20
        self.delta_y = 10
        self.min_x = 40
        self.min_y = 10

        self.health = self.max_health = 20
