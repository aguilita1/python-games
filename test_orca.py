import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Alpha Test")

# Load image
img = pygame.image.load('orca-425x250.png').convert_alpha()
img.set_alpha(None)  # Disable global alpha
img.fill((255, 0, 0))  # Fill with red — should completely override image
# img = pygame.Surface((425, 250))
# img.fill((255, 0, 0))

print('Image size:', img.get_size(), 'alpha:', img.get_alpha(), 'flags:', img.get_flags(), 'bitsize:', img.get_bitsize())

while True:
    screen.fill((0, 0, 0))  # Black background
    screen.blit(img, (100, 100))  # Draw red box
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
