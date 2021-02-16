class Settings:
    """ A Class to store all settings for Alien Invasion project"""

    def __init__(self):
        """Initialize the games settings"""

        #Screen Settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230,230,230)

        #Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (235, 76, 52)
        self.bullets_allowed = 5

        #Alien Settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 20
        self.fleet_direction = 1
