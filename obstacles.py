import pygame
from settings import *

def create_obstacles(ground, start_x):
    sequence = [
        ("ground", "bag"),
        ("air", "ruler"),
        ("ground", "desk"),
        ("air", "ruler")
    ]

    obstacles = []

    for i, (kind, img) in enumerate(sequence):
        x = start_x + i * OBSTACLE_DISTANCE

        if kind == "air":
            x += AIR_EXTRA_X
            rect = pygame.Rect(
                x,
                AIR_TOP_OFFSET,
                60,
                ground.top - AIR_GAP
            )
        else:
            if img == "bag":
                rect = pygame.Rect(x, ground.top - 70, 70, 70)
            else:
                rect = pygame.Rect(x, ground.top - 60, 60, 60)

        obstacles.append({"rect": rect, "img": img, "passed": False})

    return obstacles

def update_obstacles(obstacles):
    for i, obs in enumerate(obstacles):
        obs["rect"].x -= OBSTACLE_SPEED
        if obs["rect"].right < 0:
            obs["rect"].x = WIDTH + i * OBSTACLE_DISTANCE
            obs["passed"] = False  # ⭐ reset voor score