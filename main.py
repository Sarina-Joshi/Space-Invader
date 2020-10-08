import pygame
import random
import math
from pygame import mixer

# Initializing Pygame
pygame.init()

# Adding Background
background = pygame.image.load('space.jpg')

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Creating screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('arcade.png')
playerX = 370
playerY = 480
player_xchange = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_xchange = []
enemy_ychange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemy_xchange.append(2)
    enemy_ychange.append(30)

    # Bullet
    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bullet_xchange = 0
    bullet_ychange = 5
    bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 65)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text,(200,250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # red, green, blue(R, G, B)
    screen.fill((10, 20, 30))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_xchange = -3
            if event.key == pygame.K_RIGHT:
                player_xchange = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            player_xchange = 0

    playerX += player_xchange

    # Adding boundaries to the player
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
            
            break
            ()
        enemyX[i] += enemy_xchange[i]
        if enemyX[i] <= 0:
            enemy_xchange[i] = 2
            enemyY[i] += enemy_ychange[i]
        elif enemyX[i] >= 736:
            enemy_xchange[i] = -2
            enemyY[i] += enemy_ychange[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_ychange

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
