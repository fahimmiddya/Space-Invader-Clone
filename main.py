# This is a 2-D arcade game based on the original space invader game.
import math
import random
import pygame
from pygame import mixer

# Initialise the pygame
pygame.init()
# Creating a blank screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load("background.png").convert_alpha()

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space-invaders.png').convert_alpha()
pygame.display.set_icon(icon)

# Player and giving it a position
playerImg = pygame.image.load('main.png')
playerX = 370
playerY = 480
playerX_change = 0  # Change in the coordinate when keys are pressed

# Enemy and giving it a position
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png').convert_alpha())
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet and giving it a position
# Ready = Bullet isnt seen on the screen
# Fire - Bullet is currently moving.
bulletImg = pygame.image.load('bullet.png').convert_alpha()
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

# User score and high score
score_value = 0
font = pygame.font.SysFont('consolas', 20)
textX = 10
textY = 10

# High score
high_score = 0
font_high = pygame.font.SysFont('consolas', 20)
highX = 650
highY = 10

# Game over
over_font = pygame.font.Font('retro.ttf', 64)
FPS = 120
clock = pygame.time.Clock()


# Displaying Score
def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 83, 73))
    screen.blit(score, (x, y))


# Displaying high score of the user
def show_high(x, y):
    hscore = font_high.render("High Score:" + str(high_score), True, (255, 83, 73))
    screen.blit(hscore, (x, y))


# Displaying fps of the game
def show_fps(FPS):
    fps = font_high.render("FPS:" + str(FPS), True, (255, 83, 73))
    screen.blit(fps, (360, 10))


# Displaying the game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 83, 73))
    screen.blit(over_text, (180, 250))


# Bullet function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, ((x + 16, y + 10)))


# Defining player and enemy function
def player(x, y):
    screen.blit(playerImg, (x, y))  # Drawing the player on the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Drawing the enemy on the screen


# Code for collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # Giving color to the screen
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # Only one bullet can be fired at a time.
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # Get the current x coordinate from the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Changing the coordinates when keys are pressed
    playerX += playerX_change
    # Creating boundary so that the player doesnt go out of the game
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            bullet_Sound = mixer.Sound("gameover.wav")
            bullet_Sound.play()
        enemyX[i] += enemyX_change[i]
        # Creating boundary so that the player doesnt go out of the game
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if score_value > high_score:
                high_score = score_value
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Calling the enemy
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling the player
    player(playerX, playerY)
    # Displaying the score
    show_score(textX, textY)
    # Displaying the high score
    show_high(highX, highY)
    # Displaying the FPS
    show_fps(FPS)
    # Add this line of code to update
    pygame.display.update()
