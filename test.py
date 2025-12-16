import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 90

# Schermgrootte
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game")

# Grond Rect (voor botsing)
grond = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Speler Rect op de grond starten
speler = pygame.Rect(100, grond.top - 160, 160, 160)

# Obstakels
obstakels = [
    pygame.Rect(WIDTH + 200, grond.top - 40, 30, 40),
    pygame.Rect(WIDTH + 600, grond.top - 60, 40, 60),
    pygame.Rect(WIDTH + 1000, grond.top - 30, 20, 30)
]

# Zwaartekracht
zwaartekracht = 1
snelheid_y = 0

# Achtergrond laden en schalen
bg = pygame.image.load("bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (int(WIDTH * 1.2), int(HEIGHT * 1.2)))
bg_width = bg.get_width()
bg.set_alpha(180)

# Grond afbeelding
grond_img = pygame.image.load("ground.png").convert_alpha()
grond_img = pygame.transform.scale(grond_img, (WIDTH, 50))

# Speler afbeelding
speler_img = pygame.image.load("karakter.png").convert_alpha()
speler_img = pygame.transform.scale(speler_img, (160, 160))

# Overlay voor diepte
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(40)
overlay.fill((0, 0, 0))

# Game variables
scroll = 0
bg_speed = 3
tiles = math.ceil(WIDTH / bg_width) + 2

grond_x = 0
grond_speed = 6

running = True
while running:
    clock.tick(FPS)

    # Achtergrond tekenen (parallax)
    for i in range(tiles):
        screen.blit(bg, (i * bg_width + scroll - 100, -50))

    scroll -= bg_speed
    if abs(scroll) > bg_width:
        scroll = 0

    # Overlay tekenen
    screen.blit(overlay, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Speler springen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and speler.bottom == grond.top:
        snelheid_y = -20

    # Speler beweging
    snelheid_y += zwaartekracht
    speler.y += snelheid_y

    if speler.colliderect(grond):
        speler.bottom = grond.top
        snelheid_y = 0

    # Obstakels bewegen
    for obstakel in obstakels:
        obstakel.x -= 6
        if obstakel.right < 0:
            obstakel.x = WIDTH + 300

    # Botsing check
    for obstakel in obstakels:
        if speler.colliderect(obstakel):
            print("Game Over")
            running = False

    # Grond scrollen
    grond_x -= grond_speed
    if grond_x <= -WIDTH:
        grond_x = 0

    # Grond tekenen
    screen.blit(grond_img, (grond_x, HEIGHT - 50))
    screen.blit(grond_img, (grond_x + WIDTH, HEIGHT - 50))

    # Speler tekenen met afbeelding
    screen.blit(speler_img, (speler.x, speler.y))

    # Obstakels tekenen
    for obstakel in obstakels:
        pygame.draw.rect(screen, (200, 50, 50), obstakel)

    pygame.display.update()

pygame.quit()
