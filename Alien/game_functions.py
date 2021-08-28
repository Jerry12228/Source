import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep


# ------------------------- Response keyboard start -------------------------#
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """Response keyboard"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = True
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = True

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = False
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Run game when player click Play Button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.initialize_dynamic_settings()

        # Make cur hide
        pygame.mouse.set_visible(False)

        # Reset game statistics msg
        stats.reset_stats()
        stats.game_active = True

        # Reset score board img
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Clear alien and bullet list
        aliens.empty()
        bullets.empty()

        # Create a new group of aliens
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Response keydown"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        # Create a new bullet and add it into bullet group (if you have)
        # if len(bullets) < ai_settings.bullets_allowed:
        #     new_bullet = Bullet(ai_settings, screen, ship)
        #     bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Response keyup"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """If the limit is not reached, fire the bullet"""
    # Create a new bullet and add it into bullet group (if you have)
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# ------------------------- Response keyboard end -------------------------#


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on screen and switch to new screen"""
    # Redraw screen when every loop
    screen.fill(ai_settings.bg_color)
    # Draw all Bullets behind ship and alien
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # alien.blitme()
    aliens.draw(screen)

    # Show score
    sb.show_score()

    # Create Play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullet and del bullets which disappear"""
    # Create a bullet
    bullets.update()

    # Delete the bullet which disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))  # Print the num of bullets

    # Delete bullet which hit alien also delete this alien
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # if len(aliens) == 0:
    #     #Del all bullets on screen and create new aliens group
    #     bullets.empty()
    #     create_fleet(ai_settings, screen, ship, aliens)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Response bullet hit alien"""
    # Delete bullet which hit alien also delete this alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        stats.score += ai_settings.alien_points
        sb.prep_score()

    if len(aliens) == 0:
        # Del all bullets on screen
        bullets.empty()
        # Speed up
        ai_settings.increase_speed()
        # Level up
        stats.level += 1
        sb.prep_level()
        # Create a new aliens group
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculate how many aliens can be held in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_alien_row(ai_settings, ship_height, alien_height):
    """Calculate how many rows can screen held"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create a alien and add it in this row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create Aliens Group"""
    # Create a Alien and calculate how many aliens can be held in a row
    # The space between aliens is width of aliens
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_alien_row(ai_settings, ship.rect.height, alien.rect.height)
    # available_space_x = ai_settings.screen_width - 2 * alien_width
    # number_aliens_x = int(available_space_x / (2 * alien_width))

    # Create first line Aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            # Create a alien and add it into this line
            # alien = Alien(ai_settings, screen)
            # alien.x = alien_width + 2 * alien_width * alien_number
            # alien.rect.x = alien.x
            # aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """Take steps when alien touch edges"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Moving up and change direction (Alien)"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Response alien hit the ship"""
    if stats.ships_left > 0:
        # ships_left -1
        stats.ships_left -= 1

        # Update score board
        sb.prep_ships()

        # Empty alien and bullet group
        aliens.empty()
        bullets.empty()

        # Create new group of aliens and put ship ai mid bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # stop
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check alien touch bottom of screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check edge (Alien) and Update all aliens' position"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Check hit between ship and aliens
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Check alien touch bottom of screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check highest score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
