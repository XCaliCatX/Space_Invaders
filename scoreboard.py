import pygame as pg 
from fileinput import FileInput
# import pygame.font

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.high_score_label_rect = None
        self.high_score_label_image = None
        self.score_label_rect = None
        self.score_label_image = None

        self.get_high_score()
        self.prep_score()
        

    def increment_score(self, score_multi): 
        self.score += (self.settings.alien_points * score_multi)
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        high_score_str = str(self.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,self.settings.bg_color)
        high_score_label_str = "High Score: "
        self.high_score_label_image = self.font.render(high_score_label_str, True, self.text_color, self.settings.bg_color)
        score_label_str = "Score: "
        self.score_label_image = self.font.render(score_label_str, True, self.text_color, self.settings.bg_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right -900
        self.high_score_rect.top = 20
        self.high_score_label_rect = self.high_score_image.get_rect()
        self.high_score_label_rect.right = self.screen_rect.right -1100
        self.high_score_label_rect.top = 20
        self.score_label_rect = self.high_score_image.get_rect()
        self.score_label_rect.right = self.score_rect.left - 20
        self.score_label_rect.top = 20
        

    def reset(self): 
        self.add_high_score()
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        if self.score>self.high_score:
            self.high_score = self.score
        self.add_high_score()
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.high_score_label_image,self.high_score_label_rect)
        self.screen.blit(self.score_label_image,self.score_label_rect)
    def get_high_score(self):
        with open('high_score.txt','r+') as file:
            old_high_score = file.read()
            file.seek(0)
            if int(old_high_score)> self.high_score:
                self.high_score = int(old_high_score)
    def add_high_score(self):
        with open('high_score.txt', 'r+') as file:
            old_high_score = file.read()
            if int(old_high_score)< self.high_score:
                file.seek(0)
                file.write(str(self.high_score))
                file.truncate()


        