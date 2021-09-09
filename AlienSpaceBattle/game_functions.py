import pygame, sys
from bullet import Bullet
from alien import Alien
from missile import Missile
from star import Star
from random import randrange
from game_stats import config
from os import environ


y = 0   # for bg image update

def checkForEvents(options, screen, ship, aliens, bullets, missiles, playButton, stats, scoreboard):
    """ monitor input (keyboard and mouse) events """
    
    for event in pygame.event.get():
        
        # print(event) # check event - pygame's responce to our input
        
        # when window's X button is pressed
        if (event.type == pygame.QUIT):
            gameOver(stats)
        # check for button presses
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            isButtonClicked = playButton.rect.collidepoint(mouseX, mouseY)
            if isButtonClicked and stats.gameActive == False:
                startGame(stats, aliens, bullets, missiles, screen, ship, options, scoreboard)

        # when key is pressed
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_q):
                gameOver(stats)
            elif event.key == pygame.K_p and stats.gameActive == False:
                startGame(stats, aliens, bullets, missiles, screen, ship, options, scoreboard)
            elif (event.key == pygame.K_RIGHT):
                # move ship to the right by # of pixels as step
                ship.movingRight = True
            elif (event.key == pygame.K_LEFT):
                ship.movingLeft = True
            elif (event.key == pygame.K_UP):
                ship.movingUp = True
            elif (event.key == pygame.K_DOWN):
                ship.movingDown = True
            elif (event.key == pygame.K_SPACE):
                fireBullet(options, screen, ship, bullets)
            elif (event.key == pygame.K_RETURN):
                fireMissile(options, screen, ship, missiles)
        
        # when key is released
        elif (event.type == pygame.KEYUP):
            if (event.key == pygame.K_RIGHT):
                ship.movingRight = False
            elif (event.key == pygame.K_LEFT):
                ship.movingLeft = False
            elif (event.key == pygame.K_UP):
                ship.movingUp = False
            elif (event.key == pygame.K_DOWN):
                ship.movingDown = False


def startGame(stats, aliens, bullets, missiles, screen, ship, options, scoreboard):
    pygame.mouse.set_visible(False)
    stopBackgroundMusic(options)
    playBackgroundMusic(options)    # play background music
    stats.resetStats()
    missiles.empty()
    aliens.empty()
    bullets.empty()
    ship.centerShip()
    stats.gameActive = True
    options.resetDynamicSettings()
    scoreboard.prepScoreboard()
    createAlienFleet(options, screen, ship, aliens)

def gameOver(stats):
    stats.gameActive = False
    pygame.mouse.set_visible(True)
    print("Game Over")
    # write highscore to an .ini file
    config['highscore'] = stats.highscore
    config['name'] = environ.get('MYNAME')
    config.write()
    pygame.quit()
    sys.exit()

def updateBackgroundImage(options, screen):
    # (x = 0 - 20, y = 0 - 20) changing once per second
    global y
    inv_y = y % options.screenHeight 
    screen.blit(options.bgImage,(0,inv_y))
    screen.blit(options.bgImage,(0,inv_y - options.screenHeight))
    y -= 1


def render(options, screen, ship, aliens, bullets, missiles, stars, stats, playButton, scoreboard):
    """ Redraw screen during each pass through the loop """
    
    #screen.fill(options.bgColor)
    updateBackgroundImage(options, screen)
    
    # draw all game objects 
    for star in stars.sprites():
        star.drawStar()
    for bullet in bullets.sprites():
        bullet.drawBullet()
    ship.blitme()
    aliens.draw(screen)
    for missile in missiles:
        missile.drawMissile()

    # draw scoreboard
    scoreboard.displayScore()
    scoreboard.displayLevel()

    # draw buttons above all others
    if not stats.gameActive:
        playButton.drawButton()
    
    # make the most recently drawn screen visible (swap buffers)
    pygame.display.flip()



def fireBullet(options, screen, ship, bullets):
    """ player spaceship fires one bullet """ 
    
    # create a new bullet and add it to the bullets group
    if (len(bullets) < options.maxBulletsAllowed):
        newBullet = Bullet(options, screen, ship)
        bullets.add(newBullet)
        options.fireLaserBulletSFX.play()

