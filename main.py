import pygame
import math
import time
import random

from loading_screen import loading_screen
from menu import menu, scoreboard, death_screen, get_selected_skin
from settings import *
from assets import load_assets
from player import Player
from obstacles import create_obstacles, update_obstacles
from music import *
from leaderboard import save_score
from coins import (
    load_coin_image,
    create_coins,
    coins,
    WORLD_SPEED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COIN_MIN_Y,
    COIN_MAX_Y,
)
from how_to_play import how_to_play
from pause_menu import pause_menu

pygame.init()

selected_skin = get_selected_skin()

coin_img = load_coin_image()
create_coins()

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
current_player_name = "Player"

# =====================
# HIGHSCORE (local file)
# =====================
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore_local(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except:
        pass


# =====================
# PANEL
# =====================
def draw_rounded_panel(surface, rect, color, radius):
    panel = pygame.Surface((rect.width, rect.height + 50), pygame.SRCALPHA)
    pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)


# =====================
# MUSIC
# =====================
sound_hub.play_sound()

# =====================
# GAME FUNCTION
# =====================
def run_game(selected_skin, font):
    paused = False

    score = 0
    highscore = load_highscore()
    start_time = time.time()

    speed = OBSTACLE_SPEED
    speed_increase = 1
    timer = 0
    interval = 25000

    coins_collected = 0

    assets = load_assets()
    ground_rect = pygame.Rect(0, GROUND_Y, WIDTH, GROUND_HEIGHT)

    player = Player(ground_rect, skin=selected_skin)

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

    # pauze visuals (1x)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    pause_font = pygame.font.SysFont(None, 72)
    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))

    running = True
    while running:
        dt = clock.tick(FPS)

        # =====================
        # EVENTS
        # =====================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_SPACE) and not paused:
                    player.start_jump()

                if event.key == pygame.K_p:
                    paused = not paused

        keys = pygame.key.get_pressed()

        # =====================
        # UPDATES (ALLEEN ALS NIET GEPAUZEERD)
        # =====================
        if not paused:
            # timer/speed
            timer += dt
            if timer >= interval:
                speed += speed_increase
                timer = 0
            speed = min(speed, 20)

            # player + obstacles
            player.update(keys, ground_rect)
            update_obstacles(obstacles, player, speed)

            # background + ground
            scroll -= speed
            if abs(scroll) > bg_width:
                scroll = 0

            ground_x -= speed
            if ground_x <= -WIDTH:
                ground_x = 0

            # coins movement
            for coin in coins:
                coin["rect"].x -= WORLD_SPEED
                if coin["rect"].right < 0:
                    coin["rect"].x = random.randint(SCREEN_WIDTH + 600, SCREEN_WIDTH + 1400)
                    coin["rect"].y = random.randint(COIN_MIN_Y, COIN_MAX_Y)

        # =====================
        # COLLISION & SCORING
        # =====================
        for obs in obstacles:
            if player.hitbox.colliderect(obs["hitbox"]):
                time_survived = time.time() - start_time
                save_score(current_player_name, coins_collected, time_survived)

                stats = {
                    "Score": score,
                    "Coins": coins_collected,
                    "Time": f"{int(time_survived // 60)}:{int(time_survived % 60):02d}"
                }
                return "death_screen", stats

            if not obs.get("passed", False) and obs["rect"].right < player.rect.left:
                score += 1
                obs["passed"] = True
                highscore = max(highscore, score)
                save_highscore_local(highscore)

        # =====================
        # DRAW (ALTIJD)
        # =====================
        # background
        for i in range(tiles):
            screen.blit(bg, (i * bg_width + scroll - 100, -100))

        # ground
        screen.blit(assets["ground"], (ground_x, ground_rect.top))
        screen.blit(assets["ground"], (ground_x + WIDTH, ground_rect.top))

        # player + obstacles
        player.draw(screen)
        for obs in obstacles:
            screen.blit(obs["image"], obs["rect"])

        # coins draw + collect (collect alleen als niet gepauzeerd)
        for coin in coins:
            screen.blit(coin_img, coin["rect"])

            if not paused and player.hitbox.colliderect(coin["rect"]):
                coins_collected += 1
                coin["rect"].x = random.randint(SCREEN_WIDTH + 600, SCREEN_WIDTH + 1400)
                coin["rect"].y = random.randint(COIN_MIN_Y, COIN_MAX_Y)

        # pause overlay
        if paused:
            screen.blit(overlay, (0, 0))
            screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        # score panel
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
        coins_text = font.render(f"Candy: {coins_collected}", True, (255, 255, 255))

        padding = PANEL_PADDING
        panel_width = max(score_text.get_width(), high_text.get_width()) + padding * 2
        panel_height = score_text.get_height() * 2 + padding * 3
        panel_rect = pygame.Rect(30, 20, panel_width, panel_height)

        draw_rounded_panel(screen, panel_rect, PANEL_COLOR, PANEL_RADIUS)
        screen.blit(score_text, (panel_rect.x + padding, panel_rect.y + padding))
        screen.blit(high_text, (panel_rect.x + padding, panel_rect.y + padding + score_text.get_height() + 10))
        screen.blit(coins_text, (panel_rect.x + padding, panel_rect.y + padding + score_text.get_height() + 80))

        pygame.display.update()


# =====================
# CONTROLLER
# =====================
def main():
    state = "loading"
    selected_skin = "default"
    global current_player_name

    player_name = ""

    while state != "quit":
        if state == "loading":
            state = loading_screen(screen, clock)

        elif state == "menu":
            state, selected_skin, player_name = menu(screen, clock, font, menu_bg)
            if player_name:
                current_player_name = player_name

        elif state == "how_to_play":
            state = how_to_play(screen, clock)

        elif state == "play":
            state, stats = run_game(selected_skin, font)

        # (optioneel) je pause_menu state blijft staan, maar wordt niet gebruikt
        # omdat pauze nu in run_game zit via P toggle.
        elif state == "pause":
            result = pause_menu(screen, clock)
            if result == "resume":
                state = "play"
            else:
                state = result

        elif state == "death_screen":
            state = death_screen(screen, clock, font, font, stats)

        elif state == "scoreboard":
            state = scoreboard(screen, clock)

    pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()