import pygame
import sys

pygame.init()

# Venster
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run Game")

clock = pygame.time.Clock()
FPS = 25

# Speler
player_x = 100
player_vel = 5

base_y = HEIGHT - 220
player_y = base_y

# Sprite sheet laden
sprite_sheet = pygame.image.load("persoon3.PNG").convert_alpha()

# Sprite sheet info
NUM_FRAMES = 3
sheet_width, sheet_height = sprite_sheet.get_size()
FRAME_WIDTH = sheet_width // NUM_FRAMES
FRAME_HEIGHT = sheet_height

# Frames knippen + schalen
frames = []
for i in range(NUM_FRAMES):
    frame = sprite_sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (80, 200))
    frames.append(frame)

# Animatie
frame_index = 0
animation_speed = 0.2

# Hupje per frame (pas waarden aan)
frame_y_offsets = [0, 8, 2]   # experiment: [0, 8, 0] of [0, 5, 0]

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Beweging
    player_x += player_vel
    if player_x > WIDTH:
        player_x = -80

    # Animatie + hupje per frame
    frame_index += animation_speed
    if frame_index >= NUM_FRAMES:
        frame_index = 0

    idx = int(frame_index)
    current_frame = frames[idx]
    player_y = base_y - frame_y_offsets[idx]

    # Tekenen
    WIN.fill((255, 255, 255))
    WIN.blit(current_frame, (player_x, player_y))
    pygame.display.update()

pygame.quit()
sys.exit()
