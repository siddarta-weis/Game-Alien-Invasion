import pygame
from pygame.sprite import Sprite

class MainShip(Sprite):
    def __init__(self, ai_settings, screen, ship_size=(64,64)) -> None:
        """ Initialize the ship and set its starting position. """
        super(MainShip, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #load the ship image and get its react.
        self.image = pygame.image.load('sprites/main_ship.bmp')
        self.image = pygame.transform.scale(self.image, ship_size)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
    
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        self.center = float(self.rect.centerx)
        

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the shipt at its current location """
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """ Update the ship's position bases on movement flags """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        self.rect.centerx = self.center
    def center_ship(self):
        """ Centern the ship on the screen. """
        self.center = self.screen_rect.centerx


class Alien(Sprite):
    """ A class to represent a single alien in the fleet """
    def __init__(self, ai_settings, screen) -> None:
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Load the alien image and set its rect atribute.
        self.image = pygame.image.load('sprites/alien_ship.bmp')
        self.image = pygame.transform.scale(self.image, (46, 46))
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        available_space_x = ai_settings.screen_width - (2 * self.rect.y)
        
        number_aliens_x = available_space_x / (2 * self.rect.y)
        

        #store the alien`s exact position.
        self.x = float(self.rect.x)

    def update(self):
        """ Move the alien right or left. """
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        """ Return True if alien in at edge of screen. """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blitme(self):
        """ Draw the alien at its current location. """
        self.screen.blit(self.image, self.rect)
    