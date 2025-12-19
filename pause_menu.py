import pygame

def pause_menu(screen, clock):
    WIDTH, HEIGHT = screen.get_size()

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)

    title = font.render("PAUSED", True, (255, 255, 255))
    hint = small_font.render("Press P to continue", True, (200, 200, 200))

    pygame.event.clear()  #  voorkomt instant resume

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"

        screen.blit(overlay, (0, 0))
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        screen.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))
        pygame.display.flip()
