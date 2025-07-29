import pygame
import math
import sys
from Obstacle import Claw

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()
claw = Claw(400, 100, 5)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main loop
stretch = False
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not stretch and event.type == pygame.MOUSEBUTTONDOWN:
            stretch = True
    if not stretch:
        claw.rotate(screen)
    if stretch:
        claw.stretch(screen)
        if not (100 <= claw.x <= WIDTH - 100 and  claw.y <= HEIGHT):
            stretch = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()