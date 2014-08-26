""" infoDisplay.py
    Stores the scores and information about the game
    Also displays notifications and displays to the user
    
    5/1/2014
    Graham Rounds
"""

#Inititalize
import pygame

""" stores the scoreboard as sprite so we can easily blit it on the screen"""
class Scoreboard(pygame.sprite.Sprite):

    def __init__(self, screen, height):
    
        pygame.sprite.Sprite.__init__(self)
        
        ###=================
        ### Global Variables
        ###-----------------
        ### Change these how you see fit
        ###=================
        self.score = 0
        self.lives = 5
        self.textSize = 24
        self.bgColor = (100, 100, 100) #grey
        self.txtColor = (255, 255, 255) #white
        
        ##class variables, you probably shouldnt change these
        self.height = height
        self.font = pygame.font.SysFont('Arial', self.textSize)
        self.width = screen.get_width()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.screen = screen
        
    """ drawInfo
        this method will format and draw all of the objects onto the screen
    """
    def drawInfo(self):
        #format text
        self.scoreText = "Score: " + str(self.score)
        self.livesText = "Lives: " + str(self.lives)
        #render images of score
        self.scoreImage = self.font.render(self.scoreText, True, self.txtColor)
        self.livesImage = self.font.render(self.livesText, True, self.txtColor)
        
        ##Draw on screen!
        self.screen.fill(self.bgColor, self.rect)
        self.screen.blit(self.scoreImage, ( int((self.screen.get_width()*0.25)), ((self.height-self.textSize)/2) ))
        self.screen.blit(self.livesImage, ( int((self.screen.get_width()*0.75)), ((self.height-self.textSize)/2) ))
        
    def increaseScore(self, points):
    	self.score += points
    	
    def die(self):
    	self.lives -= 1
    	if (self.lives == 0):
    		return -1 #you lose!
    	else:
    		return 0 #no error
    		
class Overlay(pygame.sprite.Sprite):
	
    def __init__(self, text, screen, height):
		
        pygame.sprite.Sprite.__init__(self)
		
	###=================
        ### Global Variables
        ###-----------------
        ### Change these how you see fit
        ###=================
        self.textSize = 20
        self.bgColor = (100, 100, 100) #grey
        self.txtColor = (255, 255, 255) #white
        
        ##class variables, you probably shouldnt change these
        self.status = False
        self.height = height
        self.font = pygame.font.SysFont('couriernew', self.textSize)
        self.width = screen.get_width()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.screen = screen
        self.pausedText = text
        self.image = self.font.render(self.pausedText, True, self.txtColor)
        
    def showOverlay(self):
        background = pygame.Surface((self.screen.get_width(), self.height))
        background.fill(self.bgColor) #grey
        self.screen.blit(background, (0, (int(self.screen.get_height()/2) - int(self.height/2))))
        self.screen.blit(self.image, ( int(self.screen.get_width()/2), (int(self.screen.get_height()/2) - int(self.textSize/2))))
        
    def toggle(self):
        if (self.status):
            self.status = False
        elif (self.status == False):
            self.status = True
        
    def getStatus(self):
        return self.status

class Instructions(pygame.sprite.Sprite):
	
    def __init__(self, text, screen, height):
		
        pygame.sprite.Sprite.__init__(self)
		
	###=================
        ### Global Variables
        ###-----------------
        ### Change these how you see fit
        ###=================
        self.textSize = 24
        self.bgColor = (100, 100, 100) #grey
        self.txtColor = (255, 255, 255) #white
        
        ##class variables, you probably shouldnt change these
        self.status = False
        self.height = height
        self.font = pygame.font.SysFont('Arial', self.textSize)
        self.width = screen.get_width()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.screen = screen
        self.pausedText = text
        self.image = self.font.render(self.pausedText, True, self.txtColor)
        
    def showOverlay(self):
        background = pygame.Surface((self.screen.get_width(), self.height))
        background.fill(self.bgColor) #black
        self.screen.blit(background, (0, (int(self.screen.get_height()/2) - int(self.height/2))))
        self.screen.blit(self.image, ( int(self.screen.get_width()/2), (int(self.screen.get_height()/2) - int(self.textSize/2))))
        
    def toggle(self):
        if (self.status):
            self.status = False
        elif (self.status == False):
            self.status = True
        
    def getStatus(self):
        return self.status
