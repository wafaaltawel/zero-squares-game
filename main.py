import pygame
import sys
from settings import *
from grid import Grid

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
font = pygame.font.Font(None, 74)

grid = Grid(screen, font)

solve_started = False
solution_path = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                grid.move_square_full("UP")
            elif event.key == pygame.K_DOWN:
                grid.move_square_full("DOWN")
            elif event.key == pygame.K_RIGHT:
                grid.move_square_full("RIGHT")
            elif event.key == pygame.K_LEFT:
                grid.move_square_full("LEFT")
            elif event.key == pygame.K_SPACE:
                solve_started = True
                solution_path = grid.solve_with_bfs()

    if solve_started and solution_path:
        next_move = solution_path.pop(0)
        grid.move_square_full(next_move)
        pygame.time.delay(500)

        if not solution_path:
            solve_started = False

    grid.draw_grid()
    pygame.display.flip()

pygame.quit()
