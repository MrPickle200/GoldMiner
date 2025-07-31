import pygame
import math
from Obstacle import *
from hand_control import HandTracker
from Generator import Generator

pygame.init()

def collide(obs_1 : Obstacle, obs_2 : Obstacle) -> bool:
    d = distance(obs_1, obs_2)
    if d <= obs_1.get_r() + obs_2.get_r() - 5:
        return True
    return False

def distance(obs_1 : Obstacle, obs_2 : Obstacle) -> float:
    return math.sqrt((obs_1.get_x() - obs_2.get_x()) ** 2 + (obs_1.get_y() - obs_2.get_y()) ** 2)

def main():
    # Setup
    pygame.init()

    SCORE = 0
    WIDTH, HEIGHT = 800, 800
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gold Miner")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32)


    background = pygame.image.load("Assets/background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    claw = Claw(50, 50)
    generator = Generator()
    gold : list[Gold]
    bombs : list[Bomb]
    golds , bombs = generator.spawn_objects(width = 800, height = 800, n_golds = 30, n_bombs = 5)

    hand = HandTracker(show_cam = True)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Main loop
    stretch = False
    pull = False
    running = True

    in_start_menu = True
    in_game = False

    origin_x , origin_y = 0 , 0
    origin_speed = claw.get_speed()

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if in_start_menu and hand.gesture == 1:
            in_start_menu = False
            in_game = True
        
        if in_start_menu:
            print("In start menu.")

        if in_game:
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
                if not (50 <= claw.get_x() <= WIDTH - 50 and  claw.get_y() <= HEIGHT - 50):
                    pull = True

            for gold in golds:
                if collide(claw, gold):
                    if gold.get_m():
                        claw.speed = origin_speed / gold.get_m()
                    gold.pulled_angle = claw.angle
                    gold.is_pulled = True 
                    pull = True
                    for bomb in bombs:
                        if distance(bomb, gold) <= bomb.get_r() + gold.get_r():
                            bomb.exploding = True
                            gold.exist = False
                        
                if distance(Obstacle(origin_x, origin_y), gold) <= claw.get_r() + gold.get_r():
                    SCORE += gold.point
                    gold.exist = False
                    pull = False
                    stretch = False
                    claw.speed = origin_speed

                gold.update(screen, origin_speed)
                
            for bomb in bombs:
                if collide(claw, bomb):
                    SCORE += bomb.point
                    bomb.exploding = True
                    pull = True
                    for other in bombs:
                        if distance(bomb, other) <= bomb.explode_range + other.get_r():
                            other.exploding = True
                            SCORE += bomb.point
                if bomb.exploding:
                    claw.speed = origin_speed
                    for gold in golds:
                        if distance(bomb, gold) <= bomb.explode_range + gold.get_r():
                            gold.exist = False

            golds = [gold for gold in golds if gold.exist]
            bombs = [bomb for bomb in bombs if not bomb.explosion.finished]

            screen.blit(background, (0,0))

            text = font.render(f"SCORE: {SCORE}", True, WHITE)
            text_rect = text.get_rect(topleft=(300, 50))
            padding = 10
            box_rect = pygame.Rect(
                text_rect.left - padding,
                text_rect.top - padding,
                text_rect.width + padding * 2,
                text_rect.height + padding * 2
            )
            pygame.draw.rect(screen, BLACK, box_rect)
            screen.blit(text, (300, 50))

            claw.draw(screen= screen)
            for bomb in bombs:
                bomb.draw(screen= screen)
            for gold in golds:
                gold.draw(screen= screen)
        

        pygame.display.flip()
        clock.tick(35)
    pygame.quit()

if __name__ == "__main__":
    main()