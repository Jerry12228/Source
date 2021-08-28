import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize Ship and Set initializing position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Loading Ship image and get circumscribed rectangle
        self.image = pygame.image.load('images/ship_57×112.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Make every new ship at mid bottom on screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Save float value in attribute Center of ship
        self.center = float(self.rect.centerx)

        # Move sign
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """According to the move sign change position of ship"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect with self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Drawing Ship at appoint position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Make ship at mid of screen"""
        self.center = self.screen_rect.centerx
