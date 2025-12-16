import pygame
import math

from settings import *
from assets import load_assets
from player import Player
from obstacles import create_obstacles, update_obstacles

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teacher Run")
clock = pygame.time.Clock()

assets = load_assets()

ground = pygame.Rect(0, GROUND_Y, WIDTH, GROUND_HEIGHT)
player = Player(ground)
obstacles = create_obstacles(ground, WIDTH + 300)

bg = assets["bg"]
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(WIDTH / bg_width) + 2
ground_x = 0

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, ground)
    update_obstacles(obstacles)

    for obs in obstacles:
        if player.hitbox.colliderect(obs["rect"]):
            print("GESNAPT DOOR DE LEERKRACHT!")
            running = False

    scroll -= 3
    if abs(scroll) > bg_width:
        scroll = 0

    for i in range(tiles):
        screen.blit(bg, (i * bg_width + scroll - 100, -100))

    ground_x -= OBSTACLE_SPEED
    if ground_x <= -WIDTH:
        ground_x = 0

    screen.blit(assets["ground"], (ground_x, ground.top))
    screen.blit(assets["ground"], (ground_x + WIDTH, ground.top))

    player.draw(screen, assets["player"])

    for obs in obstacles:
        if obs["img"] == "bag":
            screen.blit(assets["bag"], obs["rect"])
        elif obs["img"] == "desk":
            screen.blit(assets["desk"], obs["rect"])
        else:
            bottom = obs["rect"].bottom
            screen.blit(
                assets["ruler"],
                (obs["rect"].x, bottom - assets["ruler"].get_height())
            )

    pygame.display.update()

pygame.quit()

