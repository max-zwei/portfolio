
import sys
import pygame

from maze_solver.maze_solver import Maze_Solver



def main():
    if len(sys.argv) != 3:
        message = """You didn't specify the right amount of inputs.
Usage: python maze.py <maze-file-name>.txt \"<Algorithm>\"
where <Algorithm> can be DFS (Depth-first search), 
BFS (Breadth-first search), or HS (Heuristic search)."""
        sys.exit(message)

    m = Maze_Solver(sys.argv[1])

    lab_height = m.height
    lab_width = m.width

    tile_size = 40
    tile_origin = (tile_size, tile_size)

    size = width, height = (lab_width + 2) * tile_size, (lab_height + 4) * tile_size

    # Colors
    black = (0, 0, 0)
    grey = (40, 40, 40)
    white = (255, 255, 255)
    start_color = (255, 102, 102)
    goal_color = (0, 204, 0)
    explored_color = (0, 102, 102)
    frontier_color = (0, 204, 204)
    solution_color = (148, 255, 185)
    button_color = grey

    pygame.init()
    screen = pygame.display.set_mode(size)

    def draw_current_maze():
        for i in range(lab_height):
            for j in range(lab_width):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )

                pygame.draw.rect(screen, black, rect, 3)

                if m.walls[i][j]:
                    screen.fill(grey, rect)
                elif (i, j) == m.start:
                    screen.fill(start_color, rect)
                elif (i, j) == m.goal:
                    screen.fill(goal_color, rect)
                elif m.solution and (i, j) in m.solution:
                    screen.fill(solution_color, rect)
                elif (i, j) in m.explored:
                    screen.fill(explored_color, rect)
                elif any(node.state == (i, j) for node in m.frontier.frontier):
                    screen.fill(frontier_color, rect)
                else:
                    screen.fill(white, rect)

        if m.solution:
            print(f"Your algorithm explored {len(m.explored)} nodes (including start and goal).")

        pygame.display.update()

    screen.fill(black)
    draw_current_maze()
    explore_button = pygame.Rect(width/2 - 60, tile_origin[1] + (lab_height + 1) * tile_size, 120, 40)

    small_text = pygame.font.Font("freesansbold.ttf", 30)
    text_surface = small_text.render("Explore", True, white)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if explore_button.collidepoint(event.pos):
                    if not m.solution:
                        m.explore_stepwise()
                        draw_current_maze()

        pygame.draw.rect(screen, button_color, explore_button)
        screen.blit(text_surface, explore_button)
        pygame.display.update()


if __name__ == "__main__":
    main()
