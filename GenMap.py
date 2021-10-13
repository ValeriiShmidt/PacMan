import numpy as np
from settings import *
import random
from AAlg import a_alg, manhattan

class GenMap:
    def __init__(self):
        self.cols = 0
        self.rows = 0
        self.grid = 0
        self.empty_position_count = 0
        self.coins = []

    def generate_coins(self, amount):
        empty_positions = self.get_empty_blocks_positions()
        for _ in range(amount):
            position = random.choice(empty_positions)
            self.grid[position] = COIN
            self.coins.append(position)

    def generate_map_by_kruskal(self, rows, cols):
        grid = np.full_like(np.zeros((rows, cols)), fill_value=BLOCKED, dtype=int)
        self.cols = cols
        self.rows = rows
        self.grid = grid
        start_cell = (np.random.randint(1, rows - 1, dtype=int), np.random.randint(1, cols - 1, dtype=int))
        self.grid[start_cell] = EMPTY
        self.grid[DESTINATION] = EMPTY
        neighbors_cells = self.get_neighbors_of_cell(start_cell, BLOCKED)
        while len(neighbors_cells) > 0:
            random_cell = random.choice(neighbors_cells)
            neighbors = self.get_neighbors_of_cell(random_cell, EMPTY)
            random_neighbor = random.choice(neighbors)
            self.connect_cell(random_neighbor, random_cell)
            neighbors_cells += self.get_neighbors_of_cell(random_cell, BLOCKED)
            neighbors_cells = list(set(neighbors_cells))
            self.grid[random_cell] = EMPTY
            neighbors_cells.remove(random_cell)
        self.grid[0, :] = WALL
        self.grid[rows-1, :] = WALL
        self.grid[:, 0] = WALL
        self.grid[:, cols-1] = WALL
        self.generate_coins(COIN_AMOUNTS)
        if a_alg(self.grid, START, DESTINATION, manhattan) is not None:
            return self.grid
        else:
            self.grid = self.generate_map_by_kruskal(rows, cols)
            return self.grid

    def get_empty_blocks_positions(self):
        height = self.grid.shape[0]
        width = self.grid.shape[1]
        empty_blocks_positions = []
        for i in range(height):
            for j in range(width):
                if self.grid[i, j] == EMPTY:
                    empty_blocks_positions.append((i, j))
        return empty_blocks_positions

    def connect_cell(self, first_cell, second_cell):
        if first_cell[0] == second_cell[0]:
            new_passage_cell = (first_cell[0], (first_cell[1] + second_cell[1]) // 2)
            self.grid[new_passage_cell] = EMPTY
        elif first_cell[1] == second_cell[1]:
            new_passage_cell = ((first_cell[0] + second_cell[0]) // 2, first_cell[1])
            self.grid[new_passage_cell] = EMPTY

    def get_neighbors_of_cell(self, cell, status):
        neighbors = []
        cells = [(cell[0] - 2, cell[1]), (cell[0] + 2, cell[1]), (cell[0], cell[1] - 2), (cell[0], cell[1] + 2)]
        for cell in cells:
            if self.is_valid_cell(cell) and self.grid[cell] == status:
                neighbors.append(cell)
        return neighbors

    def is_valid_cell(self, cell):
        if cell[0] < 0 or cell[0] >= self.rows or cell[1] < 0 or cell[1] >= self.cols:
            return False
        return True
