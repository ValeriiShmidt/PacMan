import random
from AAlg import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, application, start_position, ghost_type):
        self.type = None
        self.application = application
        self.position = start_position
        self.pix_position = self.get_pix_pos()
        self.path = None
        self.grid_position = start_position
        self.direction = vec(0, 0)
        self.personality = ghost_type
        self.speed = 2

    def draw(self):
        pygame.draw.circle(self.application.screen, ICE_COLOR,
                           (self.pix_position.x, self.pix_position.y),
                           self.application.cell_width // 2 - 2)
        pygame.display.update()

    def get_pix_pos(self):
        return vec((self.position[0] * self.application.cell_width) + PADDING // 2 + self.application.cell_width // 2,
                   (self.position[1] * self.application.cell_height) +
                   PADDING // 2 + self.application.cell_height // 2)

    def update(self):
        self.target = (int(self.application.player.grid_pos[1]), int(self.application.player.grid_pos[0]))
        if self.target != self.grid_position:
            self.pix_position += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_position[0] = (self.pix_position[0] - PADDING +
                                 self.application.cell_width // 2) // self.application.cell_width + 1
        self.grid_position[1] = (self.pix_position[1] - PADDING +
                                 self.application.cell_height // 2) // self.application.cell_height + 1

    def time_to_move(self):
        if int(self.pix_position.x + PADDING // 2) % self.application.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_position.y + PADDING // 2) % self.application.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def get_random_direction(self):
        while True:
            rand_int = random.randint(0, 3)
            random_direction = vec(0, 0)
            if rand_int == 0:
                random_direction = vec(-1, 0)
            elif rand_int == 1:
                random_direction = vec(1, 0)
            elif rand_int == 2:
                random_direction = vec(0, 1)
            elif rand_int == 3:
                random_direction = vec(0, -1)
            if vec(self.grid_position + random_direction) not in self.application.walls:
                return random_direction

    def get_a_star_direction(self):
        path = AAlg(self.application.grid_map, (int(self.grid_position[1]), int(self.grid_position[0])),
                    (int(self.application.player.grid_pos[1]), int(self.application.player.grid_pos[0])),
                    euclid, 0)
        next_step = (path[1][1], path[1][0])
        direction = vec(int(next_step[0] - self.grid_position[0]), int(next_step[1] - self.grid_position[1]))
        return direction

    def move(self):
        if self.personality == RANDOM:
            self.direction = self.get_random_direction()
        elif self.personality == DEFAULT:
            self.direction = self.get_a_star_direction()

    def grid_to_graph(self, grid):
        rows, cols = grid.shape
        graph = {}
        for i in range(rows - 1):
            cost = random.randint(1, 4)
            for j in range(cols - 1):
                if grid[i, j] != 1:
                    adj = []
                    for ele in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        if grid[ele[0], ele[1]] == 0:
                            adj.append((ele[0], ele[1], cost))
                    graph[(i, j)] = adj
        return graph

    def draw_path(self):
        for step in self.path[1:-1]:
            pygame.draw.rect(self.application.screen, BLUE, (step[1] * self.application.cell_width + PADDING // 2,
                                                             step[0] * self.application.cell_height + PADDING // 2,
                                                             self.application.cell_width - 5,
                                                             self.application.cell_height - 5))

    def load_grid(self):
        grid = np.zeros((ROWS + 1, COLS), dtype=int)
        with open("Map.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line[:-1]):
                    if char == "W":
                        grid[y, x] = 1
                    else:
                        grid[y, x] = 0
        return grid

    def is_valid_target(self, target):
        grid = self.load_grid()
        if grid[int(target.y), int(target.x)] == 1:
            return False
        else:
            return True
