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
        self.barriers = Group()
        self.create_barriers()
        self.dead =self.dying= False
        
    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 3.0
        top = self.settings.screen_height - 2 * height
        for i in range(4):
            barrier = Barrier(game=self.game, health = 200, rect=pg.Rect(i * 2 * width + 1.5 * width, top, width, height))
            self.barriers.add(barrier)
            print(self.barriers)
        
    
    def reset(self):
        for barrier in self.barriers.sprites():
            if barrier.dead:      # set True once the explosion animation has completed
                barrier.remove()

        self.create_barriers()
        
    
    def update(self):
        for barrier in self.barriers.sprites():
            if barrier.dead:      # set True once the explosion animation has completed
                self.barriers.remove(barrier)
            barrier.update()
        for barrier in self.barriers.sprites():
            barrier.update()
    
    def draw(self):
        for barrier in self.barriers.sprites():
            barrier.draw()