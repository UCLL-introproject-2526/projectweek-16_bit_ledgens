# import pygame
# from pygame.display import flip
# import os

# # Initialiseer Pygame
# pygame.init()

# # Achtergrond laden
# script_dir = os.path.dirname(__file__)
# image_path = os.path.join(script_dir, "achtergrond", "bos.png")
# achtergrond = pygame.image.load(image_path)
# achtergrond = pygame.transform.scale(achtergrond, (1024, 768))

# # Scherm
# WIDTH, HEIGHT = 1024, 768
# surface = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Interactieve Cirkel")

# # Clock
# clock = pygame.time.Clock()
# FPS = 60

# # Cirkel eigenschappen
# x = 60
# y = 600        # start op de grond
# radius = 40
# x_velocity = 5
# y_velocity = 0
# gravity = 0.5
# jump_strength = -12
# ground_y = 600  # grondniveau

# # Functie om achtergrond te tekenen
# def clear_surface(surface):
#     surface.blit(achtergrond, (0, 0))

# # Functie om één frame te renderen
# def render_frame(surface, x, y):
#     clear_surface(surface)
#     pygame.draw.circle(surface, (255, 0, 0), (int(x), int(y)), radius)
#     flip()

# # Main loop
# running = True
# while running:
#     keys = pygame.key.get_pressed()  # huidige toetsstatus

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Links/rechts beweging
#     if keys[pygame.K_LEFT]:
#         x -= x_velocity
#     if keys[pygame.K_RIGHT]:
#         x += x_velocity

#     # Springen
#     if keys[pygame.K_SPACE] and y >= ground_y:
#         y_velocity = jump_strength

#     # Pas positie aan door snelheid
#     y += y_velocity
#     y_velocity += gravity

#     # Zorg dat de cirkel niet onder de grond gaat
#     if y > ground_y:
#         y = ground_y
#         y_velocity = 0

#     render_frame(surface, x, y)
#     clock.tick(FPS)

# pygame.quit()

import pygame
import random

# Pygame initialiseren
pygame.init()

# Scherminstellingen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kaasje Jungle Runner")
clock = pygame.time.Clock()
FPS = 60

# Kleuren
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Kaasje
BROWN = (139, 69, 19)   # Platforms
RED = (255, 0, 0)       # Obstakels
ORANGE = (255, 165, 0)  # Kaasjes
GREEN = (34, 139, 34)   # Jungle details

# Speler instellingen
player_size = 50
player_x = 100
player_y = HEIGHT - 300
velocity_y = 0
gravity = 1
jump_power = 20
jumping = False

# Platform instellingen
platforms = []
platform_width = 200
platform_height = 20
floor_speed = 5

# Startplatform
platforms.append(pygame.Rect(0, HEIGHT - 150, platform_width, platform_height))

# Obstakels en kaasjes
obstacles = []
obstacle_timer = 0
obstacle_interval = 1500
obstacle_size = 50

cheeses = []
cheese_timer = 0
cheese_interval = 2000
cheese_size = 30

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Game loop
running = True
while running:
    dt = clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                velocity_y = -jump_power
                jumping = True

    # Speler beweging
    velocity_y += gravity
    player_y += velocity_y
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Platforms scrollen en nieuwe genereren
    for platform in platforms[:]:
        platform.x -= floor_speed
        pygame.draw.rect(screen, BROWN, platform)
        # Collision speler-platform
        if player_rect.colliderect(platform) and velocity_y > 0 and player_y + player_size <= platform.y + velocity_y:
            player_y = platform.y - player_size
            velocity_y = 0
            jumping = False
        # Verwijder platform als het uit beeld is
        if platform.right < 0:
            platforms.remove(platform)

    # Nieuwe platforms toevoegen
    if len(platforms) == 0 or platforms[-1].right < WIDTH:
        last_platform_y = HEIGHT - 150 - random.randint(0, 100)
        platforms.append(pygame.Rect(WIDTH, last_platform_y, platform_width, platform_height))

    # Obstakels genereren en bewegen
    obstacle_timer += dt
    if obstacle_timer > obstacle_interval:
        obstacle_y = platforms[-1].y - obstacle_size
        obstacles.append(pygame.Rect(WIDTH, obstacle_y, obstacle_size, obstacle_size))
        obstacle_timer = 0

    for obstacle in obstacles[:]:
        obstacle.x -= floor_speed
        pygame.draw.rect(screen, RED, obstacle)
        if player_rect.colliderect(obstacle):
            print("Game Over! Score:", score)
            running = False
        if obstacle.right < 0:
            obstacles.remove(obstacle)

    # Kaasjes genereren en bewegen
    cheese_timer += dt
    if cheese_timer > cheese_interval:
        cheese_y = platforms[-1].y - cheese_size - random.randint(0, 50)
        cheeses.append(pygame.Rect(WIDTH, cheese_y, cheese_size, cheese_size))
        cheese_timer = 0

    for cheese in cheeses[:]:
        cheese.x -= floor_speed
        pygame.draw.rect(screen, ORANGE, cheese)
        if player_rect.colliderect(cheese):
            score += 1
            cheeses.remove(cheese)
        elif cheese.right < 0:
            cheeses.remove(cheese)

    # Speler tekenen
    pygame.draw.rect(screen, YELLOW, player_rect)

    # Jungle details (optioneel)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 150, WIDTH, 10))

    # Score tekenen
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()




