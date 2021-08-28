import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """Control ship shoot class"""
    def __init__(self, ai_settings, screen, ship):
        """Create a Bullet at position of ship"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a rect to show Bullet at (0,0) and set right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Save Bullets' position which show with float
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move bullet up"""
        # Update float value which express bullet's position
        self.y -= self.speed_factor
        # Update rect position which express bullet
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw a bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
