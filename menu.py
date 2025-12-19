import pygame
import os
from leaderboard import scoreboard

from coins import *
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game")

death_bg = pygame.image.load("assets/images/death.png").convert()
death_bg = pygame.transform.scale(death_bg, (WIDTH, HEIGHT))

_selected_skin = "default"

def get_selected_skin():
    return _selected_skin

def load_skin_preview(skin_name):
    """Load the first frame of the skin's run animation as a preview."""
    path = f"assets/images/skins/{skin_name}/run.png"
    try:
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // 3  # first frame
        frame = sheet.subsurface((0, 0, frame_width, sheet.get_height()))
        preview = pygame.transform.scale(frame, (150, 150))  # preview size
        return preview
    except Exception as e:
        print(f"Error loading skin preview {skin_name}: {e}")
        return None


def menu(screen, clock, small_font, menu_bg):
    # =====================
    # LAYOUT
    # =====================
    base_y = 350
    BTN_WIDTH, BTN_HEIGHT = 200, 60
    BTN_MARGIN = 20

    play_button = pygame.Rect(650, base_y, BTN_WIDTH, BTN_HEIGHT)
    scoreboard_button = pygame.Rect(650, base_y + 70, BTN_WIDTH, BTN_HEIGHT)

    quit_button = pygame.Rect(
        650,
        base_y + 140,
        BTN_WIDTH // 2 - BTN_MARGIN // 2,
        BTN_HEIGHT
    )
    skin_button = pygame.Rect(
        650 + BTN_WIDTH // 2 + BTN_MARGIN // 2,
        base_y + 140,
        BTN_WIDTH // 2 - BTN_MARGIN // 2,
        BTN_HEIGHT
    )

    # =====================
    # SKINS
    # =====================
    SKIN_PATH = "assets/images/skins"
    skins = [
        name for name in os.listdir(SKIN_PATH)
        if os.path.isdir(os.path.join(SKIN_PATH, name))
    ]
    selected_skin = skins[0] if skins else "default"
    skin_dropdown_open = False

    SKIN_BTN_HEIGHT = 40
    skin_buttons = []
    for i, skin in enumerate(skins):
        rect = pygame.Rect(
            skin_button.x,
            skin_button.bottom + i * SKIN_BTN_HEIGHT,
            skin_button.width,
            SKIN_BTN_HEIGHT
        )
        skin_buttons.append((skin, rect))

    # =====================
    # FONTS
    # =====================
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    # =====================
    # NAME INPUT
    # =====================
    player_name = ""
    input_active = True
    input_box = pygame.Rect(550, base_y - 70, 400, 50)
    input_color_active = (255, 255, 255)
    input_color_inactive = (200, 200, 200)

    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500

    # =====================
    # PREVIEW LOADER
    # =====================
    def load_skin_preview(skin_name):
        try:
            path = f"assets/images/skins/{skin_name}/run.png"
            sheet = pygame.image.load(path).convert_alpha()
            frame_width = sheet.get_width() // 3
            frame = sheet.subsurface((0, 0, frame_width, sheet.get_height()))
            return pygame.transform.scale(frame, (150, 150))
        except:
            return None

    # =====================
    # LOOP
    # =====================
    while True:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        cursor_timer += dt
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", selected_skin, player_name

            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)

                if play_button.collidepoint(event.pos):
                    return "how_to_play", selected_skin, player_name

                if scoreboard_button.collidepoint(event.pos):
                    return "scoreboard", selected_skin, player_name

                if quit_button.collidepoint(event.pos):
                    return "quit", selected_skin, player_name

                if skin_button.collidepoint(event.pos):
                    skin_dropdown_open = not skin_dropdown_open

                elif skin_dropdown_open:
                    clicked = False
                    for skin, rect in skin_buttons:
                        if rect.collidepoint(event.pos):
                            selected_skin = skin
                            skin_dropdown_open = False
                            clicked = True
                            break
                    if not clicked:
                        skin_dropdown_open = False

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                elif len(player_name) < 20:
                    player_name += event.unicode

        # =====================
        # DRAW
        # =====================
        screen.blit(menu_bg, (0, 0))

        # Input box
        color = input_color_active if input_active else input_color_inactive
        pygame.draw.rect(screen, color, input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 3)

        display_text = player_name if player_name else (
            "" if input_active else "Enter username"
        )
        name_surf = font.render(display_text, True, (0, 0, 0))
        text_x = input_box.x + 10
        text_y = input_box.y + (input_box.height - name_surf.get_height()) // 2
        screen.blit(name_surf, (text_x, text_y))

        if input_active and cursor_visible:
            cursor_x = text_x + name_surf.get_width() + 2
            pygame.draw.line(
                screen, (0, 0, 0),
                (cursor_x, input_box.y + 5),
                (cursor_x, input_box.y + input_box.height - 5),
                2
            )

        # Buttons
        for button, color, text in [
            (play_button, (0, 200, 0), "PLAY"),
            (scoreboard_button, (100, 100, 255), "SCOREBOARD"),
            (quit_button, (200, 0, 0), "QUIT"),
            (skin_button, (200, 200, 0), "SKIN")
        ]:
            btn_color = (
                tuple(max(c - 40, 0) for c in color)
                if button.collidepoint(mouse_pos) else color
            )
            pygame.draw.rect(screen, btn_color, button, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), button, 3, border_radius=8)

            text_surf = small_font.render(text, True, (0, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center=button.center))

        # Skin dropdown
        if skin_dropdown_open:
            for skin, rect in skin_buttons:
                hover = rect.collidepoint(mouse_pos)
                rect_color = (210, 210, 210) if hover else (235, 235, 235)
                pygame.draw.rect(screen, rect_color, rect, border_radius=8)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)
                txt = small_font.render(skin, True, (0, 0, 0))
                screen.blit(txt, txt.get_rect(center=rect.center))

        # Skin preview
        preview = load_skin_preview(selected_skin)
        if preview:
            screen.blit(preview, (850, 400))

        pygame.display.flip()



