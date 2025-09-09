import pygame
import math
from Obstacle import * 
from Hand_control import HandTracker
from Generator import Generator
from Button import Button



def collide(obs_1 : Obstacle, obs_2 : Obstacle) -> bool:
    d = distance(obs_1, obs_2)
    if d <= obs_1.get_r() + obs_2.get_r() - 2:
        return True
    return False

def distance(obs_1 : Obstacle, obs_2 : Obstacle) -> float:
    return math.sqrt((obs_1.get_x() - obs_2.get_x()) ** 2 + (obs_1.get_y() - obs_2.get_y()) ** 2)

def draw_time_box(screen : pygame.Surface, in_game_time, TIME, WAIT_TIME, font):
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    WIDTH = screen.get_size()[0]
    elapsed = pygame.time.get_ticks() - in_game_time
    time_left = TIME + WAIT_TIME - elapsed // 1000
    text = font.render(f"Time left: {time_left}", True, WHITE)
    text_rect = text.get_rect(topleft=(WIDTH - 350, 50))
    padding = 10
                
    box_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding,
            text_rect.width + padding * 2,
            text_rect.height + padding * 2
                )
    
    pygame.draw.rect(screen, BLACK, box_rect)
    screen.blit(text, (WIDTH - 350, 50))

def draw_score_box(screen : pygame.Surface, SCORE, font):
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    WIDTH = screen.get_size()[0]
    text = font.render(f"SCORE: {SCORE}", True, WHITE)
    text_rect = text.get_rect(topleft=(WIDTH - 600, 50))
    padding = 10
                
    box_rect = pygame.Rect(
                    text_rect.left - padding,
                    text_rect.top - padding,
                    text_rect.width + padding * 2,
                    text_rect.height + padding * 2
                )

    pygame.draw.rect(screen, BLACK, box_rect)
    screen.blit(text, (WIDTH - 600, 50))

def time_left(in_game_time : int, TIME : int, WAIT_TIME : int) -> int:
    elapsed = pygame.time.get_ticks() - in_game_time
    return TIME + WAIT_TIME - elapsed // 1000

