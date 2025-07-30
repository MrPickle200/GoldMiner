import pygame
import math
from Obstacle import *
from hand_control import HandTracker

def collide(obs_1 : Obstacle, obs_2 : Obstacle) -> bool:
    d = distance(obs_1, obs_2)
    if d <= obs_1.get_r() + obs_2.get_r():
        return True
    return False

def distance(obs_1 : Obstacle, obs_2 : Obstacle) -> float:
    return math.sqrt((obs_1.get_x() - obs_2.get_x()) ** 2 + (obs_1.get_y() - obs_2.get_y()) ** 2)

def main():
    # Setup
    pygame.init()
    SCORE = 0
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gold Miner")
    clock = pygame.time.Clock()

    claw = Claw(50, 100)
    golds : list[Gold] = [Gold_1000(600, 600), Gold_500(300, 300), Gold_250(200, 200), Gold_100(400, 200)]
    hand = HandTracker(show_cam = True)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Main loop
    stretch = False
    pull = False
    running = True

    origin_x , origin_y = 0 , 0
    origin_speed = claw.get_speed()

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not stretch and hand.gesture == 1:
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
            
            if not (claw.get_x() <= WIDTH - 100 and  claw.get_y() <= HEIGHT - 100):
                pull = True

        for i in range(len(golds)):
            gold = golds[i]

            if collide(claw, gold):
                if gold.get_m():
                    claw.speed = origin_speed / gold.get_m()
                gold.is_pulled = True 
                pull = True
            
            if distance(Obstacle(origin_x, origin_y), gold) <= claw.get_r() + gold.get_r():
                SCORE += gold.point
                golds.pop(i)
                pull = False
                stretch = False
                claw.speed = origin_speed

            if collide(claw,gold):
                break

        for gold in golds:
            try:
                gold.update(screen, claw.get_x(), claw.get_y(), origin_speed)
            except:
                print("No gold left.")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()