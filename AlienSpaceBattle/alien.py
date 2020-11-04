import pygame
from pygame.sprite import Sprite
from random import randint, seed

class Alien(Sprite):
    """ A class to represent a single alien in the fleet. """
    
    def __init__(self, options, screen):
        """ Initialize the alien and set its starting position. """
        
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = options
        
        alienImgLocations = ["images/alien_green.png", "images/alien_purple.png", 
                             "images/alien_grey.png",  "images/alien_orange.png"]
        seed()
        
        # load alien image and set its rectangle
        self.image = pygame.image.load(alienImgLocations[randint(0,3)]).convert_alpha()
        self.destroyedImage = pygame.image.load("images/destroyed_alien.png").convert_alpha()   # use that when alien is hit
        self.rect = self.image.get_rect()
        
        # start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # store alien's exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.direction = 1  # alien direction: [1 = right], [-1 = left]
        
        self.time = None    # self destruct timer after being hit - Initially Off
    
    
    def updateAlienPosition(self):
        """ Update alien's position - left or right """
        
        # move alien right
        self.x += (self.settings.alienSpeedFactor * self.direction)
        self.rect.x = self.x
    
    def update(self):
        """ wrapper inherited from Sprite parent """
        self.updateAlienPosition()
    
    def changeDirection(self, options):
        """ If an alien reaches the bounds of the 
        window it should change direction """
        
        self.rect.y += options.alienDropSpeed
        
        self.direction *= -1
    
    def blitme(self):
        """ Draw alien at its current locaiton """
    
        self.screen.blit(self.image, self.rect)
    
    def checkIfBottomIsReached(self):
        """ Return true if alien is at edge of the screen """
        
        screenRect = self.screen.get_rect()
        if (self.rect.right >= screenRect.right):
            return True
        elif (self.rect.left <= 0):
            return True
    


