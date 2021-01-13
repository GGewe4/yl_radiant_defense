import pygame


class GMusic:
    def __init__(self, pause=False, load=False, volume=0.3, name='gelik'):
        self.is_paused = pause
        self.is_loaded = load
        self.volume = volume
        self.name = name

    def unload_m(self):
        pygame.mixer.music.unload()
        self.is_loaded = False

    def unpause_m(self):
        pygame.mixer.music.unpause()
        self.is_paused = False

    def pause_m(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def play_m(self, arg):
        if self.is_loaded:
            self.unload_m()
            self.is_loaded = True
        self.name = arg
        path = f"data/{self.name}.mp3"
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.volume)
        if self.is_paused:
            self.pause_m()

    def change_volume(self, new_value):
        self.volume = new_value
        pygame.mixer.music.set_volume(self.volume)