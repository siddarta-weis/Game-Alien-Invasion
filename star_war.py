from bullet import Bullet
import sys
import pygame
from spaceships import MainShip
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    """initialize game and create a screen object."""
    pygame.init()
    pygame.display.set_caption("Alienigenas")

    ai_settings = Settings()
    stats = GameStats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    sb = Scoreboard(ai_settings, screen, stats)

    play_button = Button(ai_settings, screen, "Play")
    # Make a ship
    ship = MainShip(ai_settings, screen)

    # Make a group to store bullets in.
    bullets = Group()

    # Make a group of Aliens
    aliens = Group()

    #timer 
    clock = pygame.time.Clock()
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        clock.tick(60)
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

  
run_game()
