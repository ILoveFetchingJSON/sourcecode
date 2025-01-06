import pygame # type: ignore
import time
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Wicked aliens')
background = pygame.image.load("background.png")
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (80, 80))
playerX = 360
playerY = 690
playerX_change = 0
playerRect = pygame.Rect(playerX, playerY, 50, 50)
enemy = pygame.image.load('alien-enemy.png')
enemyX = 50
enemyY = 50
enemyXVel = 0.1
enemyYVel = 50
enemy = pygame.transform.scale(enemy, (50, 50))
enemyRect = pygame.Rect(enemyX, enemyY, 50, 50)
paused = False
running = True

def background_display():
    screen.blit(background, (0, 0))

def player_display(x, y):
    screen.blit(player, (x, y))

def enemy_display(x, y):
    screen.blit(enemy, (x, y))

# Initialize font module and create a font object
pygame.font.init()
game_font = 'PressStart2P-Regular.ttf'
tip = pygame.font.Font(None, 36)  # None for default font, 36 is the size
def display_text(text, x, y):
    text_surface = tip.render(text, True, (255, 255, 255))  # White color
    screen.blit(text_surface, (x, y))

class Bullet:
    def __init__(self, bulletImg, bulletYVel, bulletSizeX, bulletSizeY, bulletX=360, bulletY=690):
        self.bulletImg = pygame.image.load(bulletImg)
        self.bulletYVel = bulletYVel
        self.bulletImg = pygame.transform.scale(self.bulletImg, (bulletSizeX, bulletSizeY))
        self.bulletX = bulletX
        self.bulletY = bulletY
        self.bulletRect = pygame.Rect(bulletX, bulletY, bulletSizeX, bulletSizeY)
        
    def display(self):
        screen.blit(self.bulletImg, (self.bulletRect.x, self.bulletY))
    
    def firebullet(self):
        self.bulletY += self.bulletYVel
        self.bulletRect.y = self.bulletY

bullets = []

# Create a semi-transparent overlay
overlay = pygame.Surface(screen.get_size()) 
overlay.set_alpha(128)  # Set transparency level (0-255); lower values mean more transparent
overlay.fill((0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            paused = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.1
            if event.key == pygame.K_d:
                playerX_change = 0.1
            if event.key == pygame.K_RETURN:
                bullet = Bullet('bullet.png', -0.5, 50, 50, playerX + 15, playerY - 10)
                bullets.append(bullet)
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggles pause state
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    while paused and running:  # Add 'and running' to ensure clean exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    playerX += playerX_change
        time.sleep(0.1)
        background_display()
        screen.blit(overlay, (0, 0))  # Apply the overlay when paused
        pygame.display.flip()
    if not running:
        break

    playerX += playerX_change

    background_display()

    player_display(playerX, playerY)
    
    
    for bullet in bullets:
        bullet.firebullet()
        bullet.display()
    
    bullets = [bullet for bullet in bullets if bullet.bulletY > 0]

    enemyX += enemyXVel
    if enemyX > 750 or enemyX < 0:
        enemyXVel = -enemyXVel
        enemyY += enemyYVel

    # Update the enemy rectangle's position
    enemyRect.topleft = (enemyX, enemyY)
    
    # Check for collisions with bullets
    for bullet in bullets:
        if enemyRect.colliderect(bullet.bulletRect):
            enemyX, enemyY = 50, 50
            enemyXVel += 0.03
            bullet.bulletYVel += 0.03
            bullets.remove(bullet)  # Remove bullet on collision (optional)
    if enemyRect.colliderect(playerRect):
        print("Game over!")
        running = False
    
    
    # Display your custom text
    display_text("Press ESC to temporarily pause the game.", 0, 764)
    enemy_display(enemyX, enemyY)
    pygame.display.flip()
