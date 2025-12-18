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
from coins import load_coin_image, create_coins, coins, WORLD_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_SPEED, COIN_MIN_Y, COIN_MAX_Y, coins


pygame.init()


# Startup.startup_loading_screen([
#     load_images,
#     load_audio,
#     load_fonts,
# ])


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
def run_game(selected_skin):
    score = 0
    highscore = load_highscore()
    start_time = time.time()
    speed = OBSTACLE_SPEED      # start snelheid
    speed_increase = 1          # hoeveel sneller
    timer = 0                   # tijdsteller
    interval = 25000            # 25 seconden (ms)
    coins_collected = 0


    assets = load_assets()

    ground_rect = pygame.Rect(0, GROUND_Y, WIDTH, GROUND_HEIGHT)

    # 🔥 skin toegevoegd (uit nieuwe versie)
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

    running = True
    while running:
        dt = clock.tick(FPS)
        timer += dt

        if timer >= interval:
            speed += speed_increase
            timer = 0

        speed = min(speed, 20)


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
        # ❗ FIX: ground_rect meegeven
        player.update(keys, ground_rect)
        update_obstacles(obstacles, player, speed)

        # =====================
        # COLLISION & SCORING
        # =====================
        for obs in obstacles:
            if player.hitbox.colliderect(obs["hitbox"]):
                time_survived = time.time() - start_time
                save_score(current_player_name, coins_collected, time_survived)
                return "death_screen"

            if not obs.get("passed", False) and obs["rect"].right < player.rect.left:
                score += 1
                obs["passed"] = True
                highscore = max(highscore, score)
                save_highscore_local(highscore)

        # =====================
        # BACKGROUND SCROLL
        scroll -= speed
        if abs(scroll) > bg_width:
            scroll = 0

        for i in range(tiles):
            screen.blit(bg, (i * bg_width + scroll - 100, -100))

        # =====================
        # GROUND SCROLL
        ground_x -= speed
        if ground_x <= -WIDTH:
            ground_x = 0

        screen.blit(assets["ground"], (ground_x, ground_rect.top))
        screen.blit(assets["ground"], (ground_x + WIDTH, ground_rect.top))

        # =====================
        # DRAW PLAYER & OBSTACLES
        # =====================
        player.draw(screen)

        for obs in obstacles:
            screen.blit(obs["image"], obs["rect"])

        # =====================
        # SCORE PANEL (nettere versie)
        # =====================
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
        coins_text = font.render(f"coins: {coins_collected}", True, (255, 255, 255))

        padding = PANEL_PADDING
        panel_width = max(score_text.get_width(), high_text.get_width()) + padding * 2
        panel_height = score_text.get_height() * 2 + padding * 3
        panel_rect = pygame.Rect(30, 20, panel_width, panel_height)

        draw_rounded_panel(screen, panel_rect, PANEL_COLOR, PANEL_RADIUS)

        screen.blit(score_text, (panel_rect.x + padding, panel_rect.y + padding))
        screen.blit(high_text, (panel_rect.x + padding, panel_rect.y + padding + score_text.get_height() + 10))
        screen.blit(coins_text, (panel_rect.x + padding, panel_rect.y + padding + score_text.get_height() + 80))
        pygame.display.update()

# --- COINS ---
        for coin in coins:
            # collision → 1x tellen, daarna UIT
            if player.hitbox.colliderect(coin["rect"]):
                coins_collected += 1

                coin["rect"].x = random.randint(SCREEN_WIDTH + 600, SCREEN_WIDTH + 1400)
                coin["rect"].y = random.randint(80, SCREEN_HEIGHT - 80)
                coin["rect"].y = random.randint(COIN_MIN_Y, COIN_MAX_Y)
                coin["respawn_timer"] = 180   # ⬅ 2 seconden bij 60 FPS
            # 🌍 DAN pas bewegen (zoals obstacles)
            coin["rect"].x -= WORLD_SPEED

            # buiten beeld → reset
            if coin["rect"].right < 0:
                coin["rect"].x = random.randint(SCREEN_WIDTH + 600, SCREEN_WIDTH + 1400)
                coin["rect"].y = random.randint(COIN_MIN_Y, COIN_MAX_Y)

            # Teken coin
            screen.blit(coin_img, coin["rect"])


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

            # ✅ update name ONLY after menu
            if player_name:
                current_player_name = player_name

        elif state == "play":
            state = run_game(selected_skin)

        elif state == "death_screen":
            state = death_screen(screen, clock, font, font)

        elif state == "scoreboard":
            state = scoreboard(screen, clock)

    pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
