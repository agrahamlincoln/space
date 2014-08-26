""" main.py
    Executes and controls the game
    User will control a spaceship with the arrow keys to attempt to absorb a star on the map.
    If the user collides with an enemy, the game is lost.

    Graham Rounds
    4/28/2014
"""

#Initialize  
import pygame, random, entities, math, overlays
pygame.init()

def main():
    ###=================
    ### Global Variables
    ###-----------------
    ### Change these how you see fit
    ###=================
    #window options
    game_title = "Space!"
    window_width = 1280
    window_height = 720
    scoreboard_height = 50
    bg_color = (0,0,0) #black
    #neutral options
    spawn_time = 5 #seconds
    neutral_min_size = 5
    neutral_max_size = 15
    #enemy options
    enemy_grow_time = 1 #seconds
    enemy_min_size = 25
    enemy_max_size = 55

    #Display
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(game_title)

    #Interface objects
    score = overlays.Scoreboard(screen, scoreboard_height)
    paused = overlays.ToggleOverlay("Paused", screen, scoreboard_height)
    gameOver = overlays.ToggleOverlay("Game Over", screen, scoreboard_height)
    newGame = overlays.ToggleOverlay("Welcome to Space!", screen, scoreboard_height)
    newGame.toggle() #set initial status to true
    instructions = overlays.Instructions(screen, (int(screen.get_width()*0.75), int(screen.get_height()*0.75)), scoreboard_height)

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
        enemy = entities.Enemy(screen, scoreboard_height, random.randint(enemy_min_size, enemy_max_size))
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
        
        #If the game is NEW
        if newGame.getStatus():
            #re-draw everything
            screen.blit(background, (0,0)) #clear the whole screen
            
            #first the sprites
            neutralGroup.draw(screen)
            userGroup.draw(screen)
            enemyGroup.draw(screen)

            #then the overlays
            newGame.draw()
            instructions.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN):
                        newGame.toggle() #begin game
                        keys = (False, False, False, False) #reset the movement keys
                        screen.blit(background, (0,0)) #clear the whole screen
                        
            
        #If game is LOST (Lives == 0)
        elif gameOver.getStatus():
            #re-draw everything
            screen.blit(background, (0,0)) #clear the whole screen
            
            #first the sprites
            neutralGroup.draw(screen)
            userGroup.draw(screen)
            enemyGroup.draw(screen)

            #then the overlays
            gameOver.draw()
            instructions.draw()
            score.draw()
            
            pygame.display.flip()

            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN):
                        gameOver.toggle()
                        newGame.toggle()
                        screen.blit(background, (0,0)) #clear the whole screen
                        
                        #reset score
                        score.reset()
                        
                        #reset groups
                        user.initialize()
                        enemyGroup.empty()
                        enemyGroup.add(enemies)
                        neutralGroup.empty()
                        neutralGroup.add(neutrals)

                        #reset neutrals
                        for neutral in neutrals:
                            if (neutral.getStatus() == False):
                                neutral.toggle()
                            neutral.resize( random.randint(neutral_min_size, neutral_max_size) )
                            neutral.setRandPos()

                        #reset enemies
                        for enemy in enemies:
                            if (enemy.getStatus() == False):
                                enemy.toggle()
                            enemy.resize( random.randint(enemy_min_size, enemy_max_size) )
                            enemy.setRandPos()
                        
        #If game is PAUSED
        elif paused.getStatus():
            #re-draw everything
            screen.blit(background, (0,0)) #clear the whole screen
            
            #first the sprites
            neutralGroup.draw(screen)
            userGroup.draw(screen)
            enemyGroup.draw(screen)

            #then the overlays 
            paused.draw()
            instructions.draw()
            score.draw()
            pygame.display.flip()
            
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE):
                        paused.toggle()
                        keys = (False, False, False, False) #reset the movement keys
                        screen.blit(background, (0,0)) #clear the whole screen
                    if (event.key == pygame.K_RETURN):
                        newGame.toggle()
                        keys = (False, False, False, False) #reset the movement keys
                        screen.blit(background, (0,0)) #clear the whole screen
                        
        #If game is RUNNING
        else:
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False

                if event.type == SPAWN:
                    for neutral in neutrals:
                        if (neutral.getStatus() == False):
                            #2 in 3 shot to be re-used
                            if (random.randint(1,3) > 1):
                                neutral.toggle()
                                neutral.resize( random.randint(neutral_min_size, neutral_max_size) )
                                neutral.setRandPos()
                                neutralGroup.add(neutral)
                    for enemy in enemies:
                        if (enemy.getStatus() == False):
                            #2 in 3 shot to be re-used
                            if (random.randint(1,3) > 1):
                                enemy.toggle()
                                enemy.setRandPos()
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
                enemy.toggle()
                ruok = score.die()
                if (ruok == -1):
                    gameOver.toggle()
                user.play_sound()
            neutralCollide = pygame.sprite.spritecollide(user, neutralGroup, True)
            for neutral in neutralCollide:
                neutral.toggle()
                neutral.play_sound()
                score.increaseScore((25/neutral.getSize())+25)
                
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
            score.draw()
        
            pygame.display.flip()
        	
    pygame.quit()
        
if __name__ == "__main__":
    main()
