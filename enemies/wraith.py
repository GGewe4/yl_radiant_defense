import pygame

from enemies.enemy import Enemy, load_image


class Wraith(Enemy):
    imgs = []
    for x in range(12):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        imgs.append(pygame.transform.scale(load_image(
            f"data/enemies/wraith/Walking/Wraith_frame_" + add_str + ".png"), (80, 65)))

    def __init__(self, level_path=1):
        super().__init__(level_path)
        self.frames = Wraith.imgs[:]
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_width())
        self.rect = self.rect.move(self.x, self.y)
        self.hit_box = pygame.Rect(self.x, self.y, *self.image.get_size())

        self.delta_x = 20
        self.delta_y = 0
        self.min_x = 40
        self.min_y = 10

        self.money_for_kill = 10
        self.vel = 50 / 120
        self.health = self.max_health = 50
        self.change_vel()
