import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers


class Barrier(Sprite):
    color = 125, 0, 125
    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = rect
        # self.rect.y = self.rect.height
        # self.x = float(self.rect.x)
        
    def hit(self): 
        print("Barrier hit")
        self.kill()
    
    def update(self):
        self.draw()
        
    def draw(self):
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width/5)
        
        
class Barriers:
    def __init__(self, game): # put lasers in
        self.game = game
        self.settings = game.settings
        self.create_barriers()
        
        
    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 3.0
        top = self.settings.screen_height - 2 * height
        self.barriers = [Barrier(game=self.game, rect=pg.Rect(x * 2 * width + 1.5 * width, top, width, height)) for x in range(4)]
        
    def reset(self):
        self.create_barriers()
    
    def update(self):
        for barrier in self.barriers:
            barrier.update()
    
    def draw(self):
        for barrier in self.barriers:
            barrier.draw()