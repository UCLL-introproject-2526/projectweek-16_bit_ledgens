import pygame
import os


SCORES_FILE = "scores.txt"
FONT_PATH = "assets/fonts/strip-line.otf"


# =====================
# SAVE SCORE
# =====================
def save_score(player_name, score, time_survived):
    player_name = player_name.strip() if player_name else "Player"
    player_name = player_name.replace(",", "")  # CSV safety

    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{player_name},{int(score)},{int(time_survived)}\n")


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
                name, score, time_survived = line.strip().split(",")
                scores.append((name, int(score), int(time_survived)))
            except ValueError:
                continue

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:limit]


# =====================
# SCOREBOARD SCREEN
# =====================
def scoreboard(screen, clock):
    title_font = pygame.font.Font(FONT_PATH, 60)
    small_font = pygame.font.Font(FONT_PATH, 32)

    back_button = pygame.Rect(0, 0, 140, 45)
    back_button.center = (screen.get_width() // 2, 650)

    scores = load_scores(10)

    # Load background once, scale to screen
    leaderboard_bg = pygame.image.load("assets/images/leaderboard.png").convert()
    leaderboard_bg = pygame.transform.scale(leaderboard_bg, screen.get_size())

    # Column X positions
    COL_RANK = 470
    COL_NAME = 500   # left-aligned
    COL_SCORE = 750
    COL_TIME = 1000

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

        # Draw background first
        screen.blit(leaderboard_bg, (0, 0))

        # Draw title
        title = title_font.render("Scoreboard", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 120)))

        # Draw headers
        header_y = 180
        headers = ["No.", "Name", "Score", "Time (s)"]
        cols = [COL_RANK, COL_NAME, COL_SCORE, COL_TIME]
        for h, x in zip(headers, cols):
            text = small_font.render(h, True, (255, 255, 255))
            if h == "Name":
                rect = text.get_rect(midleft=(x, header_y))
            else:
                rect = text.get_rect(center=(x, header_y))
            screen.blit(text, rect)

        # Draw scores
        y = 230
        for i, (name, score, time_survived) in enumerate(scores):
            texts = [
                small_font.render(f"{i+1}.", True, (255, 255, 255)),
                small_font.render(name, True, (255, 255, 255)),
                small_font.render(str(score), True, (255, 255, 255)),
                small_font.render(str(time_survived), True, (255, 255, 255)),
            ]
            for idx, (t, x) in enumerate(zip(texts, cols)):
                if idx == 1:  # name column
                    rect = t.get_rect(midleft=(x, y))
                else:
                    rect = t.get_rect(center=(x, y))
                screen.blit(t, rect)
            y += 38

        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        color = (7, 122, 26) if back_button.collidepoint(mouse_pos) else (217, 150, 39)
        pygame.draw.rect(screen, color, back_button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 2, border_radius=8)
        back_text = small_font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()