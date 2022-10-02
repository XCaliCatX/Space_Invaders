import pygame as pg
from pygame.sprite import Sprite, Group
from barrier import Barriers
from laser import Lasers
from timer import Timer
from random import randint
# from sound import Sound
class Alien(Sprite):
    # alien_images = []
    # for n in range(2):
    #     alien_images.append(pg.image.load(f'images/alien{n}.bmp'))

    alien_images = [pg.image.load(f'images/alien{n}.bmp') for n in range(2)]

    alien_images0 = [pg.image.load(f'images/alien0{n}.png') for n in range(2)]
    alien_images1 = [pg.image.load(f'images/alien1{n}.png') for n in range(2)]
    alien_images2 = [pg.image.load(f'images/alien2{n}.png') for n in range(2)]
    alien_images3 = [pg.image.load(f'images/alien3{n}.png') for n in range(2)]

    alien_types = {0: alien_images0, 1 : alien_images1, 2: alien_images2, 3: alien_images3}    
    alien_timers = {0 : Timer(image_list=alien_images0), 
                   1 : Timer(image_list=alien_images1), 
                   2 : Timer(image_list=alien_images2), 
                   3 : Timer(image_list=alien_images3)}    

    alien_explosion_images = [pg.image.load(f'images/aExplosion{n}.png') for n in range(3)]
    
    ufo_score0 = [pg.transform.rotozoom(pg.image.load(f'images/ufo_score0{n}.png'), 0, 2) for n in range(5)]
    ufo_score1 = [pg.transform.rotozoom(pg.image.load(f'images/ufo_score1{n}.png'), 0, 2) for n in range(5)]
    ufo_score2 = [pg.transform.rotozoom(pg.image.load(f'images/ufo_score2{n}.png'), 0, 2) for n in range(5)]
    ufo_score3 = [pg.transform.rotozoom(pg.image.load(f'images/ufo_score3{n}.png'), 0, 2) for n in range(5)]
    ufo_score4 = [pg.transform.rotozoom(pg.image.load(f'images/ufo_score4{n}.png'), 0, 2) for n in range(5)]
    score_timers = {0 : Timer(image_list=ufo_score0, is_loop= False),
                    1 : Timer(image_list=ufo_score1, is_loop= False),
                    2 : Timer(image_list=ufo_score2, is_loop= False),
                    3 : Timer(image_list=ufo_score3, is_loop= False),
                    4 : Timer(image_list=ufo_score4, is_loop= False)}

    def __init__(self, game, type): # , sound
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/alien0.bmp')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.multi = randint(0, 4)
        self.sb = game.scoreboard
        self.dying = self.dead = False
        
        # sound.ufo_approach(type=self.type)
        
        # self.timer_normal = Timer(image_list=self.alien_images)   
        # self.timer_normal = Timer(image_list=self.alien_types[type])
                      
        self.timer_normal = Alien.alien_timers[type]              
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, is_loop=False)
        self.timer_show_score = Alien.score_timers[self.multi]
        self.timer = self.timer_normal                                    
    
    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)
    
    def hit(self):
        if not self.dying:
            self.dying = True 
            score_multi = 1
            if self.type == 0:      # green alien
                self.timer = self.timer_explosion
                score_multi = 4     # 400 points
                
            if self.type == 1:      # teal alien
                self.timer = self.timer_explosion
                score_multi = 2     # 200 points
            
            if self.type == 2:      # blue alien
                self.timer = self.timer_explosion
                score_multi = 1     # 100 points
            
            if self.type == 3:      # ufo
                score_multi = self.multi + 1
                self.timer = self.timer_show_score
                print(score_multi)
                
            self.sb.increment_score(score_multi)
            
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        if self.timer == self.timer_show_score and self.timer.is_expired():
            self.kill()
            self.timer_show_score.reset()
        settings = self.settings
        if self.type != 3:
            self.x += (settings.alien_speed_factor * settings.fleet_direction)
        else:
            self.x += settings.alien_speed_factor
        self.rect.x = self.x
        if not self.timer.is_expired(): # Done to prevent out of index error when printing the ufo score
            self.draw()
        
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect) 


class Aliens:
    def __init__(self, game): 
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.ufos = Group()
        self.ship_lasers = game.ship_lasers.lasers # a laser Group
        self.aliens_lasers = game.alien_lasers
        
        self.barriers = game.barriers.barriers   
        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0     
        self.ship = game.ship
        self.alien_count = len(self.aliens)
        self.aliens_half = 0
        self.aliens_losing = False
        self.song_changed = False
        
        self.create_fleet()
        
    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1 * alien_width))
        return number_aliens_x
    
    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1.5 * alien_height))
        return number_rows
            
    def reset(self):
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()
        
    def create_alien(self, alien_number, row_number):
        # if row_number > 5: raise ValueError('row number must be less than 6')
        type = row_number // 2     
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + alien.rect.height + 1 * alien.rect.height * row_number 
        self.aliens.add(alien)  
           
    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                   self.create_alien(alien_number, row_number)
        
        self.alien_count = len(self.aliens)
        self.aliens_half = len(self.aliens)/2
    
    def remaining_check(self):
        if self.alien_count <= self.aliens_half:
            self.aliens_losing = True
    
    def make_ufo(self):
        ufo = Alien(game=self.game, type=3)
        ufo_width = ufo.rect.width
        ufo.rect.x = ufo_width + 1 * ufo_width
        ufo.rect.y = ufo.rect.height
        self.ufos.add(ufo)
        ufo_sound = pg.mixer.Sound("sounds/ufo_sounds.wav")
        pg.mixer.Sound.play(ufo_sound, 1)        
    
    def spawn_ufo(self):
        can_spawn = 1000
        spawn_try = randint(0, 9300)
        if spawn_try % can_spawn == 0:
            self.make_ufo()
            
            
            
            
    
    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.die()
                break
    
    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()
    
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return
        
        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1
    
    def check_collisions(self):  
        # aliens hit by ship laser
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()  
                self.alien_count -= 1
        # ufo hit by ship laser
        collisions = pg.sprite.groupcollide(self.ufos, self.ship_lasers, False, True)  
        if collisions:
            for ufo in collisions:
                ufo.hit()
                self.channel1.stop()
        # lasers hit each other
        collisions = pg.sprite.groupcollide(self.aliens_lasers.lasers, self.ship_lasers,False,True) 
        if collisions:
            for laser in collisions:
                self.aliens_lasers.lasers.remove()
                self.ship_lasers.remove()
        
        # Ship hits alien lasers
        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.die() # Ship doesn't have a health bar, so skipped hit and went straight to die
        #alien lasers hit barrier
        collisions = pg.sprite.groupcollide(self.barriers, self.aliens_lasers.lasers, False, True)
        if collisions:
            for barrier in collisions:
                barrier.hit()
        #ship lasers hit barrier
        collisions = pg.sprite.groupcollide(self.barriers, self.ship_lasers, False,True)
        if collisions:   
            for barrier in collisions:
                barrier.hit()
                    
        
    def update(self): 
        
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.spawn_ufo()
        print(self.alien_count)
        self.remaining_check()
        print(self.aliens_losing)
        self.shoot_from_random_alien()
        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update() 
        for ufo in self.ufos.sprites():
            if ufo.dead:      # set True once the explosion animation has completed
                ufo.remove()
            ufo.update() 
        self.aliens_lasers.update()
    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
        for ufo in self.ufos.sprites(): 
            ufo.draw() 