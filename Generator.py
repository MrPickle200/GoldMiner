import random
import math
from Obstacle import *

class Generator:
    def __init__(self):
        pass
    def is_overlapping(self, x, y, r, others):
        for obj in others:
            dx = x - obj.x
            dy = y - obj.y
            dist = math.hypot(dx, dy)
            if dist < (r + obj.get_r()):
                return True
        return False

    def spawn_objects(self, width, height, n_golds, n_bombs):
        all_gold_types = [Gold_50, Gold_100, Gold_250, Gold_500, Gold_1000, Diamond]
        golds = []
        bombs = []
        placed_objects = []  # Used for overlap checking
        margin = 10
        min_y = height // 3
        max_attempts = 1000

        # Spawn golds
        for _ in range(n_golds):
            for _ in range(max_attempts):
                GoldType = random.choice(all_gold_types)
                dummy = GoldType(0, 0)
                r = dummy.get_r()

                x = random.randint(margin + r, width - margin - r)
                y = random.randint(min_y + r, height - margin - r)

                new_gold = GoldType(x, y)

                if not self.is_overlapping(x, y, r, placed_objects):
                    golds.append(new_gold)
                    placed_objects.append(new_gold)
                    break

        # Spawn bombs
        for _ in range(n_bombs):
            for _ in range(max_attempts):
                dummy = Bomb(0, 0)
                r = dummy.get_r()

                x = random.randint(margin + r, width - margin - r)
                y = random.randint(min_y + r, height - margin - r)

                new_bomb = Bomb(x, y)

                if not self.is_overlapping(x, y, r, placed_objects):
                    bombs.append(new_bomb)
                    placed_objects.append(new_bomb)
                    break

        return golds, bombs
