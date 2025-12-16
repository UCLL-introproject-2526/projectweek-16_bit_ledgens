class Background:
    def __init__(self, bg):
        self.bg = bg
        self.scroll = 0
        self.speed = 3
        self.width = bg.get_width()

    def draw(self, screen):
        self.scroll -= self.speed
        if abs(self.scroll) > self.width:
            self.scroll = 0

        screen.blit(self.bg, (self.scroll, 0))
        screen.blit(self.bg, (self.scroll + self.width, 0))
