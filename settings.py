from pygame import image


class Settings:
    """Store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's STATIC settings."""
        # Screen settings
        self.screen_width = 640
        self.screen_height = 640
        self.bg_color = (49, 48, 102)
        self.bg_image = image.load('sprites/bg_galaxy_blue.bmp')
        # ship settings
        self.ships_limit = 3

        # bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (120, 60, 60)
        self.bullets_allowed = 3

        # alien settings
        self.fleet_drop_speed = 10

        # Alien speed factor lvl up
        self.speedup_scale = 1.5
        # how quickli the alien points values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings that change during the game, so it can be reset """
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 2
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        self.alien_points = 10
        

    def increase_speed(self):
        """ Increase speed settings. """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
