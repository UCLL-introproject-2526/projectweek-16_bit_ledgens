import pygame
import random

COIN_AMOUNT = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
WORLD_SPEED = 6
COIN_MIN_Y = 260
COIN_MAX_Y = 340

coins = []

def load_coin_image():
    coin_img = pygame.image.load("assets/images/candy.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (128, 128))
    return coin_img

def create_coins(amount=COIN_AMOUNT):
    for i in range(amount):
        coin = {
            "rect": pygame.Rect(
                SCREEN_WIDTH - 100,
                random.randint(80, SCREEN_HEIGHT - 80),
                64, 64
            ),
            "respawn_timer": 0
        }
        coins.append(coin)