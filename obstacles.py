import pygame
from settings import *
import random

GROUND_OBSTACLES = ["bag", "desk"]
AIR_OBSTACLES = ["ruler","lamp"]

MAX_AIR_IN_ROW = 1

def generate_sequence(length=4):
    sequence = []
    last_kind = None
    air_count = 0

    for _ in range(length):
        if last_kind == "air" and air_count >= MAX_AIR_IN_ROW:
            kind = "ground"
        else:
            kind = random.choice(["ground", "air"])

        if kind == "air":
            air_count += 1
        else:
            air_count = 0

        if kind == "ground":
            img = random.choice(GROUND_OBSTACLES)
        else:
            img = random.choice(AIR_OBSTACLES)

        sequence.append((kind, img))
        last_kind = kind

    return sequence


def create_obstacles(ground, start_x, length=4):
    sequence = generate_sequence(length)
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

        obstacles.append({
            "rect": rect,
            "img": img,
            "kind": kind,
            "passed": False
        })

    return obstacles

def update_obstacles(obstacles):
    for i, obs in enumerate(obstacles):
        obs["rect"].x -= OBSTACLE_SPEED
        if obs["rect"].right < 0:
            obs["rect"].x = WIDTH + i * OBSTACLE_DISTANCE
            obs["passed"] = False  # ⭐ reset voor score