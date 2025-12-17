import pygame
import sys

pygame.init()

# =====================
# Window
# =====================
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump Demo (2 Sheets)")

clock = pygame.time.Clock()
FPS = 45

# =====================
# Ground
# =====================
GROUND_Y = HEIGHT - 100

# =====================
# Player
# =====================
player_x = 100
player_vel_x = 4

# Jump physics
is_jumping = False
velocity_y = 0
GRAVITY = 1
JUMP_STRENGTH = -18

# =====================
# Helper: load frames
# =====================
def load_frames(sheet, num_frames, target_height):
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // num_frames

    scale_factor = target_height / sheet_height
    target_width = int(frame_width * scale_factor)

    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(
            pygame.Rect(i * frame_width, 0, frame_width, sheet_height)
        )
        frame = pygame.transform.smoothscale(
            frame, (target_width, target_height)
        )
        frames.append(frame)

    return frames, target_width

# =====================
# Load sprite sheets
# =====================
jump_start_sheet = pygame.image.load("assets/images/jump_start.png").convert_alpha()
jump_fall_sheet = pygame.image.load("assets/images/jump_fall.png").convert_alpha()

TARGET_HEIGHT = 120

# PAS AAN indien nodig
JUMP_START_FRAMES = 3
JUMP_FALL_FRAMES = 3

jump_start_frames, TARGET_WIDTH = load_frames(
    jump_start_sheet, JUMP_START_FRAMES, TARGET_HEIGHT
)
jump_fall_frames, _ = load_frames(
    jump_fall_sheet, JUMP_FALL_FRAMES, TARGET_HEIGHT
)

# =====================
# Animation
# =====================
jump_start_index = 0.0
jump_fall_index = 0.0
jump_start_playing = False

ANIM_SPEED = 0.2

# =====================
# Start position
# =====================
player_y = GROUND_Y - TARGET_HEIGHT

# =====================
# Game loop
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
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                velocity_y = JUMP_STRENGTH
                jump_start_playing = True
                jump_start_index = 0

    # -----------------
    # Horizontal movement
    # -----------------
    player_x += player_vel_x
    if player_x > WIDTH:
        player_x = -TARGET_WIDTH

    # -----------------
    # Jump physics & animation
    # -----------------
    if is_jumping:
        velocity_y += GRAVITY
        player_y += velocity_y

        # Jump start animation (play once)
        if jump_start_playing:
            jump_start_index += ANIM_SPEED
            if jump_start_index >= len(jump_start_frames):
                jump_start_index = len(jump_start_frames) - 1
                jump_start_playing = False

        # Jump fall animation (loop)
        else:
            jump_fall_index += ANIM_SPEED
            if jump_fall_index >= len(jump_fall_frames):
                jump_fall_index = 0

        # Landing
        if player_y >= GROUND_Y - TARGET_HEIGHT:
            player_y = GROUND_Y - TARGET_HEIGHT
            is_jumping = False
            velocity_y = 0
            jump_start_index = 0
            jump_fall_index = 0
            jump_start_playing = False

    # -----------------
    # Draw
    # -----------------
    WIN.fill((255, 255, 255))

    # Ground line (debug)
    pygame.draw.line(WIN, (0, 0, 0), (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    if is_jumping:
        if jump_start_playing:
            frame = jump_start_frames[int(jump_start_index)]
        else:
            frame = jump_fall_frames[int(jump_fall_index)]
    else:
        frame = jump_start_frames[0]  # idle frame

    WIN.blit(frame, (player_x, player_y))

    pygame.display.update()

pygame.quit()
sys.exit()
