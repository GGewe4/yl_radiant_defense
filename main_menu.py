import sys
import pygame

from audio import GMusic
from game import Game


class MainMenu:
    def __init__(self, wind):
        self.width = 1280
        self.height = 720

        self.bgr = pygame.image.load("data/ui/mt2.jpg")
        self.bgr = pygame.transform.scale(self.bgr, (self.width, self.height))
        self.wind = wind

        self.mus = GMusic(volume=0.1)
        self.mus.play_m('hom')

        self.tr_pos = 1
        self.tr_coord = (370, 500)
        self.m_x = 0
        self.m_y = 0

        self.m_icon = pygame.image.load("data/ui/mus_icon.jpg")

        self.krest = pygame.image.load("data/ui/krest.png")
        self.krest = self.krest.convert_alpha()
        self.krest = pygame.transform.scale(self.krest, (58, 60))

        self.triangle = pygame.image.load("data/ui/cht.png")
        self.triangle = self.triangle.convert_alpha()
        self.triangle = pygame.transform.scale(self.triangle, (75, 75))

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.m_x, self.m_y = pygame.mouse.get_pos()

                    if self.m_x in range(20, 80) and self.m_y in range(20, 80):
                        if self.mus.is_paused:
                            self.mus.unpause_m()
                        else:
                            self.mus.pause_m()

                    elif self.m_x in range(485, 820) and self.m_y in range(120, 230):
                        self.run_game()

                    elif self.m_x in range(485, 820) and self.m_y in range(305, 415):
                        if self.mus.name == 'hom':
                            self.mus.play_m('gelik')
                        else:
                            self.mus.play_m('hom')

                    elif self.m_x in range(485, 820) and self.m_y in range(485, 595):
                        sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.tr_pos = (self.tr_pos - 1) % 3

                    if event.key == pygame.K_DOWN:
                        self.tr_pos = (self.tr_pos + 1) % 3

                    if event.key == pygame.K_SPACE:
                        if self.tr_pos == 1:
                            self.run_game()

                        elif self.tr_pos == 2:
                            if self.mus.name == 'hom':
                                self.mus.play_m('gelik')
                            else:
                                self.mus.play_m('hom')

                        else:
                            sys.exit()

            self.draw()
        pygame.quit()

    def draw(self):
        self.wind.blit(self.bgr, (0, 0))
        self.wind.blit(self.m_icon, (20, 20))

        if self.mus.is_paused:
            self.wind.blit(self.krest, (20, 20))

        if self.tr_pos == 1:
            self.tr_coord = (370, 150)
        elif self.tr_pos == 2:
            self.tr_coord = (370, 325)
        else:
            self.tr_coord = (370, 500)

        self.wind.blit(self.triangle, self.tr_coord)
        pygame.display.update()

    def run_game(self):
        game = Game(self.wind)
        game.run()
        del game
        self.mus.play_m('hom')
