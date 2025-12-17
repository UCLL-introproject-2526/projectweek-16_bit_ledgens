import pygame
import sys

pygame.init()

# =====================
# Window
# =====================
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slide Test")

clock = pygame.time.Clock()
FPS = 60

# =====================
# Player positioning
# =====================
FOOT_X = 360              # vaste voetpositie
GROUND_Y = HEIGHT - 20    # grondlijn

# =====================
# Helper: load & scale
# =====================
def load_and_scale(path, target_h):
    img = pygame.image.load(path).convert_alpha()
    scale = target_h / img.get_height()
    new_w = int(img.get_width() * scale)
    return pygame.transform.smoothscale(img, (new_w, target_h))

TARGET_H = 120

# =====================
# Load poses
# =====================
pose_idle      = load_and_scale("assets/images/slide_deel1.png", TARGET_H)
pose_crouch    = load_and_scale("assets/images/slide_deel2.png", TARGET_H)
pose_slide     = load_and_scale("assets/images/slide_deel3.png", TARGET_H)
pose_standup   = load_and_scale("assets/images/slide_deel4.png", TARGET_H)
pose_idle_end  = load_and_scale("assets/images/slide_einde.png", TARGET_H)

# Volgorde van animatie
slide_frames = [
    pose_idle,
    pose_crouch,
    pose_slide,
    pose_standup,
    pose_idle_end
]

# =====================
# Slide logic
# =====================
state = "idle"        # idle | sliding_in | slide_hold | sliding_out
frame_index = 0
frame_speed = 0.25
down_held = False

# =====================
# Main loop
# =====================
running = True
while running:
    clock.tick(FPS)

    # -----------------
    # Events
    # -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and state == "idle":
                state = "sliding_in"
                frame_index = 0
                down_held = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                down_held = False
                if state == "slide_hold":
                    state = "sliding_out"
                    frame_index = 3  # stand up frame

    # -----------------
    # Update animation
    # -----------------
    if state == "sliding_in":
        frame_index += frame_speed
        if frame_index >= 2:
            frame_index = 2
            state = "slide_hold"

    elif state == "slide_hold":
        frame_index = 2  # blijf liggen zolang toets vast is

    elif state == "sliding_out":
        frame_index += frame_speed
        if frame_index >= len(slide_frames):
            frame_index = 0
            state = "idle"

    # -----------------
    # Draw
    # -----------------
    WIN.fill((255, 255, 255))

    # grondlijn (debug)
    pygame.draw.line(WIN, (0, 0, 0), (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    current_frame = slide_frames[int(frame_index)]
    rect = current_frame.get_rect()
    rect.midbottom = (FOOT_X, GROUND_Y)

    WIN.blit(current_frame, rect)

    pygame.display.update()

pygame.quit()
sys.exit()
