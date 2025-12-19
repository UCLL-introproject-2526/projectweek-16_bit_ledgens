import pygame

def how_to_play(screen, clock):
    img = pygame.image.load("assets/images/how_to_play.png")
    img = pygame.transform.scale(img, screen.get_size())

    # oude input wissen
    pygame.event.clear()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            #  ALLEEN toetsenbord
            if event.type == pygame.KEYUP:
                return "play"

        screen.blit(img, (0, 0))
        pygame.display.flip()
