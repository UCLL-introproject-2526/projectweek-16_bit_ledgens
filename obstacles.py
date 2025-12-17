import pygame
from settings import *
import random

GROUND_OBSTACLES = ["bag", "desk"]
AIR_OBSTACLES = ["ruler", "lamp"]

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

        img = random.choice(
            GROUND_OBSTACLES if kind == "ground" else AIR_OBSTACLES
        )

        sequence.append((kind, img))
        last_kind = kind

    return sequence


def create_obstacles(ground_rect, x_start, assets):
    obstacles = []
    x = x_start

    types = ["lamp", "ruler", "desk", "bag"]

    for _ in range(4):
        obstacle_type = random.choice(types)

        # =====================
        # LAMP (plafond)
        # =====================
        if obstacle_type == "lamp":
            img = assets["lamp"]
            rect = img.get_rect(
                midtop=(x, 0)
            )

            obstacle = {
                "type": "lamp",
                "image": img,
                "rect": rect,
                "activated": False,
                "speed_y": 0,
                "passed": False
            }

        # =====================
        # RULER (hangt in de lucht)
        # =====================
        elif obstacle_type == "ruler":
            img = assets["ruler"]
            rect = img.get_rect(
                midbottom=(x, ground_rect.top - 120)
            )

            obstacle = {
                "type": "ruler",
                "image": img,
                "rect": rect,
                "passed": False
            }

        # =====================
        # DESK (grond)
        # =====================
        elif obstacle_type == "desk":
            img = assets["desk"]
            rect = img.get_rect(
                bottomleft=(x, ground_rect.top)
            )

            obstacle = {
                "type": "desk",
                "image": img,
                "rect": rect,
                "passed": False
            }

        # =====================
        # BAG (grond)
        # =====================
        else:
            img = assets["bag"]
            rect = img.get_rect(
                bottomleft=(x, ground_rect.top)
            )

            obstacle = {
                "type": "bag",
                "image": img,
                "rect": rect,
                "passed": False
            }

        obstacles.append(obstacle)
        x += OBSTACLE_DISTANCE

    return obstacles


def update_lamp(obs, player, ground):
    if obs["state"] == "idle":
        if obs["rect"].x - player.rect.right < LAMP_TRIGGER_DISTANCE:
            obs["state"] = "dropping"

    elif obs["state"] == "dropping":
        obs["rect"].y += LAMP_DROP_SPEED

        if obs["rect"].bottom >= ground.top - LAMP_MIN_GAP:
            obs["rect"].bottom = ground.top - LAMP_MIN_GAP
            obs["state"] = "done"


from settings import *


def update_obstacles(obstacles, player):
    for obs in obstacles:
        # beweeg naar links
        obs["rect"].x -= OBSTACLE_SPEED

        # =====================
        # LAMP LOGICA
        # =====================
        if obs["type"] == "lamp":
            # activeer VROEG
            if not obs["activated"] and player.rect.x > obs["rect"].x - 500:
                obs["activated"] = True
                obs["speed_y"] = 10

            # laat vallen
            if obs["activated"] and not obs.get("landed", False):
                obs["rect"].y += obs["speed_y"]

                # stop op de grond
                if obs["rect"].bottom >= GROUND_Y:
                    obs["rect"].bottom = GROUND_Y
                    obs["speed_y"] = 0
                    obs["landed"] = True

        # =====================
        # RESPAWN
        # =====================
        if obs["rect"].right < 0:
            obs["rect"].x = WIDTH + OBSTACLE_DISTANCE
            obs["passed"] = False

            if obs["type"] == "lamp":
                obs["activated"] = False
                obs["landed"] = False
                obs["speed_y"] = 0
                obs["rect"].y = 0
