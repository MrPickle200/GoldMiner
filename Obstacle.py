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
        self.vel = 1

        self.image = pygame.image.load("Assets/claw.png")
        self.original_image = self.image
    # Rotate logic
    def rotate(self, screen) -> None:
        self.angle += self.direction
        self.x = self.origin_x + int(math.cos(math.radians(self.angle)) * self.get_length())
        self.y = int(math.sin(math.radians(self.angle)) * self.get_length())

        if self.angle <= 60:
            self.direction = 1
        elif self.angle >= 120: 
            self.direction = -1
        self.draw_claw(screen)
    # Stretch logic
    def stretch(self, screen) -> None:
        if self.angle <= 90:
            self.x += self.vel
            self.y = int(math.tan(math.radians(self.angle)) * abs(self.origin_x - self.x))    
        else:
            self.x -= self.vel
            self.y = int(math.tan(math.radians(180 - self.angle)) * abs(self.origin_x - self.x))  
        self.draw_claw(screen)
    # Pull logic
    def pull(self, screen) -> None:
        self.draw_claw(screen)
    # UI
    def draw_claw(self, screen) -> None:
        rotate_angle = 90 - self.angle 
        rotated = pygame.transform.rotate(self.original_image, rotate_angle)
        rect = rotated.get_rect(center = (self.x,self.y))
        screen.blit(rotated, rect)

    def get_length(self) -> int:
        return self.len
