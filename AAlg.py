from settings import *

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.c = 0
        self.h = 0
        self.t = 0

    def __eq__(self, other):
        return self.position == other.position


def a_alg(maze, start, end, heuristic):
    STEP_COST = 1
    start_node = Node(None, start)
    start_node.c = maze[start]

    end_node = Node(None, end)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]
        temp_index = 0
        for index, node in enumerate(open_list):
            if node.t < current_node.t:
                current_node = node
                temp_index = index

        open_list.pop(temp_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1]

        children = []
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            next_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
            if next_position[0] < maze.shape[0] - 1 and next_position[0] > 0 and next_position[1] < maze.shape[1] - 1 and next_position[1] > 0 and maze[next_position] != WALL:
                new_node = Node(current_node, next_position)
                children.append(new_node)
        for child in children:
            if child not in closed_list:
                child.heuristic = heuristic(child.position, end_node.position)
                child.total = maze[child.position] + child.heuristic + STEP_COST
                for open_node in open_list:
                    if child == open_node and child.c > open_node.c:
                        continue
                open_list.append(child)


def greedy(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5


def manhattan(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def euclid(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5


