class GameStats:
    """Count game Information"""
    def __init__(self, ai_settings):
        """Initialize game Information"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Settings inactive stats at the beginning
        self.game_active = False

        # Highest score (Never Reset)
        self.high_score = 0

    def reset_stats(self):
        """Initialize game Information which
        may change when the game running"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
