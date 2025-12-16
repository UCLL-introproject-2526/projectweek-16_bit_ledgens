import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 90

# =====================
# SCHERM
# =====================
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teacher Run")

# =====================
# GROND
# =====================
grond = pygame.Rect(0, HEIGHT - 250, WIDTH, 50)

# =====================
# SPELER
# =====================
speler = pygame.Rect(120, grond.top - 160, 160, 160)
originele_hoogte = speler.height
is_bukken = False

# kleinere hitbox
hitbox_margin = 40
hitbox = pygame.Rect(speler.x, speler.y, speler.width, speler.height)

# =====================
# ZWAARTEKRACHT
# =====================
zwaartekracht = 1
snelheid_y = 0

# =====================
# AFBEELDINGEN
# =====================
bg = pygame.image.load("bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (int(WIDTH * 1.1), int(HEIGHT * 1.1)))
bg.set_alpha(180)
bg_width = bg.get_width()

grond_img = pygame.image.load("grond.png").convert_alpha()
grond_img = pygame.transform.scale(grond_img, (WIDTH, HEIGHT - grond.top))

speler_img = pygame.image.load("karakter.png").convert_alpha()
speler_img = pygame.transform.scale(speler_img, (160, 160))

liniaal_img = pygame.image.load("liniaal.png").convert_alpha()
liniaal_img = pygame.transform.scale(liniaal_img, (60, grond.top))

rugzak_img = pygame.image.load("rugzak.png").convert_alpha()
rugzak_img = pygame.transform.scale(rugzak_img, (70, 70))

bank_img = pygame.image.load("bank.png").convert_alpha()
bank_img = pygame.transform.scale(bank_img, (60, 60))

# =====================
# OBSTAKELS (VASte SEQUENCE)
# =====================
afstand = 520
sequence = [
    ("grond", "rugzak"),
    ("lucht", "liniaal"),
    ("grond", "bank"),
    ("lucht", "liniaal")
]

obstakels = []
start_x = WIDTH + 300
opening = 220
lucht_offset = 100
lucht_extra_offset = 280

for i, (soort, img) in enumerate(sequence):
    x = start_x + i * afstand

    if soort == "lucht":
        x += lucht_extra_offset


    if soort == "grond":
        if img == "rugzak":
            rect = pygame.Rect(x, grond.top - 70, 70, 70)
        else:
            rect = pygame.Rect(x, grond.top - 60, 100, 60)

    else:  # lucht (liniaal)
        rect = pygame.Rect(x, lucht_offset, 60, grond.top - opening)

    obstakels.append({"rect": rect, "type": soort, "img": img})


scroll = 0
bg_speed = 3
tiles = math.ceil(WIDTH / bg_width) + 2
grond_x = 0
grond_speed = 6


running = True
while running:
    clock.tick(FPS)

    # Achtergrond
    for i in range(tiles):
        screen.blit(bg, (i * bg_width + scroll - 100, -120))

    scroll -= bg_speed
    if abs(scroll) > bg_width:
        scroll = 0

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Springen
    if keys[pygame.K_UP] and speler.bottom == grond.top:
        snelheid_y = -23

    # Bukken
    if keys[pygame.K_DOWN]:
        if not is_bukken:
            speler.height = originele_hoogte // 2
            speler.y += originele_hoogte // 2
            is_bukken = True
    else:
        if is_bukken:
            speler.y -= originele_hoogte // 2
            speler.height = originele_hoogte
            is_bukken = False

    # Beweging
    snelheid_y += zwaartekracht
    speler.y += snelheid_y

    if speler.colliderect(grond):
        speler.bottom = grond.top
        snelheid_y = 0

    # Hitbox
    hitbox.x = speler.x + hitbox_margin // 2
    hitbox.y = speler.y + hitbox_margin // 2
    hitbox.width = speler.width - hitbox_margin
    hitbox.height = speler.height - hitbox_margin

    # Obstakels bewegen
    for i, obs in enumerate(obstakels):
        obs["rect"].x -= 6
        if obs["rect"].right < 0:
            obs["rect"].x = WIDTH + i * afstand

    # Botsing
    for obs in obstakels:
        if hitbox.colliderect(obs["rect"]):
            print("GESNAPT DOOR DE LEERKRACHT!")
            running = False

    # Grond scrollen
    grond_x -= grond_speed
    if grond_x <= -WIDTH:
        grond_x = 0

    # =====================
    # TEKENEN
    # =====================
    screen.blit(grond_img, (grond_x, grond.top))
    screen.blit(grond_img, (grond_x + WIDTH, grond.top))
    screen.blit(speler_img, (speler.x, speler.y))

    for obs in obstakels:
        rect = obs["rect"]

        if obs["img"] == "rugzak":
            screen.blit(rugzak_img, rect)

        elif obs["img"] == "bank":
            screen.blit(bank_img, rect)

        else:  # liniaal → bodem uitlijnen
            bodem = rect.bottom
            screen.blit(
                liniaal_img,
                (rect.x, bodem - liniaal_img.get_height())
            )

    pygame.display.update()

pygame.quit()
