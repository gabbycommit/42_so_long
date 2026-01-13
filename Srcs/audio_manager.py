import pygame as pg


class AudioManager:
    def __init__(self):
        pg.mixer.init()

        self.current_bgm = None
        self.bgm_volume = 0.3

        self.sfx = {}

    def play_bgm(self, path):
        if self.current_bgm == path:
            return

        pg.mixer.music.stop()
        pg.mixer.music.load(path)
        pg.mixer.music.set_volume(self.bgm_volume)
        pg.mixer.music.play(-1)

        self.current_bgm = path

    def stop_bgm(self):
        pg.mixer.music.stop()
        self.current_bgm = None

    def load_sfx(self, name, path, volume=1.0):
        sound = pg.mixer.Sound(path)
        sound.set_volume(volume)
        self.sfx[name] = sound

    def play_sfx(self, name):
        if name in self.sfx:
            self.sfx[name].play()
