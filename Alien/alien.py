import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """Show one of aliens"""

    def __init__(self, ai_settings, screen):
        """Initialize alien and set Initial position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load image of alien and set rect attribute
        self.image = pygame.image.load('images/alien_60×33.bmp')
        self.rect = self.image.get_rect()

        # Make all aliens at left top of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Save alien's precise position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien at appoint position"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien touch edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move right or left (Alien)"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
