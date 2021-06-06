import sys
import pygame
from bullet import Bullet
from spaceships import Alien
from time import sleep


def check_keydown_events(event, ai_setings, screen, stats,sb, ship, bullets):
    """Respond to keypressed."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_setings, screen, ship)
        bullets.add(new_bullet)
    if event.key == pygame.K_q:
        save_score(stats, sb)
        sys.exit()


def check_keyup_event(event, ship):
    """Respond on releasing key"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
def save_score(stats,sb):
    try:
        with open(sb.high_score_file, 'w') as file:
            file.write(str(stats.high_score))
    except FileNotFoundError as e:
        print(e)

def check_events(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(stats, sb)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen,stats,sb, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        
        #reset the scoreboard image
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    bullets.update()
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    colission = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level +=1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
    if colission:
        for aliens in colission.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_scores(stats, sb)


def check_high_scores(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and slip to the new screen."""
    screen.blit(ai_settings.bg_image, (0,0))

    # redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_aliens_y(ai_settings, alien_height):
    available_space_y = ai_settings.screen_height - (2 * alien_height)
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


def get_number_rows(ai_setings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on screen."""
    available_space_y = ai_setings.screen_height - (3 * alien_height) - ship_height
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien adn find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #update score board
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien-ship colisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen,sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen,sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen,sb, ship, aliens, bullets):
    """Check if any alien have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            print("Aliens hit the bottom")
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens):
    """Respond apropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleets direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1
