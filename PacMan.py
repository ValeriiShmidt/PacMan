import pygame
from AAlg import *
from settings import *
vec = pygame.math.Vector2


class PacMan:
    def __init__(self, application, pos):
        self.algo_to_use = All_COINS
        self.heuristic = euclid
        self.application = application
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.old_grid_pos = None
        self.pix_pos = self.get_pixel_position()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = PLAYER_LIVES
        self.destination = DESTINATION
        if self.algo_to_use == All_COINS:
            self.path = self.collect_all_coins()
        elif self.algo_to_use == ONLY_WAY:
            self.path = a_alg(self.application.grid_map, START, DESTINATION, self.heuristic)

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.is_in_bounds():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.is_able_to_move()

        new_pos = [(self.pix_pos[0] - BORDER + self.application.cell_width // 2) // self.application.cell_width + 1,
                   (self.pix_pos[1] - BORDER + self.application.cell_height // 2) // self.application.cell_height + 1]

        if new_pos != self.grid_pos:
            self.old_grid_pos = self.grid_pos
            self.grid_pos = new_pos
            if self.algo_to_use == All_COINS:
                self.path = self.collect_all_coins()
            elif self.algo_to_use == ONLY_WAY:
                self.path = a_alg(self.application.grid_map, START, DESTINATION, self.heuristic)

        if self.on_coin():
            self.eat_coin()
        if self.on_enemy():
            self.application.remove_life()

    def draw(self):
        pygame.draw.circle(self.application.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                                    int(self.pix_pos.y)), self.application.cell_width // 2 - 2)
        for x in range(self.lives):
            pygame.draw.circle(self.application.screen, GREY, (30 + 20 * x, HEIGHT - 15), 7)

    def draw_path(self):
        for point in self.path:
            pygame.draw.rect(self.application.screen, (0, 200, 200),
                               (point[1] * self.application.cell_width + BORDER // 2,
                                point[0] * self.application.cell_height + BORDER // 2,
                                self.application.cell_width,
                                self.application.cell_height), 1)

    def collect_all_coins(self):
        hero = (int(self.grid_pos[1]), int(self.grid_pos[0]))
        coins = []
        for c in self.application.coins:
            coins.append((int(c.y), int(c.x)))
        ways = []
        for coin in coins:
            way = a_alg(self.application.grid_map, hero, coin, self.heuristic)
            if way is not None:
                ways += way
            else:
                print("oops RELOAD GAME PLZ")
                return [START]
        return ways + a_alg(self.application.grid_map, hero, self.destination, self.heuristic)

    def on_coin(self):
        if self.grid_pos in self.application.coins:
            return True
        return False

    def eat_coin(self):
        self.application.coins.remove(self.grid_pos)
        self.current_score += 1

    def on_enemy(self):
        for enemy in self.application.enemies:
            if enemy.position == self.grid_pos:
                return True

    def change_direction(self, direction):
        self.stored_direction = direction

    def get_pixel_position(self):
        return vec((self.grid_pos[0] * self.application.cell_width) + BORDER // 2 + self.application.cell_width // 2,
                   (self.grid_pos[1] * self.application.cell_height) +
                   BORDER // 2 + self.application.cell_height // 2)

    def is_in_bounds(self):
        if int(self.pix_pos.x + BORDER // 2) % self.application.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + BORDER // 2) % self.application.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def is_able_to_move(self):
        for wall in self.application.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
