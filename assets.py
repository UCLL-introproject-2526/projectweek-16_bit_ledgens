import pygame
import os
from settings import *

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets/images")


def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Asset niet gevonden: {path}")


def scale(img, w, h):
    return pygame.transform.smoothscale(img, (w, h))


def load_assets():
    return {
        # =====================
        # BACKGROUND & GROUND
        # =====================
        "bg": scale(
            load_image(os.path.join(ASSETS_DIR, "bg2.png")),
            int(WIDTH * 1.1),
            int(HEIGHT * 1.1)
        ),

        "ground": scale(
            load_image(os.path.join(ASSETS_DIR, "vloer.png")),
            WIDTH,
            HEIGHT - GROUND_Y
        ),

        # =====================
        # OBSTAKELS
        # =====================
        "ruler": scale(
            load_image(os.path.join(ASSETS_DIR, "liniaal3.png")),
            100,
            GROUND_Y
        ),

        "bag": scale(
            load_image(os.path.join(ASSETS_DIR, "rugzak.png")),
            70,
            70
        ),

        "desk": scale(
            load_image(os.path.join(ASSETS_DIR, "bank.png")),
            100,
            100
        ),

        "lamp": scale(
            load_image(os.path.join(ASSETS_DIR, "lamp2.png")),
            110,
            100
        ),
    }
