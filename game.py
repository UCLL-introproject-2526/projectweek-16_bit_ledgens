import pygame


screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# Objecten
grond = pygame.Rect(0, 350, 800, 50)
speler = pygame.Rect(100, 100, 40, 40)
obstakel = pygame.Rect(800, 310, 30, 40)

zwaartekracht = 1
snelheid_y = 0

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and speler.bottom == grond.top:
        snelheid_y = -15

    # Speler beweging
    snelheid_y += zwaartekracht
    speler.y += snelheid_y

    if speler.colliderect(grond):
        speler.bottom = grond.top
        snelheid_y = 0

    # Obstakel beweging
    obstakel.x -= 6
    if obstakel.right < 0:
        obstakel.x = 800

    # Botsing = dood
    if speler.colliderect(obstakel):
        print("Game Over")
        running = False

    # Tekenen
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (100, 200, 100), grond)
    pygame.draw.rect(screen, (255, 255, 0), speler)
    pygame.draw.rect(screen, (200, 50, 50), obstakel)

    pygame.display.flip()

pygame.quit()
