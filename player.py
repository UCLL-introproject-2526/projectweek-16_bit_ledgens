import pygame
from settings import *

SKIN_BASE_PATH = "assets/images/skins"
SKIN_SLIDE_SCALES = {
    "vrouw": 0.65,   
}

SKIN_JUMP_SPEEDS = {
    "sonni": 0.15,   
}

SKIN_SLIDE_SPEEDS = {
    "vrouw": 0.12
}




class Player:
    def __init__(self, ground, skin="sonni"):
        # =====================
        # BASIS
        # =====================
        self.ground = ground
        self.skin = skin
        self.slide_scale = SKIN_SLIDE_SCALES.get(self.skin, SLIDE_SCALE)


        self.rect = pygame.Rect(
            PLAYER_X,
            ground.top - PLAYER_HEIGHT,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

        self.hitbox = self.rect.copy()

        self.vel_y = 0
        self.base_y = self.rect.y

        self.is_jumping = False
        self.is_sliding = False

        # =====================
        # ANIMATIE STATE
        # =====================
        self.run_index = 0.0
        self.jump_start_index = 0.0
        self.jump_fall_index = 0.0
        self.slide_index = 0.0

        self.jump_start_playing = False
        self.slide_state = "idle"
        self.down_held = False

        self.run_speed = 0.2
        self.jump_anim_speed = SKIN_JUMP_SPEEDS.get(self.skin, 0.2)
        self.slide_speed = SKIN_SLIDE_SPEEDS.get(self.skin, 0.3)

        self.run_offsets = [
            0,
            int(PLAYER_HEIGHT * 0.03),
            int(PLAYER_HEIGHT * 0.01)
        ]

        # =====================
        # LOAD SKIN (NIEUW)
        # =====================
        self.load_skin()

        # veilig startframe
        self.current_frame = self.run_frames[0]

    # =====================
    # SKIN LOADER (NIEUW)
    # =====================
    def load_skin(self):
        base = f"{SKIN_BASE_PATH}/{self.skin}"

        # RUN
        run_sheet = pygame.image.load(f"{base}/run.png").convert_alpha()
        self.run_frames = self._load_sheet(
            run_sheet, 3, PLAYER_WIDTH, PLAYER_HEIGHT
        )

        # JUMP
        self.jump_start_frames = self._load_sheet(
            pygame.image.load(f"{base}/jump_start.png").convert_alpha(),
            3,
            int(PLAYER_WIDTH * JUMP_SCALE),
            int(PLAYER_HEIGHT * JUMP_SCALE),
        )

        self.jump_fall_frames = self._load_sheet(
            pygame.image.load(f"{base}/jump_fall.png").convert_alpha(),
            3,
            int(PLAYER_WIDTH * JUMP_SCALE),
            int(PLAYER_HEIGHT * JUMP_SCALE),
        )

        # SLIDE
        self.slide_frames = []
        for i in range(1, 5):
            img = pygame.image.load(f"{base}/slide_{i}.png").convert_alpha()
            self.slide_frames.append(self._scale_slide(img))

        img = pygame.image.load(f"{base}/slide_end.png").convert_alpha()
        self.slide_frames.append(self._scale_slide(img))

    # =====================
    # LOAD HELPERS
    # =====================
    def _load_sheet(self, sheet, frames, w, h):
        frame_w = sheet.get_width() // frames
        frame_h = sheet.get_height()
        result = []

        for i in range(frames):
            frame = sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
            result.append(pygame.transform.scale(frame, (w, h)))

        return result

    def _scale_slide(self, img):
        slide_h = int(PLAYER_HEIGHT * self.slide_scale)
        scale = slide_h / img.get_height()
        return pygame.transform.smoothscale(
            img, (int(img.get_width() * scale), slide_h)
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

    def update_jump(self,keys):
        if keys[pygame.K_DOWN]:
            self.vel_y += GRAVITY * FAST_FALL_MULTIPLIER
        else:
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

        if self.rect.bottom >= self.ground.top:
            self.rect.bottom = self.ground.top
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
        if keys[pygame.K_DOWN] and not self.is_sliding and not self.is_jumping:
            self.is_sliding = True
            self.slide_state = "sliding_in"
            self.slide_index = 0
            self.down_held = True

        if not keys[pygame.K_DOWN]:
            self.down_held = False

        if keys[pygame.K_UP] and not self.is_jumping and not self.is_sliding:
            self.start_jump()

        if self.is_jumping:
            self.update_jump(keys)
        elif self.is_sliding:
            self.update_slide()
        else:
            self.run()

        # hitbox
        self.hitbox.x = self.rect.x + HITBOX_MARGIN_X // 2
        self.hitbox.width = self.rect.width - HITBOX_MARGIN_X

        if self.is_sliding:
            self.hitbox.height = int(self.rect.height * self.slide_scale)
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
            frame = (
                self.jump_start_frames[int(self.jump_start_index)]
                if self.jump_start_playing
                else self.jump_fall_frames[int(self.jump_fall_index)]
            )
            rect = frame.get_rect(midbottom=self.rect.midbottom)
            screen.blit(frame, rect)

        else:
            screen.blit(self.current_frame, self.rect)
