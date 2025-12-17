import pygame

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game")

death_bg = pygame.image.load("assets/images/death.png").convert()
death_bg = pygame.transform.scale(death_bg, (WIDTH, HEIGHT))

def menu(screen, clock, small_font, menu_bg):
    play_button = pygame.Rect(650, 300, 200, 60)
    scoreboard_button = pygame.Rect(650, 370, 200, 60)
    quit_button = pygame.Rect(650, 440, 200, 60)

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    # ====== Name Input ======
    name = ""
    input_active = True
    input_box = pygame.Rect(550, 230, 400, 50)
    input_color_active = (255, 255, 255)
    input_color_inactive = (200, 200, 200)

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
                if play_button.collidepoint(event.pos):
                    return "play"
                if scoreboard_button.collidepoint(event.pos):
                    return "scoreboard"
                if quit_button.collidepoint(event.pos):
                    return "quit"
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                else:
                    if len(name) < 20:  # max name length
                        name += event.unicode

        screen.blit(menu_bg, (0, 0))

        color = input_color_active if input_active else input_color_inactive
        pygame.draw.rect(screen, color, input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 3)

        name_surf = font.render(name or "Enter username", True, (0, 0, 0))
        screen.blit(name_surf, name_surf.get_rect(center=input_box.center))


        for button, color, text in [
            (play_button, (0, 200, 0), "PLAY"),
            (scoreboard_button, (100, 100, 255), "SCOREBOARD"),
            (quit_button, (200, 0, 0), "QUIT")
        ]:
            btn_color = tuple(max(c - 50, 0) for c in color) if button.collidepoint(mouse_pos) else color
            pygame.draw.rect(screen, btn_color, button)
            pygame.draw.rect(screen, (0, 0, 0), button, 3)

            text_surf = small_font.render(text, True, (0, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center=button.center))

        pygame.display.flip()



def scoreboard(screen, clock, font):

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    back_button = pygame.Rect(0, 0, 120, 40)
    back_button.center = (400, 500)
    small_font = pygame.font.SysFont(None, 28)

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

        screen.fill((255, 255, 255))

        title = font.render("SCOREBOARD", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(400, 300)))

        mouse_pos = pygame.mouse.get_pos()
        btn_color = (150, 150, 150) if back_button.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(screen, btn_color, back_button)
        pygame.draw.rect(screen, (0, 0, 0), back_button, 3)  # outline

        back_text = small_font.render("BACK", True, (0, 0, 0))
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
