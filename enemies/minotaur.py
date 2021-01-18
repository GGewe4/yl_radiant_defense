import pygame

from enemies.enemy import Enemy, load_image


class Minotaur(Enemy):
    imgs = []
    for x in range(18):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        imgs.append(pygame.transform.scale(load_image(
            f"data/enemies/minotaur/Walking/Minotaur_01_Walking_0" + add_str + ".png"), (80, 65)))

    def __init__(self, level_path=1):
        super().__init__(level_path)
        self.frames = Minotaur.imgs[:]
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_width())
        self.rect = self.rect.move(self.x, self.y)
        self.change_vel()

        self.delta_x = 20
        self.delta_y = 10
        self.min_x = 40
        self.min_y = 10

        self.hit_box = pygame.Rect(self.x, self.y, *self.image.get_size())
