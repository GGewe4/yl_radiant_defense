import pygame
from enemies.enemy import Enemy, load_image


class Wraith(Enemy):
    def __init__(self):
        super().__init__()
        self.frames = []
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        for x in range(12):
            add_str = str(x)
            if x < 10:
                add_str = "0" + add_str
            self.frames.append(pygame.transform.scale(load_image(
                f"data/enemies/wraith/Walking/Wraith_01_MovingForward_0" + add_str + ".png"), (80, 65)))
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_width())
        self.rect = self.rect.move(self.x, self.y)
        self.change_vel()