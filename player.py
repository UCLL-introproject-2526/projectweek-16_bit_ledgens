import pygame
from settings import *


class Player:
    def __init__(self, ground):
        # =====================
        # BASIS
        # =====================
        self.rect = pygame.Rect(
            PLAYER_X,
            ground.top - PLAYER_HEIGHT,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

        self.vel_y = 0
        self.base_y = self.rect.y

        self.is_jumping = False
        self.is_sliding = False

        # hitbox
        self.hitbox = self.rect.copy()

        # =====================
        # RUN
        # =====================
        run_sheet = pygame.image.load("assets/persoon3.PNG").convert_alpha()
        self.run_frames = self._load_run_sheet(run_sheet, 3)

        self.run_index = 0.0
        self.run_speed = 0.25
        self.run_offsets = [
            0,
            int(PLAYER_HEIGHT * 0.03),
            int(PLAYER_HEIGHT * 0.01)
        ]
        self.current_frame = self.run_frames[0]

        # =====================
        # JUMP
        # =====================
        self.jump_start_frames = self._load_jump_sheet(
            pygame.image.load("assets/jump_start.png").convert_alpha(), 3
        )
        self.jump_fall_frames = self._load_jump_sheet(
            pygame.image.load("assets/jump_fall.png").convert_alpha(), 3
        )

        self.jump_start_index = 0.0
        self.jump_fall_index = 0.0
        self.jump_start_playing = False
        self.jump_anim_speed = 0.2

        # =====================
        # SLIDE
        # =====================
        self.slide_frames = [
            self._load_slide_image("assets/slide_deel1.png"),
            self._load_slide_image("assets/slide_deel2.png"),
            self._load_slide_image("assets/slide_deel3.png"),
            self._load_slide_image("assets/slide_deel4.png"),
            self._load_slide_image("assets/slide_einde.png"),
        ]

        self.slide_index = 0.0
        self.slide_speed = 0.50
        self.slide_state = "idle"
        self.down_held = False

    # =====================
    # LOADERS
    # =====================
    def _load_run_sheet(self, sheet, frames):
        w = sheet.get_width() // frames
        h = sheet.get_height()
        result = []

        for i in range(frames):
            frame = sheet.subsurface((i * w, 0, w, h))
            frame = pygame.transform.scale(
                frame, (PLAYER_WIDTH, PLAYER_HEIGHT)
            )
            result.append(frame)

        return result

    def _load_jump_sheet(self, sheet, frames):
        w = sheet.get_width() // frames
        h = sheet.get_height()

        jump_w = int(PLAYER_WIDTH * JUMP_SCALE)
        jump_h = int(PLAYER_HEIGHT * JUMP_SCALE)

        result = []
        for i in range(frames):
            frame = sheet.subsurface((i * w, 0, w, h))
            frame = pygame.transform.scale(frame, (jump_w, jump_h))
            result.append(frame)

        return result

    def _load_slide_image(self, path):
        img = pygame.image.load(path).convert_alpha()

        slide_height = int(PLAYER_HEIGHT * SLIDE_SCALE)
        scale = slide_height / img.get_height()

        return pygame.transform.smoothscale(img,(int(img.get_width() * scale), slide_height)
    )


    # =====================
    # RUN
    # =====================
    def run(self):
        self.run_index += self.run_speed
        if self.run_index >= len(self.run_frames):
            self.run_index = 0

        i = int(self.run_index)
        self.current_frame = self.run_frames[i]
        self.rect.y = self.base_y - self.run_offsets[i]

    # =====================
    # JUMP
    # =====================
    def start_jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel_y = JUMP_FORCE
            self.jump_start_playing = True
            self.jump_start_index = 0
            self.jump_fall_index = 0

    def update_jump(self, ground):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.jump_start_playing:
            self.jump_start_index += self.jump_anim_speed
            if self.jump_start_index >= len(self.jump_start_frames):
                self.jump_start_playing = False
        else:
            self.jump_fall_index += self.jump_anim_speed
            if self.jump_fall_index >= len(self.jump_fall_frames):
                self.jump_fall_index = 0

        if self.rect.bottom >= ground.top:
            self.rect.bottom = ground.top
            self.base_y = self.rect.y
            self.vel_y = 0
            self.is_jumping = False

    # =====================
    # SLIDE
    # =====================
    def update_slide(self):
        if self.slide_state == "sliding_in":
            self.slide_index += self.slide_speed
            if self.slide_index >= 2:
                self.slide_index = 2
                self.slide_state = "slide_hold"

        elif self.slide_state == "slide_hold":
            self.slide_index = 2
            if not self.down_held:
                self.slide_state = "sliding_out"
                self.slide_index = 3

        elif self.slide_state == "sliding_out":
            self.slide_index += self.slide_speed
            if self.slide_index >= len(self.slide_frames):
                self.slide_state = "idle"
                self.slide_index = 0
                self.is_sliding = False

    # =====================
    # UPDATE
    # =====================
    def update(self, keys, ground):
        # start slide
        if keys[pygame.K_DOWN] and not self.is_sliding and not self.is_jumping:
            self.is_sliding = True
            self.slide_state = "sliding_in"
            self.slide_index = 0
            self.down_held = True

        if not keys[pygame.K_DOWN]:
            self.down_held = False

        # start jump
        if keys[pygame.K_UP] and not self.is_jumping and not self.is_sliding:
            self.start_jump()

        # state logic
        if self.is_jumping:
            self.update_jump(ground)
        elif self.is_sliding:
            self.update_slide()
        else:
            self.run()

        # hitbox
        self.hitbox.x = self.rect.x + HITBOX_MARGIN_X // 2
        self.hitbox.width = self.rect.width - HITBOX_MARGIN_X

        if self.is_sliding:
            self.hitbox.height = int(self.rect.height * SLIDE_SCALE)
            self.hitbox.y = self.rect.bottom - self.hitbox.height
        else:
            self.hitbox.height = self.rect.height - HITBOX_MARGIN_Y
            self.hitbox.y = self.rect.y + HITBOX_MARGIN_Y // 2

    # =====================
    # DRAW
    # =====================
    def draw(self, screen):
        if self.is_sliding:
            frame = self.slide_frames[int(self.slide_index)]
            rect = frame.get_rect(midbottom=self.rect.midbottom)
            screen.blit(frame, rect)

        elif self.is_jumping:
            if self.jump_start_playing:
                frame = self.jump_start_frames[int(self.jump_start_index)]
            else:
                frame = self.jump_fall_frames[int(self.jump_fall_index)]

            rect = frame.get_rect(midbottom=self.rect.midbottom)
            screen.blit(frame, rect)

        else:
            screen.blit(self.current_frame, self.rect)
