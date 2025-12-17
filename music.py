import pygame

pygame.init()
pygame.mixer.init()


class SoundObject:
    def __init__(self, sound_file):
        self.sound = pygame.mixer.Sound(sound_file)

    def play_sound(self):
        self.sound.play()

sound_hub = SoundObject("assets/music/hub_music.mp3")