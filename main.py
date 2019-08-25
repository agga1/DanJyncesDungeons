import pygame

pygame.init()

# SCREEN
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Dan Jynce's Dungeons")

# TIME
clock = pygame.time.Clock()

while True:

    clock.tick(90)

    pygame.draw.line(screen, (255, 255, 255), (20, 30), (200, 300), 5)

    # QUIT GAME
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit(1)

    pygame.display.flip()
