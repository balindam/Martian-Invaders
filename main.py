import pygame
import random
import math

from pygame import mixer

# initializing pygame
pygame.init()
# creating the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("./images/background.png")

# background sound
mixer.music.load("./sounds/background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Martian Invaders")
icon = pygame.image.load("./images/icon.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("./images/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("./images/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
# ready - you cant see the bullet on the screen
# fire - the bullet is currently moving on the screen

bulletImg = pygame.image.load("./images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10


# game over display
gameOver_font = pygame.font.Font("freesansbold.ttf", 64)


def gameOverDisplay():
    gameOver_text = gameOver_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOver_text, (200, 250))


# function to show the score
def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# draw the player
def playerDraw(x, y):
    screen.blit(playerImg, (x, y))


# draw the enemy
def enemyDraw(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 16))


# checking for the condition of bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # filling the background
    screen.fill((0, 0, 0))
    # inserting background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke actions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("./sounds/laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # movement of the player
    playerX += playerX_change

    # checking for the boundaries of spaceship for out of bound
    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(no_of_enemies):

        # game over condition
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 1000
            gameOverDisplay()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision checking
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("./sounds/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemyDraw(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerDraw(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()

