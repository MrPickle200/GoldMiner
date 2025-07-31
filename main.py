import pygame
import math
from Obstacle import *
from hand_control import HandTracker
from Generator import Generator

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

    generator = Generator()
    golds, bombs = generator.spawn_objects(width = 800, height = 800, n_golds=15, n_bombs=5)

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

        # Close palm to shoot
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
            # Pull back if the claw went out the screen
            if not (claw.get_x() <= WIDTH - 50 and  claw.get_y() <= HEIGHT - 50):
                pull = True

        for gold in golds:
            if collide(claw, gold):
                if gold.get_m():
                    claw.speed = origin_speed / gold.get_m()
                gold.is_pulled = True 
                pull = True
            if distance(Obstacle(origin_x, origin_y), gold) <= claw.get_r() + gold.get_r():
                SCORE += gold.point
                gold.exist = False
                pull = False
                stretch = False
                claw.speed = origin_speed

            try:
                gold.update(screen, claw.get_x(), claw.get_y(), origin_speed)
            except:
                print("No gold left.")

        for bomb in bombs:
            if collide(claw, bomb):
                bomb.exploding = True
                pull = True
                for gold in golds:
                    if distance(bomb, gold) < bomb.explode_range:
                        gold.exist = False
            try:
                bomb.update(screen = screen)
            except:
                print("No bomb left.")

        golds = [gold for gold in golds if gold.exist]
        bombs = [bomb for bomb in bombs if not bomb.explosion.finished]
            
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()