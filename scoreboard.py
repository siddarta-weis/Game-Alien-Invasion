from os import error
import pygame.font
from pygame.sprite import Group
from spaceships import MainShip

class Scoreboard():
    """ A calsss to report scoring information. """
    def __init__(self, ai_settings, screen, stats) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_setting = ai_settings
        self.high_score_file = 'high_score.txt'
        self.stats = stats
        try:
            with open(self.high_score_file) as file:
                self.stats.high_score = int(file.readline())
        except FileNotFoundError as e:
            self.stats.high_score = 10
            print(e)
            
        
            
        #Font setting for scoring information.
        self.text_color = (30,255,30)
        self.font = pygame.font.SysFont(None, 28)

        #Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """ Turn the score into a rendered image """
        rounded_score = int(round(self.stats.score, -1))
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        #Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
            """ Turn the high score into a rendered image. """
            high_score = int(round(self.stats.high_score))
            high_score_str = f"High Score: {high_score:,}"
            self.high_score_image = self.font.render(high_score_str, True, self.text_color)
            self.high_score_rect = self.high_score_image.get_rect()
            self.high_score_rect.centerx = self.screen_rect.centerx
            self.high_score_rect.top = self.score_rect.top 

    def show_score(self):
        """ Draw score to the screen """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
    
    def prep_level(self):
        """ Turn the level into a rendered image. """
        #position the level belo the score
        self.lvl = str(self.stats.level)
        self.level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(self.level_str, True, self.text_color)

        #Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ Show how many ships are left. """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = MainShip(self.ai_setting, self.screen, (32,32))
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
