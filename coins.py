import pygame
import random

# Coin instellingen
COIN_AMOUNT = 1    # ⬅ hoeveel coins tegelijk
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
WORLD_SPEED = 6

COIN_MIN_Y = 260   # ⬅ coin kan niet hoger dan dit
COIN_MAX_Y = 340   # ⬅ coin kan niet lager dan dit

# Coin image laden (PNG met transparantie)
coin_img = pygame.image.load("assets/images/candy.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (128, 128))

# Lijst voor coins
coins = []

# Coins aanmaken
for i in range(COIN_AMOUNT):
    coin = {
       "rect": pygame.Rect(
            # random.randint(SCREEN_WIDTH + 600, SCREEN_WIDTH + 1400),
            SCREEN_WIDTH - 100,
            random.randint(80, SCREEN_HEIGHT - 80),
            64, 64
        ),  
    }
    coins_collected = 0
    coins.append(coin)