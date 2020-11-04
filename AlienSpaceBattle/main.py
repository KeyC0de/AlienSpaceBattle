import pygame
from settings import Settings   # make an instance of Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

#clock = pygame.time.Clock()
#fps = 300

#from kivy.app import App
#from kivy.uix.button import Label

#class AlienShipBattle(App):

#def build(self):
#    self.startGame()
#    #return Label()

#@staticmethod
def startGame():

    # initialize
    pygame.init()
    # configure settings
    settings = Settings("Alien Invasion")
    # setup window / screen
    screen = settings.screen
    # make a ship
    ship = Ship(settings, screen)
    # make a group (list-like data structure) of bullets
    bullets = Group()
    # make a group of aliens
    aliens = Group()
    # create the fleet of aliens
    gf.createAlienFleet(settings, screen, ship, aliens)
    # make a missile
    missiles = Group()
    # make a group of stars - non interactable environment elements
    stars = Group()
    # create stars
    gf.createStars(settings, screen, stars)
    # create an instance to store game statistics
    stats = GameStats(settings)
    # create instance to store game statistics and create a scoreboard
    sb = Scoreboard(settings, screen, stats)
    # buttons
    playButton = Button(settings, screen, "Play!")

    """ Game Loop """
    while True:
        gf.checkForEvents(settings, screen, ship, aliens, bullets, missiles, playButton, stats, sb)
        if stats.gameActive == True:
            gf.updateShip(stats, ship, sb)
            gf.updateStars(settings, screen, stars)
            gf.updateBullets(aliens, bullets, settings, screen, ship, stats, sb)
            gf.updateMissiles(aliens, missiles, settings, screen, ship, stats, sb)
            gf.updateAliens(settings, stats, screen, ship, aliens, bullets, missiles, sb)
        gf.render(settings, screen, ship, aliens, bullets, missiles, stars, stats, playButton, sb)

        #clock.tick(fps)

# Time to play the game
if __name__ == '__main__':
    #AlienShipBattle().run()
    startGame()