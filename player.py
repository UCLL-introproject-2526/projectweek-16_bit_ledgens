import pygame
from settings import *

class Player:
    def __init__(self, ground):
        self.rect = pygame.Rect(
            PLAYER_X,
            ground.top - PLAYER_SIZE,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        self.vel_y = 0
        self.is_ducking = False
        self.original_height = PLAYER_SIZE

        self.hitbox = self.rect.copy()

    def update(self, keys, ground):
        if keys[pygame.K_UP] and self.rect.bottom == ground.top:
            self.vel_y = JUMP_FORCE

        if keys[pygame.K_DOWN]:
            if not self.is_ducking:
                self.rect.height = self.original_height // 2
                self.rect.y += self.original_height // 2
                self.is_ducking = True
        else:
            if self.is_ducking:
                self.rect.y -= self.original_height // 2
                self.rect.height = self.original_height
                self.is_ducking = False

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.colliderect(ground):
            self.rect.bottom = ground.top
            self.vel_y = 0

        self.hitbox.x = self.rect.x + HITBOX_MARGIN // 2
        self.hitbox.y = self.rect.y + HITBOX_MARGIN // 2
        self.hitbox.width = self.rect.width - HITBOX_MARGIN
        self.hitbox.height = self.rect.height - HITBOX_MARGIN

    def draw(self, screen, image):
        screen.blit(image, self.rect)

