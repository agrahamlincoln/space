""" entities.py
    A class library of objects.
    Each entity is a seperate entity in the game
    There will be the USER, NEUTRAL, and ENEMY entities

    Graham Rounds
    4/28/2014
"""

import pygame, random, math

class Entity(pygame.sprite.Sprite):

    def __init__(self, screen, scoreboard_height):
        pygame.sprite.Sprite.__init__(self)
        self.heightSB = scoreboard_height
        self.image = pygame.Surface((50,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.rect.centery = random.randrange(self.heightSB, screen.get_height())
        
    """ loadImg(self, width, height)
        Loads an image from file, resizes to the size passed
        in the parameters.
        returns the image as a pygame surface object
    """
    def loadImg(self, img, width, height):
        userImg = pygame.image.load(img)
        userImg = pygame.transform.smoothscale(userImg, (width,height))
        return userImg

    """ rotateImg(self, baseImg, angle)
        rotates the image.
        you should pass in the original un-rotated image.
        This is so the image doesn't get distorted.
    """
    def rotateImg(self, baseImg, angle):
        #base img has angle of 90 degrees
        return pygame.transform.rotate(baseImg, angle-90)

#####
#  NEUTRAL
#####
class Neutral(Entity):
    """ makes a neutral entity with a random starting position
        the neutral entity can play an explosion sound
    """
        
    #load any external elements from file
    pygame.mixer.init(44100, 16, 1, 1024) #Initialize the mixer
    explosion = pygame.mixer.Sound("smallExplosion.ogg")
        
    def __init__(self, screen, scoreboard_height, size):
		
		#perform super methods
        super(Neutral, self).__init__(screen, scoreboard_height)
        self.baseImg = super(Neutral, self).loadImg("star.png",size,size)

        #store for later usage
        self.size = size
        self.image = self.baseImg
        self.rect = self.image.get_rect()

        #initialize position
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.rect.centery = random.randrange(scoreboard_height, screen.get_height())

    def play_sound(self):
        self.explosion.play()
        
    def getSize(self):
    	return self.size

#####
#  ENEMY
#####        
class Enemy(Entity):
    """ makes an enemy with a random starting position
        the enemy can grow
    """
        
    def __init__(self, screen, scoreboard_height, size):
    
    	#perform super methods
        super(Enemy, self).__init__(screen, scoreboard_height)
        self.baseImg = super(Enemy, self).loadImg("enemy.png",size,size)
        
        #store for future usage
        self.size = size
        self.image = self.baseImg
        self.rect = self.image.get_rect()

        #initialize position
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.rect.centery = random.randrange(self.heightSB, screen.get_height())


    """ grow(self)
        re-loads the image from file
        sizes up between 0 and 5 pixels on each width and height.
        We re-load the file to avoid image distortion on re-scaling
    """
    def grow(self):
        newSize = self.rect.width + random.randint(5,10)
        self.image = super(Enemy, self).loadImg("enemy.png", newSize, newSize)
        #store old position
        xpos = self.rect.centerx
        ypos = self.rect.centery
        self.rect = self.image.get_rect()
        #recover old position
        self.rect.centerx = xpos
        self.rect.centery = ypos
    
    def getSize(self):
    	return self.size	
        
#####
#  USER
#####        
class User(Entity):
    """ makes a spaceship sprite with vector-based movement
    """
    #load any external elements from file
    pygame.mixer.init(44100, 16, 1, 1024) #Initialize the mixer
    explosion = pygame.mixer.Sound("largeExplosion.ogg")
        
    def __init__(self, screen, scoreboard_height):
        super(User, self).__init__(screen, scoreboard_height)

        #load image
        self.baseImg = super(User, self).loadImg("spaceship.png",25,47)
        #we will use this baseImg later
        self.image = self.baseImg
        self.rect = self.image.get_rect()

        #initialize velocity, direction, and position
        self.rect.centerx = (screen.get_width()/2)
        self.rect.centery = ((screen.get_height()/2)+self.heightSB)
        self.velocity = 0
        self.direction = 90 #angle measure in degrees

    #accelerate increases velocity
    def accelerate(self):
        self.velocity += 0.25
        
    #deccelerate decreases velocity
    #deccelerate cannot go below 0
    def deccelerate(self):
        if (self.velocity > 0):
            self.velocity -= 1
        elif (self.velocity <0):
            self.velocity = 0
        
    """ turnRight()
        changes the direction (clockwise)
        rotates the sprite
        keeps the angle measure 0 <= direction <= 360
    """
    def turnRight(self):
        self.direction -= 5
        #keep anglemeasure in the period [0,360]
        if (self.direction < 0):
            self.direction += 360
        elif (self.direction > 360):
            self.direction -= 360
            
        #rotate sprite clockwise by 1 degree
        self.image = self.rotateImg(self.baseImg, self.direction)
        
        #store old position
        xpos = self.rect.centerx
        ypos = self.rect.centery
        self.rect = self.image.get_rect()
        #recover old position
        self.rect.centerx = xpos
        self.rect.centery = ypos
        
    """ turnLeft()
        changes the direction (counter-clockwise)
        rotates the sprite
        keeps the angle measure 0 <= direction <= 360
    """
    def turnLeft(self):
        self.direction += 5
        #keep anglemeasure in the period [0,360]
        if (self.direction < 0):
            self.direction += 360
        elif (self.direction > 360):
            self.direction -= 360
            
        #rotate sprite counter-clockwise by 1 degree
        self.image = self.rotateImg(self.baseImg, self.direction)

        #store old position
        xpos = self.rect.centerx
        ypos = self.rect.centery
        self.rect = self.image.get_rect()
        #recover old position
        self.rect.centerx = xpos
        self.rect.centery = ypos
        
    """ update(screen)
        updates the position of the user
        moves based off direction and velocity
        will not bounce off wall, will wrap to other side
    """
    def update(self, screen):
        #move left or right
        self.rect.centerx += self.velocity * math.cos(math.radians(self.direction))
        #boundary checks
        if (self.rect.right > screen.get_width()): #too far right
            self.rect.left = 0
        elif (self.rect.left < 0): #too far left
            self.rect.right = screen.get_width()

        #move up or down
        self.rect.centery -= self.velocity * math.sin(math.radians(self.direction))
        #boundary checks
        if (self.rect.bottom > screen.get_height()): #too far down
            self.rect.top = self.heightSB
        elif (self.rect.top < self.heightSB): #too far up
            self.rect.bottom = screen.get_height()

    def play_sound(self):
        self.explosion.play()