def updateBullets(aliens, bullets, options, screen, ship, stats, scoreboard):
    """ Handles bullets and their interactions """
    
    bullets.update()  # auto-calls function for each bullet
    removeOldBullets(bullets, options)
    
    checkBulletAlienCollisions(aliens, bullets, options, screen, ship, stats, scoreboard)

def fireMissile(options, screen, ship, missiles):
    """ spaceship fires a missile (really big bullet) """
    
    if (len(missiles) < options.maxMissilesAllowed):
        newMissile = Missile(options, screen, ship)
        missiles.add(newMissile)
        options.fireMissileSFX.play()

def updateMissiles(aliens, missiles, options, screen, ship, stats, scoreboard):
    """ Handlers missiles and their interactions """
    
    for missile in missiles:
        missile.updateMissilePosition()
    removeOldMissiles(missiles)
    
    checkMissileAlienColliisions(aliens, missiles, options, screen, ship, stats, scoreboard)


def checkBulletAlienCollisions(aliens, bullets, options, screen, ship, stats, scoreboard):
    """ checks for any bullets that have hit aliens. If so get rid of them """
    #collisions = 
    crashed = pygame.sprite.groupcollide(bullets, aliens, True, False)
    
    if (len(crashed) != 0):
        options.fireLaserBulletImpactSFX.play()
        
        # alien that was hit has triggered the countdown timer. After .5s it will be destroyed
        for aliens in crashed.values():
            for alien in aliens:
                alien.image = alien.destroyedImage
                alien.time = pygame.time.get_ticks()
    
    # if all aliens are dead repopulate the fleet
    if (len(aliens) == 0):
        bullets.empty()
        bullets.empty()
        options.increaseSpeed()
        stats.level += 1
        scoreboard.prepLevel()
        createAlienFleet(options, screen, ship, aliens)

def checkMissileAlienColliisions(aliens, missiles, options, screen, ship, stats, scoreboard):
    crashed = pygame.sprite.groupcollide(missiles, aliens, False, True)
    
    if (len(crashed) != 0):
        options.missileHitSFX.play()
        howManyDead = len(crashed.values())
        stats.score = stats.score + (options.alienPoints * howManyDead)
        scoreboard.prepScore()
        checkHighScore(stats, scoreboard)
    
    # if all aliens are dead repopulate the fleet
    if (len(aliens) == 0):
        missiles.empty()
        createAlienFleet(options, screen, ship, aliens)

def checkHighScore(stats, scoreboard):
    """"Check for a new high score"""
    if stats.score > stats.highscore:
        stats.highscore = stats.score
        scoreboard.prepHighScore()

def removeOldBullets(bullets, options):
    """ Remove any bullets that go beyond window bounds """
    
    # we should loop over a *copy* of the group
    for bullet in bullets.copy():
        if (bullet.rect.bottom < 0 or bullet.rect.top > options.screenHeight):
            bullets.remove(bullet)
    #print(len(bullets)) # prints # of bullets currently on the screen
    
def removeOldMissiles(missiles):
    """ Remove any missiles that go beyond window bounds """
    
    for missile in missiles.copy():
        if (missile.rect.bottom < 0):
            missiles.remove(missile)
#

def getAlienRows(options, screen, ship):
    """ Determines the number of rows of aliens that fit on the screen."""
    
    # vertical spacing between each alien is equal to one alien width
    alien = Alien(options, screen)
    alienHeight = alien.rect.height
    shipHeight = ship.rect.height
    
    availableSpace_y = options.screenHeight - (2 * alienHeight) - shipHeight
    numberOfRows = int(availableSpace_y / (2 * alienHeight)) - 1 # experiment
    return numberOfRows


def getNumberOfAliens_x(options, screen):
    """ Determine the number of aliens that fit in a row. """
    """ [space] [alien1] [space] [alien2] [space] ... [alienN] [space] """
    
    # horizontal spacing between each alien is equal to one alien width
    alien = Alien(options, screen)
    alienWidth = alien.rect.width   # calc alien rect width
    
    availableSpace_x = options.screenWidth - 3 * alienWidth
    totalAliens_x = int(availableSpace_x / (2 * alienWidth))
    return totalAliens_x


def createAlien(options, screen, aliens, colNumber, rowNumber):
    """ create alien and place it in the row """
    
    alien = Alien(options, screen)
    alienWidth = alien.rect.width
    alien.x = alienWidth + 2 * alienWidth * colNumber   # calc alien position
    alien.rect.x = alien.x  # place alien @ appropriate position on the screen
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * rowNumber
    aliens.add(alien)


