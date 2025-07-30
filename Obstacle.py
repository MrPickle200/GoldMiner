import math
import pygame

class Obstacle:
    def __init__(self, x : int, y : int, r : int ):
        self.x = x
        self.y = y
        self.r = r
    def get_x(self) -> int:
        return self.x
    def get_y(self) -> int:
        return self.y
    def get_r(self) -> int:
        return self.r

class Claw(Obstacle):
    def __init__(self,x ,y , r):
        super().__init__(x, y, r)
        self.direction : int = -1 # -1 for right , 1 for left
        self.angle : float = 90 
        self.origin_x = x
        self.origin_y = y
        self.len = y
        self.speed = 10  # speed along the rope

        self.image = pygame.image.load("Assets/claw.png")
        self.original_image = self.image
    # Rotate logic
    def rotate(self, screen) -> None:
        if self.angle <= 40:
            self.direction = 1
        elif self.angle >= 80: 
            self.direction = -1

        self.angle += self.direction
        self.x = self.origin_x + int(math.cos(math.radians(self.angle)) * self.get_length())
        self.y = int(math.sin(math.radians(self.angle)) * self.get_length())

        self.draw_claw(screen)
    # Stretch logic
    def stretch(self, screen) -> None:
        rad = math.radians(self.angle)

        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed  
        
        self.draw_claw(screen)
    # Pull logic
    def pull(self, screen, origin_x, origin_y) -> None:
        if self.x > origin_x:
            rad = math.radians(self.angle)

            self.x -= math.cos(rad) * self.speed
            self.y -= math.sin(rad) * self.speed 

        else: 
            self.x = origin_x
            self.y = origin_y
        self.draw_claw(screen)
    # UI
    def draw_claw(self, screen) -> None:
        rotate_angle = 90 - self.angle 
        rotated = pygame.transform.rotate(self.original_image, rotate_angle)
        rect = rotated.get_rect(center = (self.x,self.y))
        screen.blit(rotated, rect)

    def get_length(self) -> int:
        return self.len
    
class Gold_50(Obstacle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.image = pygame.image.load("Assets/gold50.png")
        self.point = 50
    def draw_gold(self, screen) -> None:
        image = self.image
        rect = image.get_rect(center = (self.x,self.y))
        screen.blit(image, rect)

class Gold_100(Obstacle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.image = pygame.image.load("Assets/gold100.png")
        self.point = 100
    def draw_gold(self, screen) -> None:
        image = self.image
        rect = image.get_rect(center = (self.x,self.y))
        screen.blit(image, rect)

class Gold_250(Obstacle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.image = pygame.image.load("Assets/gold250.png")
        self.point = 250
    def draw_gold(self, screen) -> None:
        image = self.image
        rect = image.get_rect(center = (self.x,self.y))
        screen.blit(image, rect)

class Gold_500(Obstacle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.image = pygame.image.load("Assets/gold500.png")
        self.point = 500
    def draw_gold(self, screen) -> None:
        image = self.image
        rect = image.get_rect(center = (self.x,self.y))
        screen.blit(image, rect)

class Gold_1000(Obstacle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.image = pygame.image.load("Assets/gold1000.png")
        self.point = 1000

    def update(self, screen, pulled : bool, claw_x, claw_y) -> None:
        if pulled:
            dy = abs(self.y - claw_y)
            dx = abs(self.x - claw_x)
            pulled_angle = math.atan2(dy, dx)

            self.x -= math.cos(pulled_angle) * 2
            self.y -= math.sin(pulled_angle) * 2   
        if self.x <= claw_x and self.y <= claw_y:
            # Delete object
            return    
        self.draw_gold(screen)

    def draw_gold(self, screen) -> None:
        image = self.image
        rect = image.get_rect(center = (self.x,self.y))
        screen.blit(image, rect)
