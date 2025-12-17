import pygame
import random
from settings import *

# =====================
# OBSTAKEL TYPES
# =====================
GROUND_OBSTACLES = ["bag", "desk"]
AIR_OBSTACLES = ["ruler", "lamp"]

MAX_AIR_IN_ROW = 1

# =====================
# HITBOX MARGINS
# =====================
HITBOX_MARGIN = {
    "lamp": 20,
    "ruler": 20,
    "desk": 10,
    "bag": 5
}

# =====================
# AFSTAND INSTELLINGEN
# =====================
MIN_OBSTACLE_GAP = 220
MAX_EXTRA_GAP = 180
PLAYER_SAFE_GAP = 160   # extra ruimte bij 2 grond obstakels


# =====================
# RANDOM OBSTAKEL KEUZE
# =====================
def get_random_obstacle(last_kind, air_count):
    if last_kind == "air" and air_count >= MAX_AIR_IN_ROW:
        kind = "ground"
    else:
        kind = random.choice(["ground", "air"])

    obstacle_type = random.choice(
        GROUND_OBSTACLES if kind == "ground" else AIR_OBSTACLES
    )

    return kind, obstacle_type


# =====================
# OBSTAKELS AANMAKEN
# =====================
def create_obstacles(ground_rect, x_start, assets, amount=7):
    obstacles = []
    x = x_start

    last_kind = None
    air_count = 0

    for _ in range(amount):
        kind, obstacle_type = get_random_obstacle(last_kind, air_count)

        if kind == "air":
            air_count += 1
        else:
            air_count = 0

        img = assets[obstacle_type]

        # ---------------------
        # POSITIE
        # ---------------------
        if obstacle_type == "lamp":
            rect = img.get_rect(midtop=(x, 0))
        elif obstacle_type == "ruler":
            rect = img.get_rect(midbottom=(x, ground_rect.top - 110))
        else:
            rect = img.get_rect(bottomleft=(x, ground_rect.top))

        # ---------------------
        # VEILIGE PLAATSING
        # ---------------------
        if obstacles:
            prev = obstacles[-1]
            gap = MIN_OBSTACLE_GAP + random.randint(0, MAX_EXTRA_GAP)

            # extra ruimte voor 2 grond obstakels
            if (
                prev["type"] in GROUND_OBSTACLES
                and obstacle_type in GROUND_OBSTACLES
            ):
                gap += PLAYER_SAFE_GAP

            rect.x = prev["rect"].right + gap

        # ---------------------
        # HITBOX
        # ---------------------
        margin = HITBOX_MARGIN[obstacle_type]
        hitbox = pygame.Rect(
            rect.x + margin // 2,
            rect.y + margin // 2,
            rect.width - margin,
            rect.height - margin
        )

        obstacle = {
            "type": obstacle_type,
            "image": img,
            "rect": rect,
            "hitbox": hitbox,
            "passed": False
        }

        # extra lamp data
        if obstacle_type == "lamp":
            obstacle.update({
                "activated": False,
                "speed_y": 0,
                "landed": False
            })

        obstacles.append(obstacle)
        last_kind = kind

    return obstacles


# =====================
# OBSTAKELS UPDATEN
# =====================
def update_obstacles(obstacles, player):
    for obs in obstacles:
        # beweging
        obs["rect"].x -= OBSTACLE_SPEED
        obs["hitbox"].x -= OBSTACLE_SPEED

        # ---------------------
        # LAMP LOGICA
        # ---------------------
        if obs["type"] == "lamp":
            if not obs["activated"] and player.rect.right > obs["rect"].x - 500:
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

        # ---------------------
        # RESPAWN (VEILIG)
        # ---------------------
        if obs["rect"].right < 0:
            last = max(obstacles, key=lambda o: o["rect"].right)

            gap = MIN_OBSTACLE_GAP + random.randint(0, MAX_EXTRA_GAP)
            if (
                last["type"] in GROUND_OBSTACLES
                and obs["type"] in GROUND_OBSTACLES
            ):
                gap += PLAYER_SAFE_GAP

            obs["rect"].x = last["rect"].right + gap
            margin = HITBOX_MARGIN[obs["type"]]
            obs["hitbox"].x = obs["rect"].x + margin // 2
            obs["passed"] = False

            if obs["type"] == "lamp":
                obs["activated"] = False
                obs["landed"] = False
                obs["speed_y"] = 0
                obs["rect"].y = 0
                obs["hitbox"].y = 0
