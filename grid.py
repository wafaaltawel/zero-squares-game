from collections import deque
import pygame
from colors import *
from settings import *
from display import DisplayMessage

class Grid:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.display_message = DisplayMessage(screen, font)
        self.grid = [
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.movable_square_pos = [1, 0]
        self.goal_square_pos = [4, 4]
        self.trap_square_pos = [3, 0]
        self.grid[self.movable_square_pos[0]][self.movable_square_pos[1]] = 2

    def draw_grid(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * (SQUARE_SIZE + MARGIN)
                y = row * (SQUARE_SIZE + MARGIN)
                color = self.get_square_color(row, col)
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE), width=5)

    def get_square_color(self, row, col):
        if [row, col] == self.goal_square_pos:
            return GOAL_SQUARE_COLOR
        elif [row, col] == self.trap_square_pos:
            return TRAP_SQUARE_COLOR
        elif self.grid[row][col] == 2:
            return MOVABLE_SQUARE_COLOR
        elif self.grid[row][col] == 0:
            return (0, 0, 255)
        elif self.grid[row][col] == 1:
            return (0, 0, 0)
        return SQUARE_COLOR

    def move_square_full(self, direction):
        row, col = self.movable_square_pos
        self.grid[row][col] = 1

        if direction == "UP":
            while row > 0 and self.grid[row - 1][col] == 1:
                row -= 1
        elif direction == "LEFT":
                while col > 0 and self.grid[row][col - 1] == 1:
                    col -= 1

        elif direction == "RIGHT":
            while col < GRID_SIZE - 1 and self.grid[row][col + 1] == 1:
                col += 1
        elif direction == "DOWN":
            while row < GRID_SIZE - 1 and self.grid[row + 1][col] == 1:
                row += 1


        self.movable_square_pos = [row, col]
        self.grid[row][col] = 2
        self.check_goal_or_trap()

    def solve_with_bfs(self):
        start = tuple(self.movable_square_pos)
        goal = tuple(self.goal_square_pos)

        directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1),
        }

        queue = deque([(start, [])])
        visited = set()

        while queue:
            current_pos, path = queue.popleft()
            if current_pos in visited:
                continue

            visited.add(current_pos)

            if current_pos == goal:
                return path  # إعادة المسار بالكامل

            for direction, (dr, dc) in directions.items():
                new_row, new_col = current_pos[0] + dr, current_pos[1] + dc
                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                    if self.grid[new_row][new_col] == 1:  # المسارات المتاحة فقط
                        new_path = path + [direction]
                        queue.append(((new_row, new_col), new_path))

        return []  # إذا لم يكن هناك مسار

    def check_goal_or_trap(self):
        if self.movable_square_pos == self.trap_square_pos:
            self.display_message.show("You Lose!", (255, 0, 0), "😂")
        elif self.movable_square_pos == self.goal_square_pos:
            self.display_message.show("You Win!", (255, 255, 255), "🥲")
