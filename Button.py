import pygame

class Button:
    def __init__(self, path : str):
        self.image = None
        self.x = 0
        self.y = 0

        try:
            self.image = pygame.image.load(path)
        except:
            print("Path is not available.")

    def draw(self, screen : pygame.Surface):
        image = self.image
        if image:
            WIDTH = screen.get_size()[0]
            self.x = WIDTH - 120
            screen.blit(image, (self.x, self.y))

    def is_pressed(self, mouse_pos : tuple[int]) -> bool:
        mouse_x , mouse_y = mouse_pos

        return True if (self.x < mouse_x < self.x + 120 and self.y < mouse_y < self.y + 120) \
                else False