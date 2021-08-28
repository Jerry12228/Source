class Settings:
    """Save all Settings in this game"""

    def __init__(self):
        """Initialize game Static State Settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet Settings
        # self.bullet_speed_factor = 3
        # self.bullet_width = 3  # Official width
        self.bullet_width = 1200  # Text width
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # Alien Settings
        # self.alien_speed_factor = 10
        self.fleet_drop_speed = 10
        # self.fleet_direction = 1  # 1: right  -1: left

        # Speed up rate
        # self.speedup_scale = 2  # For test
        self.speedup_scale = 1.1  # For Official
        # Speed of points up
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings which change with game running"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1  # 1: right  -1: left

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Setting speed up and score"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.speedup_scale)
        print(self.alien_points)
