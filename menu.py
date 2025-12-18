import pygame
import os

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game")

death_bg = pygame.image.load("assets/images/death.png").convert()
death_bg = pygame.transform.scale(death_bg, (WIDTH, HEIGHT))

_selected_skin = "default"

def get_selected_skin():
    return _selected_skin

def menu(screen, clock, small_font, menu_bg):
    play_button = pygame.Rect(650, 300, 200, 60)
    scoreboard_button = pygame.Rect(650, 370, 200, 60)
    quit_button = pygame.Rect(650, 440, 200, 60)
    skin_button = pygame.Rect(650, 510, 200, 60)

    SKIN_PATH = "assets/images/skins"
    skins = [name for name in os.listdir(SKIN_PATH)
         if os.path.isdir(os.path.join(SKIN_PATH, name))]

    selected_skin = skins[0] if skins else "default"
    skin_dropdown_open = False

    SKIN_BTN_HEIGHT = 40
    skin_buttons = []

    for skin, rect in skin_buttons:
        if rect.collidepoint(event.pos):
            global _selected_skin
            _selected_skin = skin

    for i, skin in enumerate(skins):
        rect = pygame.Rect(
            skin_button.x,
            skin_button.bottom + i * SKIN_BTN_HEIGHT,
            skin_button.width,
            SKIN_BTN_HEIGHT
        )
        skin_buttons.append((skin, rect))

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    # ====== Name Input ======
    name = ""
    input_active = True
    input_box = pygame.Rect(550, 230, 400, 50)
    input_color_active = (255, 255, 255)
    input_color_inactive = (200, 200, 200)

    # cursor instellingen
    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500  # ms

    while True:
        dt = clock.tick(60)  # tijd sinds laatste frame in ms
        mouse_pos = pygame.mouse.get_pos()

        # update cursor timer
        cursor_timer += dt
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
                if play_button.collidepoint(event.pos):
                    return ("play", selected_skin, name if name.strip() else "Player")
                if scoreboard_button.collidepoint(event.pos):
                    return ("scoreboard", selected_skin, name)
                if quit_button.collidepoint(event.pos):
                    return ("quit", selected_skin, name)
                if skin_button.collidepoint(event.pos):
                    skin_dropdown_open = not skin_dropdown_open

                elif skin_dropdown_open:
                    clicked_skin = False
                    for skin, rect in skin_buttons:
                        if rect.collidepoint(event.pos):
                            selected_skin = skin
                            skin_dropdown_open = False
                            clicked_skin = True
                            break
                    if not clicked_skin:
                        skin_dropdown_open = False

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                else:
                    if len(name) < 20:  # max name length
                        name += event.unicode

        screen.blit(menu_bg, (0, 0))

        # input box
        color = input_color_active if input_active else input_color_inactive
        pygame.draw.rect(screen, color, input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 3)

        # render tekst
        if name:
            display_text = name
        elif input_active:
            display_text = ""
        else:
            display_text = "Enter username"

        name_surf = font.render(display_text, True, (0, 0, 0))
        text_x = input_box.x + 10
        text_y = input_box.y + (input_box.height - name_surf.get_height()) // 2
        screen.blit(name_surf, (text_x, text_y))

        # cursor tekenen
        if input_active and cursor_visible:
            cursor_x = text_x + name_surf.get_width() + 2
            cursor_y1 = input_box.y + 5
            cursor_y2 = input_box.y + input_box.height - 5
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

        # buttons
        for button, color, text in [
            (play_button, (0, 200, 0), "PLAY"),
            (scoreboard_button, (100, 100, 255), "SCOREBOARD"),
            (quit_button, (200, 0, 0), "QUIT"),
            (skin_button, (200, 200, 0), f"SKIN: {selected_skin}")
        ]:
            if skin_dropdown_open:
                for skin, rect in skin_buttons:
                    hover = rect.collidepoint(mouse_pos)
                    color = (210, 210, 210) if hover else (230, 230, 230)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                    txt = small_font.render(skin, True, (0, 0, 0))
                    screen.blit(txt, txt.get_rect(center=rect.center))

            btn_color = tuple(max(c - 50, 0) for c in color) if button.collidepoint(mouse_pos) else color
            pygame.draw.rect(screen, btn_color, button)
            pygame.draw.rect(screen, (0, 0, 0), button, 3)
            text_surf = small_font.render(text, True, (0, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center=button.center))

            preview_text = font.render("Selected Skin:", True, (0, 0, 0))
            skin_text = font.render(selected_skin, True, (0, 0, 0))

            screen.blit(preview_text, (950, 300))
            screen.blit(skin_text, (950, 350))

        pygame.display.flip()



def scoreboard(screen, clock):
    # Load fonts (handwriting font)
    try:
        font = pygame.font.Font("assets/fonts/cartoon.ttf", 48)  # Replace with your .ttf font path
        small_font = pygame.font.Font("assets/fonts/cartoon.ttf", 28)
    except:
        font = pygame.font.SysFont(None, 48)
        small_font = pygame.font.SysFont(None, 28)

    # Back button
    back_button = pygame.Rect(0, 0, 120, 40)
    back_button.center = (750, 720)

    # Read scores from file
    scores = []
    try:
        with open("scores.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    name, seconds, day = line.split(",")
                    scores.append((name, int(seconds), day))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass

    # Sort by time survived (highest first)
    scores.sort(key=lambda x: x[1], reverse=True)

    # Keep only top 10
    scores = scores[:10]

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

        # Fill background black
        screen.fill((0, 0, 0))

        # Title
        title = font.render("SCOREBOARD", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(750, 50)))

        # Display scores
        y_start = 150
        for i, (name, seconds, day) in enumerate(scores):
            text = f"{name} - {seconds} sec - Day {day}"
            score_text = small_font.render(text, True, (255, 255, 255))
            screen.blit(score_text, score_text.get_rect(center=(750, y_start + i * 50)))

        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        btn_color = (100, 100, 100) if back_button.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(screen, btn_color, back_button)
        pygame.draw.rect(screen, (255, 255, 255), back_button, 3)  # outline

        back_text = small_font.render("BACK", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()


def death_screen(screen, clock, font, small_font):

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    back_button = pygame.Rect(0, 0, 120, 40)
    back_button.center = (750, 470)
    retry_button = pygame.Rect(0, 0, 120, 40)
    retry_button.center = (750, 400)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "menu"
                if retry_button.collidepoint(event.pos):
                    return "play"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        screen.fill((0, 0, 0))
        screen.blit(death_bg, (0, 0))

        title = font.render("YOU HAVE BEEN CAUGHT", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(750, 300)))

        pygame.draw.rect(screen, (200, 200, 200), back_button)
        pygame.draw.rect(screen, (200, 200, 200), retry_button)

        screen.blit(
            small_font.render("TO MENU", True, (0, 0, 0)),
            small_font.render("TO MENU", True, (0, 0, 0)).get_rect(center=back_button.center)
        )

        screen.blit(
            small_font.render("RETRY", True, (0, 0, 0)),
            small_font.render("RETRY", True, (0, 0, 0)).get_rect(center=retry_button.center)
        )

        pygame.display.flip()

