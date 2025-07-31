import pygame

class Explosion:
    def __init__(self, frames: list[pygame.Surface], pos: tuple[int, int], frame_delay: int = 150):
        self.frames = frames
        self.pos = pos
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = frame_delay
        self.finished = False

    def update(self, screen : pygame.Surface):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_delay:
            self.current_frame += 1
            self.last_update = now
            if self.current_frame >= len(self.frames):
                self.finished = True
        self.draw(screen = screen)

    def draw(self, screen):
        if not self.finished:
            x = self.pos[0]
            y = self.pos[1]
            image = self.frames[self.current_frame]
            rect = image.get_rect(center = (x,y))
            screen.blit(image, rect)

# Load and split the sprite sheet
def split_explosion_sprite_sheet(image_path, rows=3, cols=3):
    sprite_sheet = pygame.image.load(image_path)
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // cols
    frame_height = sheet_height // rows

    frames = []
    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
    return [frames[i] for i in [6,3,0,7,4,1,8]]


