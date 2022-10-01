import pygame as pg
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector
from timer import Timer
from sys import exit


class Ship(Sprite):
    
    ship_explosion_images = [pg.image.load(f'images/ship_exp_{n}.png') for n in range(12)]
    ship_image = [pg.image.load('images/ship2.3.png') for n in range(1)]
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.ships_left = game.settings.ship_limit  
        self.image = pg.image.load('images/ship2.3.png')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.posn = self.center_ship()    # posn is the centerx, bottom of the rect, not left, top
        self.vel = Vector()
        self.lasers = game.ship_lasers
        self.lasers_attempted = 0
        self.shooting = False
        # self.dying = False
                
        #the first one is for the ship (still image) and the second one is the explosion (animation)
        self.timer_normal = Timer(image_list = Ship.ship_image)
        self.timer_explosion = Timer(image_list = Ship.ship_explosion_images, is_loop=False)
    
        self.timer = self.timer_normal
        
        
    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)
    
    def reset(self): 
        self.timer = self.timer_normal
        # reset the explosion
        self.timer_explosion.reset()
        self.vel = Vector()
        self.posn = self.center_ship()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y
        
    def die(self):
# # TODO: reduce the ships_left, 
# #       reset the game if ships > 0
# #       game_over if the ships == 0
        self.timer = self.timer_explosion
        print(f'Ship is dead! Only {self.ships_left} ships left')
        
    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.ships_left -= 1
            self.kill()
            self.game.reset() if self.ships_left > 0 else self.game.game_over()
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(game=self.game, x = self.rect.centerx, y=self.rect.top)
        self.lasers.update()
        self.draw()
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)
