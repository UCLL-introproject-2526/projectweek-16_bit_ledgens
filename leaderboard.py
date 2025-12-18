import pygame
import time
import os
from datetime import datetime

SCORES_FILE = "scores.txt"


# =====================
# SAVE SCORE
# =====================
def save_score(player_name, time_survived):
    if not player_name:
        player_name = "Player"

    day = datetime.now().day  # only day of month

    with open(SCORES_FILE, "a") as f:
        f.write(f"{player_name},{int(time_survived)},{day}\n")


# =====================
# LOAD SCORES
# =====================
def load_scores(limit=10):
    if not os.path.exists(SCORES_FILE):
        return []

    scores = []
    with open(SCORES_FILE, "r") as f:
        for line in f:
            try:
                name, survived, day = line.strip().split(",")
                scores.append((name, int(survived), day))
            except:
                pass

    # Sort by survival time (highest first)
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:limit]


# =====================
# SCOREBOARD SCREEN
# =====================
def scoreboard(screen, clock, font):
    title_font = pygame.font.SysFont(None, 56)
    small_font = pygame.font.SysFont(None, 30)

    back_button = pygame.Rect(0, 0, 140, 45)
    back_button.center = (750, 650)

    scores = load_scores(10)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "menu"

        screen.fill((245, 245, 245))

        # Title
        title = title_font.render("SCOREBOARD", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(750, 120)))

        # Headers
        header = small_font.render("Name        Time Survived (s)        Day", True, (0, 0, 0))
        screen.blit(header, (420, 180))

        # Scores
        y = 220
        for i, (name, survived, day) in enumerate(scores):
            text = small_font.render(
                f"{i+1}. {name:<10}     {survived:>5}                {day}",
                True,
                (0, 0, 0)
            )
            screen.blit(text, (420, y))
            y += 35

        # Back button
        mouse_pos = pygame.mouse.get_pos()
        color = (180, 180, 180) if back_button.collidepoint(mouse_pos) else (210, 210, 210)

        pygame.draw.rect(screen, color, back_button)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 3)

        back_text = small_font.render("BACK", True, (0, 0, 0))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()