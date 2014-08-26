""" overlays.py
    Stores the scores and information about the game
    Also displays notifications and displays to the user
    
    5/5/2014
    Graham Rounds
"""

#Initialize
import pygame

""" Class Overlay
    Generic Overlay Class which displays a pygame sprite at a designated location on the screen
    The sprite is the width of the screen and includes the text provided.
"""
class Overlay(pygame.sprite.Sprite):

    def __init__(self, text, screen, centery=-1, height=50):
        pygame.sprite.Sprite.__init__(self)

        ###=================
        ### Global Variables
        ###-----------------
        ### Change these how you see fit
        ###=================
        self.textSize = 20
        self.bgColor = (100, 100, 100) #grey
        self.txtColor = (255, 255, 255) #white

        ###class variables, you probably shouldn't change these
        self.screen = screen
        self.height = height
        self.width = screen.get_width()
        self.font = pygame.font.SysFont('arial', self.textSize, True)
        self.text = text

        #create rect object for background
        self.topy = (centery - self.height/2)
        if (self.topy < 0):
            self.topy = 0
        self.rect = pygame.Rect(0, self.topy, self.width, self.height)

    """ draw()
        draw's the overlay.
        passing true - will draw text
        passing false - will not draw text
    """
    def draw(self, drawText=True):
        #Draw background first
        self.screen.fill(self.bgColor, self.rect)
        
        if drawText:
            #render images of text
            self.textImage = self.font.render(self.text, True, self.txtColor)
            xpos = int(self.width/2 - self.textImage.get_width()/2) #horizontal center
            ypos = int(self.screen.get_height()/2 - self.textSize/2) #vertical center
            self.screen.blit(self.textImage, (xpos,ypos))

""" Class ToggleOverlay
    Subclass of Overlay. Functions the same way but is toggle-able
"""
class ToggleOverlay(Overlay):

    def __init__ (self, text, screen, height=50, status=False):
        self.centery = screen.get_height()/2
        super(ToggleOverlay, self).__init__(text, screen, self.centery, height)

        #class variables
        self.status = status

    #toggle status method
    def toggle(self):
        self.status = not self.status

    #return status method
    def getStatus(self):
        return self.status

""" Class Scoreboard
    Subclass of Overlay. Displays at top of screen and has multiple text objects.
    Also handles score and lives of the User
"""
class Scoreboard(Overlay):
    def __init__ (self, screen, height):
        super(Scoreboard, self).__init__("scoreboard", screen, 0, height)

        #class variables
        self.score = 0
        self.lives = 5

    """ draw()
        draw's the overlay.
        overrides Overlay class because we have multiple text objects to draw
    """
    def draw(self):
        super(Scoreboard, self).draw(False)
        #format text
        self.scoreText = "Score: " + str(self.score)
        self.livesText = "Lives: " + str(self.lives)
        #render images of score
        self.scoreImage = self.font.render(self.scoreText, True, self.txtColor)
        self.livesImage = self.font.render(self.livesText, True, self.txtColor)
        
        ##Draw on screen!
        ypos = int(self.height/2 - self.textSize/2) #vertical center
        scorePos = int(self.width*0.25 - self.scoreImage.get_width()/2) #horizontal center
        livesPos = int(self.width*0.75 - self.scoreImage.get_width()/2) #horizontal center
        self.screen.blit(self.scoreImage, (scorePos, ypos))
        self.screen.blit(self.livesImage, (livesPos, ypos))

    """ increaseScore()
        increases score by a number of points
    """
    def increaseScore(self, points):
    	self.score += points

    """ die()
        decreases lives by 1
        returns -1 if there are no lives left
    """
    def die(self):
    	self.lives -= 1
    	if (self.lives == 0):
    		return -1 #you lose!
    	else:
    		return 0 #no error
    	    
    """ reset()
        resets the class variables
    """
    def reset(self):
        self.lives = 5
        self.score = 0

""" Class Instructions
    Generic Overlay Class which displays instructions on how to play the game
    Instructions are loaded as a sprite on screen.
"""
class Instructions(pygame.sprite.Sprite):

    def __init__ (self, screen, position, scoreboard_height):
        self.instructions = pygame.image.load("instructions.png")
        #class variables
        self.yminimum = scoreboard_height
        self.status = True
        self.screen = screen

        #scale on smaller screens
        if (screen.get_width() < 1000):
            self.width = (screen.get_width()/2)
            self.height = int(self.width*0.487)
            self.instructions = pygame.transform.smoothscale(self.instructions, (self.width,self.height))

        self.rect = self.instructions.get_rect()
        
        #initialize position
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        #boundary checks
        if (self.rect.right > self.screen.get_width()): #too far right
            self.rect.right = self.screen.get_width()
        elif (self.rect.left < 0): #too far left
            self.rect.left = 0
            
        #boundary checks
        if (self.rect.bottom > self.screen.get_height()): #too far down
            self.rect.top = self.yminimum
        elif (self.rect.top < self.yminimum): #too far up
            self.rect.bottom = self.screen.get_height()
            
    def draw(self):
        self.screen.blit(self.instructions ,(self.rect.left, self.rect.top))
        
    #toggle status method
    def toggle(self):
        self.status = not self.status

    #return status method
    def getStatus(self):
        return self.status
