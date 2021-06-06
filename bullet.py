import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship) -> None:
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        self.image_file = 'sprites/shoot.bmp'
        self.image = pygame.image.load(self.image_file)
        self.image = pygame.transform.scale(self.image, (15,35))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    def update(self):
        """ Move the bullet up the screen. """
        #update the decimal position of the bullet.
        self.y -= self.speed_factor
        self.rect.y = self.y
    def draw_bullet(self):
        """ Draw the bullet to the screen """
        self.screen.blit(self.image, self.rect)
        