def death_screen(screen, clock, font, small_font, stats):
    # Fonts
    font = pygame.font.SysFont(None, 64)
    small_font = pygame.font.SysFont(None, 32)

    # Buttons (horizontaal)
    button_width, button_height = 150, 50
    spacing = 50
    retry_button = pygame.Rect(0, 0, button_width, button_height)
    back_button = pygame.Rect(0, 0, button_width, button_height)

    center_x = 750
    y_pos = 610
    retry_button.center = (center_x - button_width//2 - spacing//2, y_pos)
    back_button.center = (center_x + button_width//2 + spacing//2, y_pos)

    # Pre-render texts
    title_text = font.render("YOU HAVE BEEN CAUGHT", True, (255, 0, 0))
    back_text = small_font.render("TO MENU", True, (0, 0, 0))
    retry_text = small_font.render("RETRY", True, (0, 0, 0))

    # Stats surfaces
    stats_surfaces = []
    max_width = 0
    for key, value in stats.items():
        surf = small_font.render(f"{key}: {value}", True, (255, 255, 255))
        stats_surfaces.append(surf)
        max_width = max(max_width, surf.get_width())

    # Stats box parameters
    padding = 20
    box_width = max_width + padding * 2
    box_height = len(stats_surfaces) * 35 + padding * 2
    box_rect = pygame.Rect(center_x - box_width//2, 410, box_width, box_height)

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
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return "play"

        # Achtergrond
        screen.fill((0, 0, 0))
        screen.blit(death_bg, (0, 0))

        dark_overlay = pygame.Surface(screen.get_size())
        dark_overlay.set_alpha(120)  # Pas dit aan voor meer/minder donker
        dark_overlay.fill((0, 0, 0))
        screen.blit(dark_overlay, (0, 0))

        # Titel
        screen.blit(title_text, title_text.get_rect(center=(center_x, 300)))

        # Stats box
        pygame.draw.rect(screen, (50, 50, 50), box_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), box_rect, 3, border_radius=10)

        # Stats text
        for i, surf in enumerate(stats_surfaces):
            screen.blit(surf, surf.get_rect(center=(center_x, box_rect.top + padding + i*35 + 15)))

        # Knoppen
        pygame.draw.rect(screen, (200, 200, 200), retry_button, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), back_button, border_radius=8)
        screen.blit(retry_text, retry_text.get_rect(center=retry_button.center))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()

