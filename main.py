import pygame
import math
import time

from menu import menu, scoreboard, death_screen
from settings import *
from assets import load_assets
from player import Player
from obstacles import create_obstacles, update_obstacles
from music import *
from leaderboard import save_score

pygame.init()


# =====================
# WINDOW
# =====================
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teacher Run")
clock = pygame.time.Clock()

# =====================
# BACKGROUNDS
# =====================
menu_bg = pygame.image.load("assets/images/menu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

# =====================
# FONTS
# =====================
font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)

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
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except:
        pass

# =====================
# PANEL
# =====================
def draw_rounded_panel(surface, rect, color, radius):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)

# =====================
# Just play the music
# =====================

sound_hub.play_sound()




# =====================
# GAME FUNCTION
# =====================
def run_game():
    score = 0
    highscore = load_highscore()
    start_time = time.time()

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

    

    running = True
    while running:
        clock.tick(FPS)

        # =====================
        # EVENTS
        # =====================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.start_jump()

        keys = pygame.key.get_pressed()

        # =====================
        # UPDATES
        # =====================
        player.update(keys, ground_rect)
        update_obstacles(obstacles, player)

        # COLLISION & SCORING
        for obs in obstacles:
            if player.hitbox.colliderect(obs["hitbox"]):
                time_survived = time.time() - start_time
                save_score("Player", time_survived)
                return "death_screen"

            if not obs.get("passed", False) and obs["rect"].right < player.rect.left:
                score += 1
                obs["passed"] = True
                highscore = max(highscore, score)

        # BACKGROUND SCROLL
        scroll -= OBSTACLE_SPEED
        if abs(scroll) > bg_width:
            scroll = 0

        for i in range(tiles):
            screen.blit(bg, (i * bg_width + scroll - 100, -100))

        # GROUND SCROLL
        ground_x -= OBSTACLE_SPEED
        if ground_x <= -WIDTH:
            ground_x = 0

        screen.blit(assets["ground"], (ground_x, ground_rect.top))
        screen.blit(assets["ground"], (ground_x + WIDTH, ground_rect.top))

        # DRAW PLAYER
        player.draw(screen)

        # DRAW OBSTACLES
        for obs in obstacles:
            screen.blit(obs["image"], obs["rect"])

        # DRAW SCORE PANEL
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))

        padding = PANEL_PADDING
        panel_rect = pygame.Rect(
            30, 20,
            max(score_text.get_width(), high_text.get_width()) + padding * 2,
            score_text.get_height() * 2 + padding * 3
        )

        draw_rounded_panel(screen, panel_rect, PANEL_COLOR, PANEL_RADIUS)

        screen.blit(score_text, (panel_rect.x + padding, panel_rect.y + padding))
        screen.blit(high_text, (panel_rect.x + padding, panel_rect.y + padding + score_text.get_height() + 10))

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
            state = run_game()

        elif state == "death_screen":
            state = death_screen(screen, clock, font, font)

        elif state == "scoreboard":
            state = scoreboard(screen, clock)

    pygame.quit()

if __name__ == "__main__":
    main()
