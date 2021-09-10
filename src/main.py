from Node import *
from queue import PriorityQueue

# Setup pop up screen
solved = False
WIDTH = 1020
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


# Calculates the H score
def h_score(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstruct the shortest path in grid
def reconstruct_path(came_from, current, draw):
    global solved
    while current in came_from:
        current = came_from[current]
        if current.is_start() != True:
            current.make_path()
        if solved == False:
            draw()

# Resets any non essential nodes, such as closed, open and path nodes
def reset_non_essential(grid):
    for row in grid:
        for node in row:
            if node.is_closed() == True or node.is_open() == True or node.is_path() == True:
                node.reset()
                
# Runs the A* Pathfinding Algorithm                
def algorithm(draw, grid, start, end):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
    reset_non_essential(grid)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h_score(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            end.make_end()
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h_score(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if solved == False:
            draw()
        if current != start:
            current.make_closed()
    return False

# Creates list to store the Nodes
def make_grid(rows, width):
    grid = []
    node_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, node_width, rows)
            grid[i].append(node)
    return grid

# Resets grid, but does not change the start and end nodes
def reset_grid(grid):
    for row in grid:
        for node in row:
            if node.is_start() == False and node.is_end() == False:
                node.reset()
    return grid

# Draws on screen the grid's lines
def draw_grid(win, rows, width):
    node_width = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * node_width),
                         (width, i * node_width))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * node_width, 0),
                             (j * node_width, width))

# Draws entire game on each loop
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Get position the mouse clicked
def get_clicked_pos(pos, rows, width):
    node_width = width // rows
    y, x = pos

    row = y // node_width
    col = x // node_width

    return row, col

# Main function
def main(win, width):
    ROWS = 51
    global solved
    drag = 0
    run = True
    prev_node = [None, None, None] # List to preserve Barrier intregity
    grid = make_grid(ROWS, width)
    end = grid[ROWS-14][ROWS//2] # Pre position both start and end nodes
    end.make_end()
    start = grid[13][ROWS//2]
    start.make_start()
    while run: # Game loop
        draw(win, grid, ROWS, width) # Draw game loop
        for event in pygame.event.get():
            row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
            node = grid[row][col]
            
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left click to place barriers
                if drag == 0 and node != end and node != start:
                    if solved:
                        node.make_barrier()
                        algorithm(lambda: draw(win, grid, ROWS, width),
                                    grid, start, end)
                    elif node.is_barrier() == False:
                        node.make_barrier()
            if pygame.mouse.get_pressed()[2]: # Right click to remove barriers
                if node.is_barrier():
                    reset_non_essential(grid)
                    node.reset()
                    if solved:
                        algorithm(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Check if left mouse button is down
                node_before = node
                if node == start: # If mouse is down on start or end nodes, then assign value to drag
                    drag = 1
                elif node == end:
                    drag = 2
                        
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # If left mouse button is up, 
                drag = 0                                                 # then set drag to 0 and reset prev_node
                prev_node = [None, None, None]
                
            elif event.type == pygame.MOUSEMOTION and drag != 0: # If mouse is moving and left mouse button 
                if node_before.is_barrier() == False:            # is being pressed on start or end nodes
                        node_before.reset()
                if prev_node[2] and prev_node[:2] != [row,col]:
                    grid[prev_node[0]][prev_node[1]].make_barrier()
                if node.is_barrier():
                    prev_node = [row, col, True]
                if drag == 1 and node != end: # Moves start node
                    start = node
                    node_before = node
                    start.make_start()
                    
                elif drag == 2 and node != start: # Moves end node
                    end = node
                    node_before = node
                    end.make_end()
                    
                if solved and drag != 0:
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: # If space is pressed then rerun the algorithm
                    solved = False
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                    solved = True

                elif event.key == pygame.K_c: # If "c" key is pressed then clear screen and reset algortihm 
                    solved = False
                    prev_node = [ROWS, ROWS, None]
                    grid = reset_grid(grid)

    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH)