import pygame as pg
from settings import Settings
import game_functions as gf

from laser import Lasers
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")

        self.scoreboard = Scoreboard(game=self)  
        self.lasers = Lasers(settings=self.settings)
        self.ship = Ship(game=self, screen=self.screen, settings=self.settings, sound=self.sound, lasers=self.lasers)
        self.aliens = Aliens(game=self, screen=self.screen, settings=self.settings, lasers=self.lasers, ship=self.ship)
        self.settings.initialize_speed_settings()
    def game_intro(self):
         # white color 
        color = (0,0,0)
        white= (250,250,250) 
        green= (118,238,0)
        # light shade of the button 
        color_light = (202,255,112) 
        # dark shade of the button 
        color_dark = (100,100,100)
        # stores the width of the 
        # screen into a variable 
        width = self.screen.get_width() 
        # stores the height of the 
        # screen into a variable 
        height = self.screen.get_height() 
        # defining a font 
        smallfont = pg.font.SysFont('Corbel',35)
        largefont=pg.font.Font('space_invaders.ttf', 60)
        point_values = pg.font.Font('space_invaders.ttf',30)
        # rendering a text written in 
        # this font
        #Words
        quit = smallfont.render('quit' , True , color) 
        play = smallfont.render('play' , True , color)
        space = largefont.render('Space', True, white)
        invaders = largefont.render('INVADERS',True, green)
        #point values
        equals_400 = point_values.render('= 400',True, green)
        equals_200 = point_values.render('=200', True, green)
        equals_100 = point_values.render('=100', True, green)
        #images
        aliengreen=pg.image.load("images/alien01.png")
        alienblue=pg.image.load("images/alien20.png")
        alienteal = pg.image.load("images/alien10.png")
        while True: 
            for ev in pg.event.get(): 
                if ev.type == pg.QUIT: 
                    pg.quit() 
            #checks if a mouse is clicked 
                if ev.type == pg.MOUSEBUTTONDOWN: 
            #if the mouse is clicked on the 
            # button the game is terminated 
                    if width/2 <= mouse[0] <= width/2+140 and height/2+(height/4) <= mouse[1] <= height/2+40+(height/4): 
                        pg.quit() 
                    elif width/2-140 <= mouse[0] <= width/2 and (height/2)+(height/4) <= mouse[1] <= (height/2)+40+(height/4):
                        self.play()
        # fills the screen with a color 
            self.screen.fill((0,0,0)) 
      
        # stores the (x,y) coordinates into 
        # the variable as a tuple 
            mouse = pg.mouse.get_pos() 
        # if mouse is hovered on a button it 
         # changes to lighter shade 
            if width/2 <= mouse[0] <= width/2+140 and height/2+(height/4) <= mouse[1] <= height/2+40+(height/4): 
                pg.draw.rect(self.screen,color_light,[width/2,height/2+(height/4),140,40])
            elif width/2-180 <= mouse[0] <= width/2+40 and (height/2)+(height/4) <= mouse[1] <= height/2+40+(height/4): 
                pg.draw.rect(self.screen,color_light,[width/2-180,(height/2)+(height/4),140,40])
            else: 
                pg.draw.rect(self.screen,color_dark,[width/2,height/2+(height/4),140,40])
                pg.draw.rect(self.screen,color_dark,[width/2-180,(height/2)+(height/4),140,40])  
        # superimposing the text onto our button 
            self.screen.blit(quit , (width/2+40,height/2+(height/4)))
            self.screen.blit(play,(width/2+-140,height/2+(height/4)))
        #adding title
            self.screen.blit(space,(width/2-140, height/2-250))
            self.screen.blit(invaders,(width/2-200, height/2-175))
        #adding alien images point values
            self.screen.blit(equals_400,(width/2, height/2+130))
            self.screen.blit(equals_200,(width/2, height/2+40))
            self.screen.blit(equals_100,(width/2, height/2-40))
        #adding alien images
            self.screen.blit(aliengreen,(width/2-160,height/2+125))
            self.screen.blit(alienblue,(width/2-165, height/2-50))
            self.screen.blit(alienteal,(width/2-160, height/2+30))
        # updates the frames of the game 
            pg.display.update() 
        

    def reset(self):
        print('Resetting game...')
        self.lasers.reset()
        self.ship.reset()
        self.aliens.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed

            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.aliens.update()
            self.lasers.update()
            self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    all_fonts=pg.font.get_fonts()
    print(all_fonts)
    g.game_intro()



if __name__ == '__main__':
    main()
