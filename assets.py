import pygame
from settings import *

def load_assets():
    return {
        "bg": pygame.transform.scale(
            pygame.image.load("assets/bg.png").convert_alpha(),
            (int(WIDTH * 1.1), int(HEIGHT * 1.1))
        ),
        "ground": pygame.transform.scale(
            pygame.image.load("assets/grond.png").convert_alpha(),
            (WIDTH, HEIGHT - GROUND_Y)
        ),
        "player": pygame.transform.scale(
            pygame.image.load("assets/karakter.png").convert_alpha(),
            (PLAYER_SIZE, PLAYER_SIZE)
        ),
        "ruler": pygame.transform.scale(
            pygame.image.load("assets/liniaal.png").convert_alpha(),
            (60, GROUND_Y)
        ),
        "bag": pygame.transform.scale(
            pygame.image.load("assets/rugzak.png").convert_alpha(),
            (70, 70)
        ),
        "desk": pygame.transform.scale(
            pygame.image.load("assets/bank.png").convert_alpha(),
            (60, 60)
        ),
    }

