import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(1.5)
        alienlaser_sound = pg.mixer.Sound('sounds/alien_laser.wav')
        shiplaser_sound = pg.mixer.Sound('sounds/ship_laser.wav')
        gameover_sound = pg.mixer.Sound('sounds/game_over.wav')
        ufo_sound = pg.mixer.Sound('sounds/ufo_sounds.wav')
        self.sounds = {'alienlaser': alienlaser_sound, 'shiplaser': shiplaser_sound,
                       'gameover': gameover_sound, 'ufo':ufo_sound}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def shoot_laser(self, type): 
        pg.mixer.Sound.play(self.sounds['alienlaser' if type == LaserType.ALIEN else 'shiplaser'])
        
    def gameover(self): 
        self.stop_bg() 
        pg.mixer.music.load('sounds/game_over.wav')
        pg.mixer.music.set_volume(2.0)
        self.play_bg()
        time.sleep(3.5)
        self.stop_bg()
        pg.mixer.music.load('sounds/enemy_theme_v1.wav')
        pg.mixer.music.set_volume(2.0)
        self.play_bg()
