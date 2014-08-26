""" main.py
    Executes and controls the game
    User will control a spaceship with the arrow keys to attempt to absorb a star on the map.
    If the user collides with an enemy, the game is lost.

    Graham Rounds
    4/28/2014
"""

#Initialize  
import pygame, random, entities, math, scoreboard
pygame.init()

def main():
    ###=================
    ### Global Variables
    ###-----------------
    ### Change these how you see fit
    ###=================
    #window options
    game_title = "Space!"
    window_width = 800
    window_height = 600
    scoreboard_height = 50
    bg_color = (0,0,0) #black
    #neutral options
    spawn_time = 5 #seconds
    neutral_min_size = 5
    neutral_max_size = 15
    #enemy options
    enemy_grow_time = 15 #seconds
    enemy_min_size = 25
    enemy_max_size = 55

    #Display
    screen = pygame.display.set_mode((window_width, window_height))
    score = scoreboard.Scoreboard(screen, scoreboard_height)
    paused = scoreboard.Overlay("Paused", screen, scoreboard_height)
    gameOver = scoreboard.Overlay("Game Over", screen, scoreboard_height)
    pygame.display.set_caption(game_title)

    #Background
    background = pygame.Surface(screen.get_size())
    background.fill(bg_color) #black
    screen.blit(background, (0,0))

    #Entities
    numNeutrals = int((screen.get_width() * (screen.get_height()-scoreboard_height) / 30000)) #calculate number of neutrals
    numEnemies = int(math.floor(numNeutrals/3)) #number of enemies
    user = entities.User(screen, scoreboard_height)
    neutrals = []
    enemies = []
    #fill the arrays
    for i in range(numNeutrals):
        neutral = entities.Neutral(screen, scoreboard_height, random.randint(neutral_min_size,neutral_max_size))
        neutrals.append(neutral)
    for i in range(numEnemies):
        enemy =  entities.Enemy(screen, scoreboard_height, random.randint(enemy_min_size, enemy_max_size))
        enemies.append(enemy)   
    

    #put entities in groups
    userGroup = pygame.sprite.Group(user)
    enemyGroup = pygame.sprite.Group(enemies)
    neutralGroup = pygame.sprite.Group(neutrals)

    #timers
    SPAWN = (pygame.USEREVENT + 1)
    pygame.time.set_timer(SPAWN, 1000*spawn_time)
    ENEMYGROW = (pygame.USEREVENT + 2)
    pygame.time.set_timer(ENEMYGROW, 1000*enemy_grow_time)
    
    #Action
        #Assign
    keepGoing = True
    clock = pygame.time.Clock()
    keys = (False, False, False, False)
    # K_LEFT , K_RIGHT , K_UP , K_DOWN
    
        #Loop
    while keepGoing:
        #Time
        clock.tick(30)
        
        #If game is LOST (Lives == 0)
        if gameOver.getStatus():
            gameOver.showOverlay()
            pygame.display.flip()

            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN):
                        gameOver.toggle()
                        screen.blit(background, (0,0)) #clear the whole screen
                        
        #If game is PAUSED
        elif paused.getStatus():
            paused.showOverlay()
            pygame.display.flip()
            
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE):
                        paused.toggle()
                        screen.blit(background, (0,0)) #clear the whole screen
                        
        #If game is RUNNING
        else:
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False

                if event.type == SPAWN:
                	#Spawn New Neutrals
                    if (len(neutralGroup) < numNeutrals):
                        numNewNeutrals = random.randint(0, (numNeutrals-len(neutralGroup)) )
                        for i in range(numNewNeutrals):
                            neutral = entities.Neutral(screen, scoreboard_height, random.randint(neutral_min_size, neutral_max_size))
                            neutralGroup.add(neutral)
                    #Spawn New Enemies
                    if (len(enemyGroup) < numEnemies):
                    	numNewEnemies = random.randint(0, (numEnemies-len(enemyGroup)) )
                    	for i in range(numNewEnemies):
                    		enemy = entities.Enemy(screen, scoreboard_height, random.randint(enemy_min_size, enemy_max_size))
                    		enemyGroup.add(enemy)
                    		
                if event.type == ENEMYGROW:
                    for enemy in enemyGroup:
                        enemy.grow()

                #these values are stored while the key is held down
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT):
                        keys = (True, keys[1], keys[2], keys[3]) #rotating left
                    elif (event.key == pygame.K_RIGHT):
                        keys = (keys[0], True, keys[2], keys[3]) #rotating right
                    elif (event.key == pygame.K_UP):
                        keys = (keys[0], keys[1], True, keys[3]) #accelerating
                    elif (event.key == pygame.K_DOWN):
                        keys = (keys[0], keys[1], keys[2], True) #decellerating
                    elif (event.key == pygame.K_SPACE):
                        paused.toggle()
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT):
                        keys = (False, keys[1], keys[2], keys[3]) #rotating left
                    elif (event.key == pygame.K_RIGHT):
                        keys = (keys[0], False, keys[2], keys[3]) #rotating right
                    elif (event.key == pygame.K_UP):
                        keys = (keys[0], keys[1], False, keys[3]) #accelerating
                    elif (event.key == pygame.K_DOWN):
                        keys = (keys[0], keys[1], keys[2], False) #decellerating
                    
            #act upon what keys are held down
            if (keys[0]): #K_LEFT
                user.turnLeft()
            if (keys[1]): #K_RIGHT
                user.turnRight()
            if (keys[2]): #K_UP
                user.accelerate()
            if (keys[3]): #K_DOWN
                user.deccelerate()

            #collisions
            enemyCollide = pygame.sprite.spritecollide(user,enemyGroup, True)
            for enemy in enemyCollide:
                ruok = score.die()
                if (ruok == -1):
                    gameOver.toggle()
                user.play_sound()
            neutralCollide = pygame.sprite.spritecollide(user, neutralGroup, True)
            for neutral in neutralCollide:
                neutral.play_sound()
                score.increaseScore((10/neutral.getSize())+25)
                
            #Refresh gameArea 
            neutralGroup.clear(screen, background)
            userGroup.clear(screen, background)
            enemyGroup.clear(screen, background)
            
            neutralGroup.update(screen, background)
            userGroup.update(screen)
            enemyGroup.update(screen)
		        
            neutralGroup.draw(screen)
            userGroup.draw(screen)
            enemyGroup.draw(screen)
            
            #update scoreboard
            score.drawInfo()
        
            pygame.display.flip()
        	
    pygame.quit()
        
if __name__ == "__main__":
    main()
