import pygame

class Menu:
    def __init__(self, path : str):
        self.image = None
        try:
            self.image = pygame.image.load(path)
        except:
            print("Path is not available.")

    def draw(self, screen : pygame.Surface, pos : tuple[int]):
        WIDTH, HEIGHT = screen.get_size()
        start_menu = self.image

        if start_menu:
            start_menu = pygame.transform.scale(start_menu, (WIDTH, HEIGHT))
            screen.blit(start_menu, pos)

    def get_image_size(self) -> tuple[int] | None:
        return self.image.get_size() if self.image else None
            