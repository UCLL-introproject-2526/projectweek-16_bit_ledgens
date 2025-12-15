import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Schermgrootte
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mijn Pygame Project")

bg = pygame.image.load("backg.png").convert_alpha()
bg_width = bg.get_width()


# define game variables
scroll = 0
tiles = math.ceil(WIDTH / bg_width ) + 1

running = True
while running:

    # Beperk framerate
    clock.tick(FPS)

    #draw scrolling background
    for i in range(0,tiles):
        screen.blit(bg, (i * bg_width + scroll ,0))

    scroll -= 5

    #reset scroll
    if abs(scroll) > bg_width:
        scroll= 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic hier


    # Teken hier alles


    # Update scherm
    pygame.display.update()

# Pygame afsluiten
pygame.quit()

