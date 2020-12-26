import pygame
import random
from pygame import mixer

# Initialyze the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
player_icon = pygame.image.load("player.png")
pygame.display.set_icon(player_icon)
playerX = 370
playerY = 480
playerX_change = 0

# Ennemy
ennemy_icon = []
ennemyX = []
ennemyY = []
ennemyX_change = []
ennemyY_change = []
num_of_ennemies = 6
for i in range(num_of_ennemies):
    ennemy_icon.append(pygame.image.load("ennemy.png"))
    ennemyX.append(random.randint(0,735))
    ennemyY.append(random.randint(50,150))
    ennemyX_change.append(3)
    ennemyY_change.append(40)

#Bullet
#Ready - You can't see the bullet on the screen
#Fire - The bullet is on the screen
bullet_icon = pygame.image.load("bullet.png")
pygame.display.set_icon(player_icon)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10


def show_score(x,y):
    score = font.render("Score :"+ str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_font = pygame.font.Font("freesansbold.ttf", 64)
    over_text = font.render(f"GAME OVER - Score of {score_value}.", True, (255,255,255))
    screen.blit(over_text, (200, 250))
def player(x,y):
    # Blit = draw on screem
    screen.blit(player_icon,(x,y))
def ennemy(x,y,i):
    # Blit = draw on screem
    screen.blit(ennemy_icon[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_icon,(x+16, y+10))

def collision(ennemyX,ennemyY,bulletX,bulletY):
    distance = ((ennemyX-bulletX)**2+(ennemyY-bulletY)**2)**0.5
    if distance < 27:
        return True
    else:
        return False

#Game loop
running = True
while running:
    screen.fill((50, 55, 55))
    # Background Image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # chekc if key pressed (Down= appuyer, UP = relache)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_ennemies):

        if ennemyY[i] > 440:
            for j in range(num_of_ennemies):
                ennemyY[j] = 2000
            game_over_text()
            break
        ennemyX[i] += ennemyX_change[i]

        if ennemyX[i] <= 0:
            ennemyX_change[i] = 3
            ennemyY[i] += ennemyY_change[i]

        elif ennemyX[i] >= 736:
            ennemyX_change[i] = -3
            ennemyY[i] += ennemyY_change[i]

        collision_ = collision(ennemyX[i], ennemyY[i], bulletX, bulletY)
        if collision_:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            ennemyX[i] = random.randint(0, 735)
            ennemyY[i] = random.randint(50, 150)
        ennemy(ennemyX[i],ennemyY[i],i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()