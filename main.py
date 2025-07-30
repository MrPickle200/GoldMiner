import pygame
import math
from Obstacle import *

def collide(obs_1 : Obstacle, obs_2 : Obstacle) -> bool:
    d = math.sqrt((obs_1.get_x() - obs_2.get_x()) ** 2 + (obs_1.get_y() - obs_2.get_y()) ** 2)
    if d <= obs_1.get_r() + obs_2.get_r():
        return True
    return False

def main():
    # Setup
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gold Miner")
    clock = pygame.time.Clock()
    claw = Claw(50, 100, 9)
    golds = [Gold_1000(400, 400, 156)]

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Main loop
    stretch = False
    pull = False
    running = True

    origin_x , origin_y = 0 , 0
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not stretch and event.type == pygame.MOUSEBUTTONDOWN:
                stretch = True
                origin_x = claw.get_x()
                origin_y = claw.get_y()
        if not stretch:
            claw.rotate(screen)
        if stretch:
            if not pull:
                claw.stretch(screen)
            else:
                claw.pull(screen, origin_x, origin_y)

            if claw.get_x() <= origin_x and claw.get_y() <= origin_y:
                stretch = False
                pull = False
            elif not (claw.get_x() <= WIDTH - 200 and  claw.get_y() <= HEIGHT - 200):
                pull = True
        for gold in golds:
            if collide(claw, gold):
                print("COLLIDED.")
                pull = True 
            gold.update(screen, pull, claw.get_x(), claw.get_y())
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()