import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 90



# Schermgrootte
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mijn Pygame Project")

grond = pygame.Rect(0, 750, 1500, 550)
speler = pygame.Rect(100, 500, 40, 40)
obstakels = [
    pygame.Rect(WIDTH + 200, grond.top - 40, 30, 40),
    pygame.Rect(WIDTH + 600, grond.top - 60, 40, 60),
    pygame.Rect(WIDTH + 1000, grond.top - 30, 20, 30)
]

zwaartekracht = 1
snelheid_y = 0
# Achtergrond laden en schalen (verder weg)
bg = pygame.image.load("bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (int(WIDTH * 1.2), int(HEIGHT * 1.2)))
bg_width = bg.get_width()

bg.set_alpha(180)  # verder weg-effect

# Overlay voor diepte
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(40)
overlay.fill((0, 0, 0))

# Game variables
scroll = 0
bg_speed = 3  # langzamer = verder weg
tiles = math.ceil(WIDTH / bg_width) + 2

running = True
while running:
    clock.tick(FPS)

    # Achtergrond tekenen (parallax)
    for i in range(tiles):
        screen.blit(
            bg,
            (i * bg_width + scroll - 100, -50)
        )

    scroll -= bg_speed

    if abs(scroll) > bg_width:
        scroll = 0

    # Overlay opnieuw tekenen
    screen.blit(overlay, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and speler.bottom == grond.top:
        snelheid_y = -15

    # Speler beweging
    snelheid_y += zwaartekracht
    speler.y += snelheid_y

    if speler.colliderect(grond):
        speler.bottom = grond.top
        snelheid_y = 0

    # Obstakel beweging
    for obstakel in obstakels:
        obstakel.x -= 6
        if obstakel.right < 0:
            obstakel.x = WIDTH + 300

    # Botsing = dood
    for obstakel in obstakels:
        if speler.colliderect(obstakel):
            print("Game Over")
            running = False
        
    pygame.draw.rect(screen, (100, 200, 100), grond)
    pygame.draw.rect(screen, (255, 255, 0), speler)
    for obstakel in obstakels:
        pygame.draw.rect(screen, (200, 50, 50), obstakel)

    pygame.display.update()

pygame.quit()
