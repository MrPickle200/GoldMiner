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
    def estimate_spawn_score(self, n_golds, n_bombs):
        gold_types = [Gold_50, Gold_100, Gold_250, Gold_500, Gold_1000, Diamond, Rock_10, Rock_20]
        total_score = 0

        for _ in range(n_golds):
            GoldType = random.choice(gold_types)
            temp = GoldType(0, 0)
            total_score += temp.get_point()

        for _ in range(n_bombs):
            temp = Bomb(0, 0)
            total_score += temp.get_point()

        return total_score

    def spawn_objects(self, width, height, n_golds, n_bombs, tolerance = 200):
        all_gold_types = [Gold_50, Gold_100, Gold_250, Gold_500, Gold_1000, Diamond, Rock_10, Rock_20]
        golds = []
        bombs = []
        placed_objects = []
        margin = 10
        min_y = height // 3
        max_attempts = 1000
        current_score = 0
        target_score = self.estimate_spawn_score(n_golds, n_bombs)

        # Spawn fixed number of golds
        for _ in range(n_golds):
            for _ in range(max_attempts):
                GoldType = random.choice(all_gold_types)
                temp = GoldType(0, 0)
                r = temp.get_r()
                points = temp.get_point()

                # If this would push the score too high, retry
                if current_score + points > target_score + tolerance:
                    continue

                x = random.randint(margin + r, width - margin - r)
                y = random.randint(min_y + r, height - margin - r)
                new_gold = GoldType(x, y)

                if not self.is_overlapping(x, y, r, placed_objects):
                    golds.append(new_gold)
                    placed_objects.append(new_gold)
                    current_score += points
                    break

        # Spawn fixed number of bombs
        for _ in range(n_bombs):
            for _ in range(max_attempts):
                temp = Bomb(0, 0)
                r = temp.get_r()
                points = temp.get_point()

                if current_score + points > target_score + tolerance:
                    continue

                x = random.randint(margin + r, width - margin - r)
                y = random.randint(min_y + r, height - margin - r)
                new_bomb = Bomb(x, y)

                if not self.is_overlapping(x, y, r, placed_objects):
                    bombs.append(new_bomb)
                    placed_objects.append(new_bomb)
                    current_score += points
                    break

        return golds, bombs

