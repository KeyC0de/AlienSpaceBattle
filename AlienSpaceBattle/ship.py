import pygame
from pygame.sprite import  Sprite


class Ship(Sprite):
	# This class manages most of the player's ship behavior
	
	def __init__( self, options, screen ):
		"""Initialize ship and set its starting position."""

		super( Ship, self ).__init__()

		self.screen = screen	# draw ship at the screen surface supplied
		self.settings = options

		self.time = None		# cooldown timer after being hit - Initially Off
		self.lostPoints = 100
		self.bhit = False
		
		# load ship image and get its rect
		self.image = pygame.image.load('images/ship_nobg.png').convert_alpha() # returns a surface representing a ship
		self.rect = self.image.get_rect()       # treating an image as a rectangle is efficient
		self.screenRect = screen.get_rect()
		
		# start each new ship at the bottom center of the screen
		# set image's rect equal to the image's rect on the window
		self.rect.centerx = self.screenRect.centerx
		self.rect.bottom = self.screenRect.bottom
		
		# ship current position
		self.x = float( self.rect.centerx )
		self.y = float( self.rect.centery )
		
		# movement flag
		self.movingRight = False
		self.movingLeft = False
		self.movingUp = False
		self.movingDown = False


	def draw( self ):
		""" Draws ship at its current location """
		
		self.screen.blit( self.image, self.rect )


	def center( self ):
		""" Centers the ship on the screen """
		  
		self.rect.x = self.x
		self.rect.bottom = self.screenRect.bottom