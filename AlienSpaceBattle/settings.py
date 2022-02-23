import pygame


class Settings():
	""" A class to store all settings for the game """
	
	def __init__(self, title):
		"""Initialize the game's settings."""
		
		# window screen settings
		pygame.display.set_caption(title)        
		self.screenWidth = 1140
		self.screenHeight = 900
		self.screenSize = self.screenWidth, self.screenHeight
		self.screen = pygame.display.set_mode(self.screenSize)
		self.bgColor = (30, 30, 30)
		self.bgImage = pygame.image.load("images/space_background.png").convert_alpha()
		self.bgImage = pygame.transform.scale(self.bgImage, (self.screenSize))
		
		# ship settings
		self.lives = 3
		
		# bullet settings
		self.bulletWidth = 6
		self.bulletHeight = 14
		self.bulletColor = (180, 90, 130)
		self.maxBulletsAllowed = 3
		
		# missile settings
		self.maxMissilesAllowed = 1
		
		# star settings
		self.starSpeedFactor = 1

		# scoring settings
		self.alienPoints = 10
		
		# audio 
		self.music = pygame.mixer.Sound('sounds/bg_romariogrande__alien-dream.ogg')
		self.fireMissileSFX = pygame.mixer.Sound('sounds/fire_missile.ogg')
		self.missileHitSFX = pygame.mixer.Sound('sounds/missile_hit.wav')
		self.missileHitSFX.set_volume(0.1)
		self.fireLaserBulletSFX = pygame.mixer.Sound('sounds/laser_bullet.wav')
		self.fireLaserBulletImpactSFX = pygame.mixer.Sound('sounds/laser_impact.ogg')

		'''dynamic settings: 
		Initialize settings that change throughout the course of the game'''
		self.shipSpeedFactor = .6
		self.alienSpeedFactor = .2
		self.bulletSpeedFactor = 1

		# general settings
		self.speedupMultiplier = 1.1


	def increaseSpeed(self):
		self.shipSpeedFactor *= self.speedupMultiplier
		self.alienSpeedFactor *= self.speedupMultiplier
		self.bulletSpeedFactor *= self.speedupMultiplier
		self.missileSpeedFactor *= self.speedupMultiplier
		self.alienDropSpeed *= self.speedupMultiplier

	def reset(self):
		self.shipSpeedFactor = .6
		self.alienSpeedFactor = .2
		self.bulletSpeedFactor = 1
		self.missileSpeedFactor = .6
		self.alienDropSpeed = 60