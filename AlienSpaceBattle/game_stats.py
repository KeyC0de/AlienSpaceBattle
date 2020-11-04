from configobj import ConfigObj


config = ConfigObj('conf.ini')

class GameStats():
    """ Tracks game statistics """
    
    def __init__(self, options):
        """ Initialize statistics class """
        
        self.settings = options
        self.resetStats()
        self.gameActive = False # start game in an inactive state
        self.highscore = int(config['highscore'])    # must never be reset

    def resetStats(self):
        """ Initialize statistics """
        
        self.shipsLeft = self.settings.lives
        self.score = 0
        self.level = 1