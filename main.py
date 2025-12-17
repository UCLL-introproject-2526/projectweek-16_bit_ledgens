import pygame
import math

from menu import menu, scoreboard, death_screen
from settings import *
from assets import load_assets
from player import Player
from obstacles import create_obstacles, update_obstacles
from music import sound_hub

pygame.init()

# =====================
# WINDOW
# =====================
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teacher Run")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)

# =====================
# BACKGROUNDS
# =====================
menu_bg = pygame.image.load("assets/menu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

# =====================
# HIGHSCORE
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
# PANEL
# =====================
def draw_rounded_panel(surface, rect, color, radius):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)


# =====================
# GAME FUNCTION
# =====================
def run_game(screen, clock, font):
    score = 0
    highscore = load_highscore()

    assets = load_assets()

    ground_rect = pygame.Rect(0, GROUND_Y, WIDTH, GROUND_HEIGHT)
    player = Player(ground_rect)

    obstacles = create_obstacles(
        ground_rect,
        WIDTH + 300,
        assets
    )

    bg = assets["bg"]
    bg_width = bg.get_width()
    scroll = 0
    tiles = math.ceil(WIDTH / bg_width) + 2
    ground_x = 0

    sound_hub.play_sound()

    running = True
    while running:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()

        # UPDATE
        player.update(keys, ground_rect)
        update_obstacles(obstacles, player)

        # COLLISION + SCORE
        for obs in obstacles:
            if player.hitbox.colliderect(obs["hitbox"]):
                if score > highscore:
                    save_highscore(score)
                return "death_screen"

            if not obs.get("passed", False) and obs["rect"].right < player.rect.left:
                score += 1
                obs["passed"] = True
                highscore = max(highscore, score)

        # BACKGROUND
        scroll -= OBSTACLE_SPEED
        if abs(scroll) > bg_width:
            scroll = 0

        for i in range(tiles):
            screen.blit(bg, (i * bg_width + scroll - 100, -100))

        # GROUND
        ground_x -= OBSTACLE_SPEED
        if ground_x <= -WIDTH:
            ground_x = 0

        screen.blit(assets["ground"], (ground_x, ground_rect.top))
        screen.blit(assets["ground"], (ground_x + WIDTH, ground_rect.top))

        # PLAYER
        player.draw(screen)

        # OBSTACLES
        for obs in obstacles:
            screen.blit(obs["image"], obs["rect"])

        # SCORE PANEL
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))

        panel_rect = pygame.Rect(30, 20, 260, 90)
        draw_rounded_panel(screen, panel_rect, PANEL_COLOR, PANEL_RADIUS)

        screen.blit(score_text, (40, 30))
        screen.blit(high_text, (40, 60))

        pygame.display.update()


# =====================
# CONTROLLER
# =====================
def main():
    state = "menu"

    while state != "quit":
        if state == "menu":
            state = menu(screen, clock, font, menu_bg)

        elif state == "play":
            state = run_game(screen, clock, font)

        elif state == "death_screen":
            state = death_screen(screen, clock, font, font)

        elif state == "scoreboard":
            state = scoreboard(screen, clock, font)

    pygame.quit()


# =====================
# START
# =====================
if __name__ == "__main__":
    main()
