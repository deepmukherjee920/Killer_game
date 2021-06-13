import pygame
import random
import math
from pygame import mixer
#Initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((700,500))

#show the screen permanenetly
#while true:
    #pass

#change the background screen
background = pygame.image.load("background.png")

#Backgroung Sound
mixer.music.load("background.wav")
mixer.music.play(-1)


#Change the Title and Icon of screen
pygame.display.set_caption("Deep's Creation")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

#My Player spaceship.png(download from 'flaticon') and I have to set size for my player in screen.
playerImg = pygame.image.load("spaceship.png")
playerX = 310
playerY = 400
#signify the change that I want in X
playerX_change = 0

#code for enemy as well as playerX

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 3
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 636))
    enemyY.append(random.randint(50, 100))
    # signify the change that I want in X,Y
    enemyX_change.append(2)
    enemyY_change.append(40)


#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 400
bulletX_change = 4
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)    #style of display
textX = 10
testY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("CHOL BHAG", True, (255, 255, 255))
    screen.blit(over_text, (200,250))


#define the player
def player(x,y):
    #we use blit to draw on the screen
    screen.blit(playerImg, (x, y))


#This code is for enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))



def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+14, y+8))



#we want collision between bullet and enemy
#formula --> D = root((x2-x1)**2 + (y2-y1)**2)

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:                                    #27 means 27pixels
        return True
    else:
        return False


#But the while loop exceeds the screen means the cross button doesn't work. for that the process given below
#Game Loop
running = True
while running:

    # RGB = Red, Green, Blue and everone's value is (0 -> 255)  .. 0 means none and 255 means color active in screen
    # if there is all (0), that means screen color will not be changed
    screen.fill((0, 0, 0))

    #to show the background Image
    screen.blit(background, (0,0))

    #to move right, use (+) and to move left,use (-), for the playerX and use (+) to up and (-) for down for playerY
    #playerX -= 0.1


    # In this while loop,we can quit the game by using cross button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether it's right or left
        #Keydown is used to press any key on the keyboard..
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    #bullet sound
                    bullet_sound = mixer.Sound("bullet.wav")
                    bullet_sound.play()
                    #get the current X co_ordinate of this spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


            #Keyup is used to release the press
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    #add the change of playerX and checking for boundaries
    playerX += playerX_change
    # to stop player to go to out of the screen
    if playerX <= 0:
        playerX = 0
    # Here player size is 64. so I want to substract from 700
    elif playerX >= 636:
        playerX = 636


    # add the change of enemy and checking for boundaries
    #to understand the number of enemies
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        # to stop player to go to out of the screen
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            # to move down
            enemyY[i] += enemyY_change[i]
        # Here player size is 64. so I want to substract from 700
        elif enemyX[i] >= 636:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]


        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #collision sound
            bullet_sound = mixer.Sound("collision.wav")
            bullet_sound.play()
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 636)
            enemyY[i] = random.randint(50, 100)
        # call the enemy in while loop
        enemy(enemyX[i], enemyY[i], i)


    #bullet movement
    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    #call the player in while loop
    player(playerX, playerY)

    #To show the score
    show_score(textX,testY)




    #Update the screen like color change by using RGB values and when i put any value of any part of RGB,the screen color will change
    pygame.display.update()