def createAlienFleet(options, screen, ship, aliens):
    """ create an entire fleet of aliens """
    
    alienCount_x = getNumberOfAliens_x(options, screen)
    alienCount_y = getAlienRows(options, screen, ship)
        
    # create the fleet of aliens
    for rowNum in range(alienCount_y):
        for colNum in range(alienCount_x):
            createAlien(options, screen, aliens, colNum, rowNum)
#
 
def updateAliens(options, stats, screen, ship, aliens, bullets, missiles, scoreboard):
    """ Update the positions of all aliens in the fleet """
    
    for alien in aliens.sprites():
        
        # check whether an alien has been hit. If so and its timer has passed then kill() it
        if alien.time is not None:
            if (pygame.time.get_ticks() - alien.time >= 500):
                stats.score += options.alienPoints
                scoreboard.prepScore()
                checkHighScore(stats, scoreboard)
                alien.kill()
        
        # check if a side wall / edge has been reached
        if (alien.checkIfBottomIsReached()):
            alien.changeDirection(options)
        alien.update()
    
    # look for alien-ship collisions

    if (pygame.sprite.spritecollideany(ship, aliens)):
        print("Ship hit!!!")
        shipHit(options, stats, screen, ship, aliens, bullets, missiles, scoreboard)
        return
    
    # look for aliens hitting the bottom of the screen
    checkIfAliensReachedBottom(options, stats, screen, ship, aliens, bullets, missiles)
#


def checkIfAliensReachedBottom(options, stats, screen, ship, aliens, bullets, missiles):
    """ Check if any aliens have reached the bottom of the screen. """
    
    screenRect = screen.get_rect()
    for alien in aliens.sprites():
        if (alien.rect.bottom >= screenRect.bottom):
            # treat this the same as if the ship got hit
            #shipHit(options, stats, screen, ship, aliens, bullets, missiles)
            gameOver(stats)   # game over
            break
#


def updateShip(stats, ship, scoreboard):
    """Update ship's position based on the movement flag's status."""

    # also careful not to go outside window bounds
    if (ship.movingRight and (ship.rect.right < ship.screenRect.right)):
        ship.x += ship.settings.shipSpeedFactor
    if (ship.movingLeft and (ship.rect.left)):
        ship.x -= ship.settings.shipSpeedFactor
    if (ship.movingUp and (ship.rect.top > ship.screenRect.top)):
        ship.y -= ship.settings.shipSpeedFactor
    if (ship.movingDown and (ship.rect.bottom < ship.screenRect.bottom)):
        ship.y += ship.settings.shipSpeedFactor

    ship.rect.centerx = ship.x
    ship.rect.centery = ship.y

    if ship.time is not None and ship.bhit == True and pygame.time.get_ticks() - ship.time >= 1000:
        ship.bhit = False
        stats.shipsLeft -= 1
        print(stats.shipsLeft)
        if (stats.shipsLeft < 0):
            gameOver(stats)
        stats.score -= ship.lostPoints
        scoreboard.prepScore()
        scoreboard.prepShips()


def shipHit(options, stats, screen, ship, aliens, bullets, missiles, scoreboard):
    """ respond to ship being hit by alien. """

    # start the timer
    if ship.bhit == False:
        ship.time = pygame.time.get_ticks()
        ship.bhit = True
    
    # empty the list of aliens and bullets
    #aliens.empty()
    #bullets.empty()
    #missiles.empty()
    
    # create a new fleet and center the ship
    #ship.centerShip()
    #createAlienFleet(options, screen, ship, aliens)
    
    # pause
    #sleep(.5)


def createStars(options, screen, stars):
    """ create a few stars and place them randomly on the screen """
    
    starCount = randrange(0, 16)
    while starCount > 0:
        star = Star(screen, options)
        stars.add(star)
        starCount -= 1


def updateStars(options, screen, stars):
    """ update position of all stars in the grid. """
    
    for star in stars.sprites():
        star.rect.y += options.starSpeedFactor
        
        # remove stars receding far down the screen
        for star in stars.copy():
            if star.rect.y >= options.screenHeight:
                stars.remove(star)
    
    if (len(stars) == 0):
        createStars(options, screen, stars)


def playBackgroundMusic(options):
    """ Play background music """ 
    
    options.music.play(10)

def stopBackgroundMusic(options):
    options.music.stop()