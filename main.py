import pygame
import math

from settings import *
from assets import load_assets
from player import Player
from obstacles import create_obstacles, update_obstacles
from music import *

pygame.init()

# =====================
# HIGHSCORE FUNCTIES
# =====================
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))


# =====================
# PANEL TEKEN FUNCTIE
# =====================
def draw_rounded_panel(surface, rect, color, radius):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)


# =====================
# BASIS
# =====================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teacher Run")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)

score = 0
highscore = load_highscore()

# =====================
# ASSETS
# =====================
assets = load_assets()

# =====================
# OBJECTEN
# =====================
ground_rect = pygame.Rect(0, GROUND_Y, WIDTH, GROUND_HEIGHT)

player = Player(ground_rect)

obstacles = create_obstacles(
    ground_rect,
    WIDTH + 300,
    assets
)

# =====================
# ACHTERGROND
# =====================
bg = assets["bg"]
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(WIDTH / bg_width) + 2
ground_x = 0

# =====================
# Music
# =====================

sound_hub.play_sound()

# =====================
# GAME LOOP
# =====================
running = True
while running:
    clock.tick(FPS)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # =====================
    # UPDATE
    # =====================
    player.update(keys, ground_rect)
    update_obstacles(obstacles, player)

    # =====================
    # COLLISIE + SCORE
    # =====================
    for obs in obstacles:
        if player.hitbox.colliderect(obs["rect"]):
            if score > highscore:
                save_highscore(score)
            print("GESNAPT DOOR DE LEERKRACHT!")
            running = False

        if not obs.get("passed", False) and obs["rect"].right < player.rect.left:
            score += 1
            obs["passed"] = True
            if score > highscore:
                highscore = score

    # =====================
    # ACHTERGROND
    # =====================
    scroll -= OBSTACLE_SPEED
    if abs(scroll) > bg_width:
        scroll = 0

    for i in range(tiles):
        screen.blit(bg, (i * bg_width + scroll - 100, -100))

    # =====================
    # GROND
    # =====================
    ground_x -= OBSTACLE_SPEED
    if ground_x <= -WIDTH:
        ground_x = 0

    screen.blit(assets["ground"], (ground_x, ground_rect.top))
    screen.blit(assets["ground"], (ground_x + WIDTH, ground_rect.top))

    # =====================
    # SPELER
    # =====================
    player.draw(screen)

    # =====================
    # OBSTAKELS
    # =====================
    for obs in obstacles:
        screen.blit(obs["image"], obs["rect"])

    # =====================
    # SCORE PANEL
    # =====================
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))

    padding = PANEL_PADDING

    panel_width = max(
        score_text.get_width(),
        high_text.get_width()
    ) + padding * 2

    panel_height = score_text.get_height() * 2 + padding * 3

    panel_rect = pygame.Rect(30, 20, panel_width, panel_height)

    draw_rounded_panel(
        screen,
        panel_rect,
        PANEL_COLOR,
        PANEL_RADIUS
    )

    screen.blit(
        score_text,
        (panel_rect.x + padding, panel_rect.y + padding)
    )

    screen.blit(
        high_text,
        (
            panel_rect.x + padding,
            panel_rect.y + padding + score_text.get_height() + 10
        )
    )

    pygame.display.update()

pygame.quit()
