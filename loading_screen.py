import pygame
import time

WIDTH, HEIGHT = 1500, 800

def draw_text_outline(surface, text, font, color, outline_color, center, outline_width=2):
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)

    x, y = base.get_rect(center=center).topleft

    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surface.blit(outline, (x + dx, y + dy))

    surface.blit(base, (x, y))

def loading_screen(screen, clock):
    # Load image
    loading_img = pygame.image.load(
        "assets/images/loadingscreen.png"
    ).convert()
    loading_img = pygame.transform.scale(loading_img, (WIDTH, HEIGHT))

    # Fonts
    font = pygame.font.Font("assets/fonts/arcade.ttf", 30)

    # Loading bar settings
    bar_width = 600
    bar_height = 30
    bar_x = (WIDTH - bar_width) // 2
    bar_y = 600

    progress = 0
    loading_speed = 0.5

    start_time = time.time()

    while progress < 100:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        
        progress += loading_speed
        progress = min(progress, 100)

        
        screen.blit(loading_img, (0, 0))

        
        draw_text_outline(
            screen, "Loading...", font,
            (255, 255, 255),   (0, 0, 0),
            (WIDTH // 2, bar_y - 40),outline_width=2
            )

        
        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=10
        )

        pygame.draw.rect(
        screen,
        (0, 0, 0),  # black outline
        (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4),
        border_radius=12
)
        
        fill_width = int((progress / 100) * bar_width)
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (bar_x, bar_y, fill_width, bar_height),
            border_radius=10
        )

        pygame.display.flip()

    # Small pause so it feels finished
    time.sleep(0.3)

    return "menu"