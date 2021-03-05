import pygame
import random
import math

from pygame import mixer

pygame.init()

# Create Window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Explosion
explosionImg = pygame.image.load('Explosion.png')
explosionX = 50
explosionY = 50

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)
mixer.music.set_volume(.1)

# stuff i don't know what to call
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 395
playerY = 531
playerspeed = 2
playerX_changeL = 0
playerX_changeR = 0
playerY_changeU = 0
playerY_changeD = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 1

# Bullet
# Ready - You can't see the bullet
# Fire - The bullet is moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('Stay and Shine.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('PKMN-Mystery-Dungeon.ttf', 128)


# Functions

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def Explosion(x, y):
    screen.blit(explosionImg, (explosionX, explosionY))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def createEnemy():
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 739))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


for i in range(num_of_enemies):
    createEnemy()

# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((37, 0, 60))
    # background Image
    screen.blit(background, (0, 0))

    # Movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_changeL = -playerspeed

            if event.key == pygame.K_RIGHT:
                playerX_changeR = playerspeed

            if event.key == pygame.K_UP:
                playerY_changeU = -playerspeed

            if event.key == pygame.K_DOWN:
                playerY_changeD = playerspeed

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bulletY = playerY

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_changeL = 0

            if event.key == pygame.K_RIGHT:
                playerX_changeR = 0

            if event.key == pygame.K_UP:
                playerY_changeU = 0

            if event.key == pygame.K_DOWN:
                playerY_changeD = 0

    # Checking for boundaries of spaceship so it doesn't go out of the screen
    playerX += playerX_changeL + playerX_changeR
    playerY += playerY_changeD + playerY_changeU

    if playerX <= -4:
        playerX = -4
    elif playerX >= 740:
        playerX = 740
    if playerY <= 360.6000000000076:
        playerY = 360.6000000000076
    elif playerY >= 531:
        playerY = 531

    # Enemy Max

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 740:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:

            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(.25)
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 739)
            enemyY[i] = random.randint(50, 150)
            if num_of_enemies < 6:
                createEnemy()
                num_of_enemies += 1

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

    player(playerX, playerY)
    Explosion(explosionX, explosionY)
    show_score(textX, textY)
    pygame.display.update()
