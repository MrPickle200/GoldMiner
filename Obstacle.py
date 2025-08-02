import math
import pygame
from Explosion import Explosion, split_explosion_sprite_sheet

class Obstacle:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        self.point = 0
        self.r = 1
    def get_x(self) -> int:
        return self.x
    def get_y(self) -> int:
        return self.y
    def get_r(self) -> int:
        return self.r
    def get_point(self) -> int:
        return self.point

class Claw(Obstacle):
    def __init__(self,x ,y):
        super().__init__(x, y)
        self.direction : int = -1 # -1 for right , 1 for left
        self.angle : float = 90 
        self.r = 7
        self.origin_x = x
        self.origin_y = y
        self.len = y
        self.speed = 20  # speed along the rope

        self.image = pygame.image.load("Assets/claw.png")
        self.original_image = self.image
    # Rotate logic
    def rotate(self) -> None:
        if self.angle <= 25:
            self.direction = 1
        elif self.angle >= 85: 
            self.direction = -1

        self.angle += self.direction
        self.x = self.origin_x + int(math.cos(math.radians(self.angle)) * self.get_length())
        self.y = int(math.sin(math.radians(self.angle)) * self.get_length())

    # Stretch logic
    def stretch(self) -> None:
        rad = math.radians(self.angle)

        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed  
    
    # Pull logic
    def pull(self, origin_x, origin_y) -> None:
        if self.x > origin_x:
            rad = math.radians(self.angle)

            self.x -= math.cos(rad) * self.speed
            self.y -= math.sin(rad) * self.speed 

        else: 
            self.x = origin_x
            self.y = origin_y

    # UI
    def draw(self, screen) -> None:
        rotate_angle = 90 - self.angle 
        rotated = pygame.transform.rotate(self.original_image, rotate_angle)
        rect = rotated.get_rect(center = (self.x,self.y))
        screen.blit(rotated, rect)

    def get_length(self) -> int:
        return self.len
    
    def get_speed(self) -> None:
        return self.speed
    
class Gold(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = None
        self.point = 0
        self.mass = 1
        self.is_pulled = False
        self.exist = True
        self.pulled_angle : float = 0

    def update(self, screen, claw_speed) -> None:
        if self.is_pulled:
            pulled_angle = math.radians(self.pulled_angle)
            self.x -= math.cos(pulled_angle) * (claw_speed / self.mass)
            self.y -= math.sin(pulled_angle) * (claw_speed / self.mass)   


    def draw(self, screen) -> None:
        if self.image:
            image = self.image
            rect = image.get_rect(center = (self.x,self.y))
            screen.blit(image, rect)
    
    def get_m(self) -> int :
        return self.mass

class Gold_50(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/gold50.png")
        self.r = 20
        self.point = 50
        self.mass = 2

class Gold_100(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/gold100.png")
        self.r = 22
        self.point = 100
        self.mass = 4

class Gold_250(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/gold250.png")
        self.r = 29
        self.point = 250
        self.mass = 8

class Gold_500(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/gold500.png")
        self.r = 34
        self.point = 500
        self.mass = 16

class Gold_1000(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/gold1000.png")
        self.r = 150
        self.point = 1000
        self.mass = 32

class Diamond(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/diamond.png")
        self.r = 20
        self.point = 2000
        self.mass = 2

class Rock_10(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/rock10.png")
        self.r = 15
        self.point = 10
        self.mass = 5

class Rock_20(Gold):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("Assets/rock20.png")
        self.r = 17
        self.point = 20
        self.mass = 10

class Bomb(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.r = 45
        self.point = -100
        self.explode_range = 80
        self.image = pygame.image.load("Assets/bomb.png")
        self.exploding = False

        frames = split_explosion_sprite_sheet("Animations/explosion.png")
        self.explosion : Explosion = Explosion(frames = frames, pos = (x, y))

    def draw(self, screen : pygame.Surface):
        if self.exploding:
            self.explosion.update(screen = screen)
        else:
            image = self.image
            rect = image.get_rect(center = (self.x,self.y))
            screen.blit(image, rect)
    
