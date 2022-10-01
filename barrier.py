import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers


class Barrier(Sprite):
    color = 125, 0, 125
    def __init__(self, game, health, rect):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.rect = rect
        self.health = health
        self.dead =self.dying= False
        # self.rect.y = self.rect.height
        # self.x = float(self.rect.x)
        self.remake()
        
    def hit(self): 
        print("Barrier hit")
        self.health-=50
        print(self.health)
        if self.health <= 0:
            self.dying = True
        return self.dying

    def destroyed(self):
        if self.dying:
            self.dead = True
    
    def remake(self):
        self.dead = False
        self.dying = False
          
    def update(self):
        self.draw()
        
    def draw(self):
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width/5)
        
        
class Barriers:
    def __init__(self, game): 
        self.game = game
        self.settings = game.settings
        self.create_barriers()
        self.dead =self.dying= False
        
    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 3.0
        top = self.settings.screen_height - 2 * height
        self.barriers = [Barrier(game=self.game, health = 200, rect=pg.Rect(x * 2 * width + 1.5 * width, top, width, height)) for x in range(4)]
        print(self.barriers)
        
    def hit(self, barrier):
        dying = barrier.hit()
        if barrier.destroyed(): # So we don't get errors when the lasers hit a barrier that was destroyed
            return
        if dying:
            self.barriers.remove(barrier)
            
    def reset(self):
        self.create_barriers()
        
    
    def update(self):
        for barrier in self.barriers:
            barrier.update()
    
    def draw(self):
        for barrier in self.barriers:
            barrier.draw()