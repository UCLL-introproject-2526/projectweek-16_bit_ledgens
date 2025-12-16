import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 90

# Schermgrootte
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mijn Pygame Project")

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
bg_speed = 5  # langzamer = verder weg
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

    pygame.display.update()

pygame.quit()
