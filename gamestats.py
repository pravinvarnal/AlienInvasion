class GameStats:
    """ Manage statistics for Alien Invasion """

    def __init__(self,ai_game):
        """Initialize statistics"""
        self.game_active = True
        self.settings = ai_game.settings
        self.reset_stats()
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit