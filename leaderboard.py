import pygame
import time
import os
from datetime import datetime

SCORES_FILE = "scores.txt"
FONT_PATH = "assets/fonts/blooming.ttf"


# =====================
# SAVE SCORE
# =====================
def save_score(player_name, time_survived):
    player_name = player_name.strip() if player_name else "Player"

    # prevent commas (they break CSV format)
    player_name = player_name.replace(",", "")

    day = datetime.now().day

    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{player_name},{int(time_survived)},{day}\n")


# =====================
# LOAD SCORES
# =====================
def load_scores(limit=10):
    if not os.path.exists(SCORES_FILE):
        return []

    scores = []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                name, survived, day = line.split(",")
                scores.append((name.strip(), int(survived), day.strip()))
            except ValueError:
                continue

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:limit]



def scoreboard(screen, clock):

    title_font = pygame.font.Font("assets/fonts/blooming.ttf", 60)
    small_font = pygame.font.Font("assets/fonts/blooming.ttf", 32)

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

        
        title = title_font.render("Scoreboard", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(750, 120)))

        
        header = small_font.render("Name      Time (s)      Day", True, (0, 0, 0))
        screen.blit(header, (420, 180))

        
        y = 230
        for i, (name, survived, day) in enumerate(scores):
            line = f"{i+1:>2}. {name:<15} {survived:>6} s   Day {day}"
            text = small_font.render(line, True, (0, 0, 0))
            screen.blit(text, (420, y))
            y += 38

       
        mouse_pos = pygame.mouse.get_pos()
        color = (180, 180, 180) if back_button.collidepoint(mouse_pos) else (210, 210, 210)

        pygame.draw.rect(screen, color, back_button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 2, border_radius=8)

        back_text = small_font.render("Back", True, (0, 0, 0))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()