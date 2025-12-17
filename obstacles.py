import pygame
from settings import *
import random

GROUND_OBSTACLES = ["bag", "desk"]
AIR_OBSTACLES = ["ruler", "lamp"]

MAX_AIR_IN_ROW = 1

# =====================
# HITBOX MARGINS PER OBSTAKEL
# =====================
HITBOX_MARGIN = {
    "lamp": 20,
    "ruler": 20,
    "desk": 10,
    "bag": 5
}


def generate_sequence(length=4):
    """Genereer een sequentie van obstakels met afwisseling van lucht/grond."""
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

        img = random.choice(GROUND_OBSTACLES if kind == "ground" else AIR_OBSTACLES)

        sequence.append((kind, img))
        last_kind = kind

    return sequence


def create_obstacles(ground_rect, x_start, assets):
    """Maak obstakels op basis van sequentie en assets."""
    sequence = generate_sequence(4)
    obstacles = []
    x = x_start

    for kind, obstacle_type in sequence:
        img = assets[obstacle_type]

        # =====================
        # LAMP (plafond)
        # =====================
        if obstacle_type == "lamp":
            rect = img.get_rect(midtop=(x, 0))
            obstacle = {
                "type": "lamp",
                "image": img,
                "rect": rect,
                "hitbox": pygame.Rect(
                    rect.x + HITBOX_MARGIN["lamp"] // 2,
                    rect.y + HITBOX_MARGIN["lamp"] // 2,
                    rect.width - HITBOX_MARGIN["lamp"],
                    rect.height - HITBOX_MARGIN["lamp"]
                ),
                "activated": False,
                "speed_y": 0,
                "landed": False,
                "passed": False
            }

        # =====================
        # RULER (lucht)
        # =====================
        elif obstacle_type == "ruler":
            rect = img.get_rect(midbottom=(x, ground_rect.top - 120))
            obstacle = {
                "type": "ruler",
                "image": img,
                "rect": rect,
                "hitbox": pygame.Rect(
                    rect.x + HITBOX_MARGIN["ruler"] // 2,
                    rect.y + HITBOX_MARGIN["ruler"] // 2,
                    rect.width - HITBOX_MARGIN["ruler"],
                    rect.height - HITBOX_MARGIN["ruler"]
                ),
                "passed": False
            }

        # =====================
        # DESK (grond)
        # =====================
        elif obstacle_type == "desk":
            bank_width, bank_height = 100, 100
            rect = img.get_rect(bottomleft=(x, ground_rect.top))
            obstacle = {
                "type": "desk",
                "image": img,
                "rect": rect,
                "hitbox": pygame.Rect(
                    rect.x + HITBOX_MARGIN["desk"] // 2,
                    rect.y + HITBOX_MARGIN["desk"] // 2,
                    rect.width - HITBOX_MARGIN["desk"],
                    rect.height - HITBOX_MARGIN["desk"]
                ),
                "passed": False
            }

        # =====================
        # BAG (grond)
        # =====================
        else:
            rect = img.get_rect(bottomleft=(x, ground_rect.top))
            obstacle = {
                "type": "bag",
                "image": img,
                "rect": rect,
                "hitbox": pygame.Rect(
                    rect.x + HITBOX_MARGIN["bag"] // 2,
                    rect.y + HITBOX_MARGIN["bag"] // 2,
                    rect.width - HITBOX_MARGIN["bag"],
                    rect.height - HITBOX_MARGIN["bag"]
                ),
                "passed": False
            }

        obstacles.append(obstacle)
        x += OBSTACLE_DISTANCE

    return obstacles


def update_obstacles(obstacles, player):
    """Update obstakels: beweging, lamp logica en respawn."""
    for obs in obstacles:
        # Beweeg naar links
        obs["rect"].x -= OBSTACLE_SPEED
        obs["hitbox"].x -= OBSTACLE_SPEED  # hitbox meebewegen

        # =====================
        # Lamp logica
        # =====================
        if obs["type"] == "lamp":
            if not obs["activated"] and player.rect.x > obs["rect"].x - 500:
                obs["activated"] = True
                obs["speed_y"] = 10

            if obs["activated"] and not obs["landed"]:
                obs["rect"].y += obs["speed_y"]
                obs["hitbox"].y += obs["speed_y"]

                if obs["rect"].bottom >= GROUND_Y:
                    obs["rect"].bottom = GROUND_Y
                    obs["hitbox"].bottom = GROUND_Y
                    obs["speed_y"] = 0
                    obs["landed"] = True

        # =====================
        # Respawn obstakel
        # =====================
        if obs["rect"].right < 0:
            obs["rect"].x = WIDTH + OBSTACLE_DISTANCE
            obs["hitbox"].x = obs["rect"].x + HITBOX_MARGIN.get(obs["type"], 0) // 2
            obs["passed"] = False

            if obs["type"] == "lamp":
                obs["activated"] = False
                obs["landed"] = False
                obs["speed_y"] = 0
                obs["rect"].y = 0
                obs["hitbox"].y = 0
