import pygame

import os


SCORES_FILE = "scores.txt"
FONT_PATH = "assets/fonts/blooming.ttf"


# =====================
# SAVE SCORE
# =====================
def save_score(player_name, coins_collected, time_survived):
    player_name = player_name.strip() if player_name else "Player"
    player_name = player_name.replace(",", "")  # CSV safety

    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{player_name},{coins_collected},{int(time_survived)}\n")


# =====================
# LOAD SCORES
# =====================
def load_scores(limit=10):
    if not os.path.exists(SCORES_FILE):
        return []

    scores = []

    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                name, coins, time_survived = line.strip().split(",")
                scores.append((name, int(coins), int(time_survived)))
            except ValueError:
                continue

    # Sort by time survived (highest first)
    scores.sort(key=lambda x: x[2], reverse=True)
    return scores[:limit]


# =====================
# SCOREBOARD SCREEN
# =====================
def scoreboard(screen, clock):
    title_font = pygame.font.Font(FONT_PATH, 60)
    small_font = pygame.font.Font(FONT_PATH, 32)

    back_button = pygame.Rect(0, 0, 140, 45)
    back_button.center = (750, 650)

    scores = load_scores(10)

    # Load the background image
    leaderboard_bg = pygame.image.load("assets/images/leaderboard.png").convert()
    leaderboard_bg = pygame.transform.scale(leaderboard_bg, screen.get_size())

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "menu"

        # Draw background
        screen.blit(leaderboard_bg, (0, 0))

        # Title
        title = title_font.render("Scoreboard", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(750, 120)))

        # Header
        header = small_font.render(
            "Name              Coins        Time (s)",
            True,
            (255, 255, 255)
        )
        screen.blit(header, (550, 180))

        # Scores
        y = 230
        for i, (name, coins, time_survived) in enumerate(scores):
            line = f"{i+1:>2}. {name:<15} {coins:^10} {time_survived:>6}"
            text = small_font.render(line, True, (255, 255, 255))
            screen.blit(text, (550, y))
            y += 38

        # Back button
        mouse_pos = pygame.mouse.get_pos()
        color = (7, 122, 26) if back_button.collidepoint(mouse_pos) else (217, 150, 39)
        pygame.draw.rect(screen, color, back_button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 2, border_radius=8)

        back_text = small_font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()