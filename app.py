import pygame                  # Pygame importeren voor grafische functionaliteit
from pygame.display import flip # flip() wordt gebruikt om de back buffer naar het scherm te kopiëren

# Initialiseer Pygame
pygame.init()

# Functie om het hoofdvenster en de surface te maken
def create_main_surface():
    screen_size = (1024, 768)         # breedte en hoogte van het venster
    surface = pygame.display.set_mode(screen_size)  # maak het venster en return de surface
    return surface                     # surface is het canvas waarop we tekenen

# Functie om de surface te wissen
def clear_surface(surface):
    surface.fill((0, 80, 0))           # vul de hele surface met groen

# Functie om één frame te renderen
def render_frame(surface, x):
    clear_surface(surface)             # wis eerst de vorige frame
    pygame.draw.circle(                # teken een cirkel
        surface,                       # teken op deze surface
        (255, 0, 0),                   # kleur: blauw
        (x, 250),                      # positie van het midden van de cirkel
        40                              # straal van de cirkel
    )
    flip()                             # kopieer de back buffer naar de front buffer om te laten zien

# Main programma
surface = create_main_surface()        # maak het venster en sla de surface op
x = 60                                 # startpositie van de cirkel (horizontaal)

running = True                         # boolean om de main loop te controleren
while running:
    for event in pygame.event.get():   # loop door alle events
        if event.type == pygame.QUIT: # als het kruisje wordt aangeklikt
            running = False            # stop de loop

    render_frame(surface, x)           # teken het frame met de huidige positie
    x += 0.1                              # verhoog de x-positie, zodat de cirkel naar rechts beweegt

# Sluit Pygame netjes af als de loop stopt
pygame.quit()