def main():
    # Setup
    pygame.init()

    SCORE = 0
    WIDTH, HEIGHT = 1200, 800
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gold Miner")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32)

    setting_button = Button("Animations/settingbutton.png")

    background = pygame.image.load("BackGrounds/background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Main loop
    stretch = False
    pull = False
    running = True

    TIME = 60
    WAIT_TIME = 3
    GOLDS = 40
    BOMBS = 15

    in_start_menu : bool = True
    in_pause_menu : bool = False
    in_game : bool = False
    end_game : bool = False

    claw = Claw(50, 120)
    generator = Generator()
    gold : list[Gold]
    bombs : list[Bomb]
    golds , bombs = generator.spawn_objects(width = WIDTH, height = HEIGHT, n_golds = GOLDS, n_bombs = BOMBS)

    hand = HandTracker(show_cam = True)

    origin_x , origin_y = 0, 0
    origin_speed = claw.get_speed()

    game_start_time = None
    in_game_time = None
    game_active = False 


    while running:
        screen.fill(BLACK)
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                resume_rect = pygame.Rect(520, 290, 150, 50)
                quit_rect = pygame.Rect(520, 360, 150, 50)
                mouse_x , mouse_y = mouse_pos

                if setting_button.is_pressed(mouse_pos= mouse_pos):
                    in_pause_menu = True
                    
                if in_pause_menu:
                    if resume_rect.x < mouse_x < resume_rect.x + resume_rect.width \
                    and resume_rect.y < mouse_y < resume_rect.y + resume_rect.height:

                        in_pause_menu = False

                    elif quit_rect.x < mouse_x < quit_rect.x + quit_rect.width \
                        and quit_rect.y < mouse_y < quit_rect.y + quit_rect.height:

                    # RESET
                        in_start_menu = True
                        in_pause_menu = False
                        in_game = False
                        end_game = False

                        origin_x , origin_y = 0, 0
                        SCORE = 0
                        golds , bombs = generator.spawn_objects(width = WIDTH, height = HEIGHT, n_golds = GOLDS, n_bombs = BOMBS)
                        
        # DRAW MAIN MENU. IF HAND GESTURE IS CLOSE, GAME START

        if in_start_menu:
            if hand.gesture == 1:
                in_start_menu = False
                in_game = True           
                game_start_time = pygame.time.get_ticks()
                in_game_time = pygame.time.get_ticks()
                game_active =False

            text_1 = pygame.font.SysFont("Arial", 64).render("FDS GOLD MINER", True, WHITE)
            screen.blit(text_1, (WIDTH // 2 - 200, HEIGHT // 2 - 150))

            text_2 = pygame.font.SysFont("Arial", 32).render("Close your hand to start the game.", True, WHITE)
            screen.blit(text_2, (WIDTH // 2 - 180, HEIGHT // 2))
   
        if in_game:

            if not game_active:
                # Show countdown or wait
                elapsed = pygame.time.get_ticks() - game_start_time
                if elapsed >= 3000:
                    game_active = True
                else:
                    # Draw countdown timer 
                    countdown = WAIT_TIME - elapsed // 1000
                    text_surface = font.render(f"Game starts in: {countdown}", True, WHITE)
                    screen.blit(text_surface, (WIDTH // 2 - 100, HEIGHT // 2))
            else:
                # Close palm to shoot
                if not in_pause_menu:
                    if not stretch and hand.gesture == 1:
                        stretch = True
                        origin_x = claw.get_x()
                        origin_y = claw.get_y()
   
                if not stretch:
                    claw.rotate()
                else:
                    if not pull:
                        claw.stretch()
                    else:
                        claw.pull(origin_x, origin_y)

                    if claw.get_x() <= origin_x and claw.get_y() <= origin_y:
                        stretch = False
                        pull = False
                    # Pull back if the claw went out the screen
                    if not (50 <= claw.get_x() <= WIDTH and  claw.get_y() <= HEIGHT):
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

                # DRAW BACKGROUND

                screen.blit(background, (0,0))

                # DRAW OBJECTS

                claw.draw(screen= screen)
                for bomb in bombs:
                    bomb.draw(screen= screen)
                for gold in golds:
                    gold.draw(screen= screen)

                # DRAW PAUSE MENU

                if in_pause_menu:

                    black_box = pygame.Rect(500, 270, 190, 160)
                    resume_rect = pygame.Rect(520, 290, 150, 50)
                    quit_rect = pygame.Rect(520, 360, 150, 50)

                    pygame.draw.rect(screen, BLACK, black_box)
                    pygame.draw.rect(screen, WHITE, resume_rect)
                    pygame.draw.rect(screen, WHITE, quit_rect)

                    resume_text = font.render('RESUME', True, BLACK)
                    quit_text = font.render('QUIT', True, BLACK)

                    screen.blit(resume_text, (525, 295))
                    screen.blit(quit_text, (525, 365))

                # DRAW TIME BOX

                draw_time_box(screen= screen, in_game_time= in_game_time, TIME= TIME, WAIT_TIME= WAIT_TIME, font= font)    

                # DRAW SCORE

                draw_score_box(screen= screen, SCORE= SCORE, font= font)
                
                # DRAW SETTING BUTTON
                setting_button.draw(screen= screen) 

                if time_left(in_game_time= in_game_time, TIME= TIME, WAIT_TIME= WAIT_TIME) <= 0 \
                    or len(golds) == 0:
                    end_game = True
                    in_game = False

        if end_game:
            text_1 = font.render(f"Your score is: {SCORE}.", True, WHITE)
            text_2 = font.render(f"Close your hand to play again.", True, WHITE)
            screen.blit(text_1, (WIDTH // 2 - 100, HEIGHT // 2))
            screen.blit(text_2, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

            if hand.gesture == 1:
                in_start_menu = True
                in_pause_menu = False
                in_game = False
                end_game = False

                origin_x , origin_y = 0, 0
                SCORE = 0
                golds , bombs = generator.spawn_objects(width = WIDTH, height = HEIGHT, n_golds = GOLDS, n_bombs = BOMBS)

        pygame.display.flip()
        clock.tick(45)

    pygame.quit()

    


if __name__ == "__main__":
    main()