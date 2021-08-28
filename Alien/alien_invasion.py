import sys
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


def run_game():
    # Initialization pygame, settings and create a Screen Object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create a Button
    play_button = Button(ai_settings, screen, "Play")
    # Create a example to save game Information
    stats = GameStats(ai_settings)
    # Create a scoreboard
    sb = Scoreboard(ai_settings, screen, stats)
    # Create a Ship on screen
    ship = Ship(ai_settings, screen)
    # Create a group to save bullets
    bullets = Group()
    # Create a group to save aliens
    aliens = Group()

    # Create a Aliens group
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start game's main loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            ship.update()  # Create a ship
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

        # alien = Alien(ai_settings, screen)  # Create a alien

        # bullets.update()
        # Delete the bullet which disappeared
        # for bullet in bullets.copy():
        #     if bullet.rect.bottom <= 0:
        #         bullets.remove(bullet)
        # print(len(bullets))  # Print the num of bullets

        # Check mouse and keyboard events
        # for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        sys.exit()

        # Redraw screen when every loop
        # screen.fill(ai_settings.bg_color)
        # ship.blitme()

        # Make recently drawn screen visible
        # pygame.display.flip()


run_game()
