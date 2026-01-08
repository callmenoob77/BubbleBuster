#This is the py file for mainly backend stuff, like checking the groups and stuff like that

import random
from settings import BASE_ROWS, BASE_COLS, MAX_ROWS, MAX_COLS, MAX_COLORS

#Phase 1

#returns the 6 neighbors of a bubble in the hexagonal grid
def get_neighbors(row, col, row_max, col_max):
    neighbors = []

    if row % 2 == 0:
        potential_moves = [
            (row - 1, col - 1),
            (row - 1, col),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col)
        ]
    else:
        potential_moves = [
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col),
            (row + 1, col + 1)
        ]
    
    for r, c in potential_moves:
        if r % 2 == 0:
            if 0 <= r < row_max and 0 <= c < col_max:
                neighbors.append((r, c))
        else:
            if 0 <= r < row_max and 0 <= c < col_max - 1:
                neighbors.append((r, c))
    
    return neighbors


#finds all bubbles connected to start bubble with same color
def get_connected_bubbles(grid, start_row, start_col):
    value = grid[start_row][start_col]
    if value == 0 or value is None or value == 8:
        return []
    
    target_color = get_color(value)
    
    bubbles = []
    to_visit = [(start_row, start_col)]
    visited = set()
    visited.add((start_row, start_col))

    while to_visit:
        current_r, current_c = to_visit.pop()
        bubbles.append((current_r, current_c))

        nbrs = get_neighbors(current_r, current_c, len(grid), len(grid[0]))
        for nbrs_r, nbrs_c in nbrs:
            if (nbrs_r, nbrs_c) not in visited:
                neighbor_value = grid[nbrs_r][nbrs_c]
                if neighbor_value != 0 and neighbor_value != 8:
                    if get_color(neighbor_value) == target_color:
                        visited.add((nbrs_r, nbrs_c))
                        to_visit.append((nbrs_r, nbrs_c))
    return bubbles


#Phase 3

#removes bubbles from grid if theres 3 or more
def pop_bubbles(grid, bubbles):
    if len(bubbles) >= 3:
        for r, c in bubbles:
            grid[r][c] = 0
        return True
    return False


#finds all bubbles connected to the top row
def get_attached_to_ceiling(grid):
    attached = set()
    to_visit = []
    
    for c in range(len(grid[0])):
        if grid[0][c] != 0:
            to_visit.append((0, c))
            attached.add((0, c))
    
    while to_visit:
        r, c = to_visit.pop()
        neighbors = get_neighbors(r, c, len(grid), len(grid[0]))
        for nr, nc in neighbors:
            if (nr, nc) not in attached and grid[nr][nc] != 0:
                attached.add((nr, nc))
                to_visit.append((nr, nc))
    
    return attached


#finds bubbles that arent connected to ceiling (should fall)
def get_floating_bubbles(grid):
    attached = get_attached_to_ceiling(grid)
    floating = []
    
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != 0 and (r, c) not in attached:
                floating.append((r, c))
    
    return floating


#clears floating bubbles from grid
def remove_floating_bubbles(grid, floating):
    for r, c in floating:
        grid[r][c] = 0


#Phase 4

#creates a new level grid with colors and stones
def generate_level(level_num):
    grid = []
    num_colors = min(3 + ((level_num - 1) // 3), MAX_COLORS)
    
    extra_rows = (level_num - 1) // 2
    extra_cols = level_num // 2
    
    num_rows = min(BASE_ROWS + extra_rows, MAX_ROWS)
    num_cols = min(BASE_COLS + extra_cols, MAX_COLS)
    
    for r in range(num_rows):
        current_row = []
        if r % 2 == 0:
            cols = num_cols
        else:
            cols = num_cols - 1
        
        for c in range(cols):
            neighbors = get_neighbors(r, c, num_rows, num_cols)
            nbs_colors = []
            for (nr, nc) in neighbors:
                if nr < len(grid):
                    if nc < len(grid[nr]):
                        if grid[nr][nc] != 0:
                            nbs_colors.append(grid[nr][nc])
            
            if random.randint(1, 10) < 4 and nbs_colors:
                color = random.choice(nbs_colors)
                current_row.append(color)
            else:
                current_row.append(random.randint(1, num_colors))
        grid.append(current_row)
    
    max_stones = (num_rows + num_cols) // 4
    if level_num >= 16:
        max_stones += (level_num - 15)
    for _ in range(max_stones):
        r = random.randint(0, num_rows - 1)
        max_c = num_cols if r % 2 == 0 else num_cols - 1
        c = random.randint(0, max_c - 1)
        grid[r][c] = 8
    
    return grid, num_rows, num_cols


#checks if all bubbles are cleared
def is_board_clear(grid):
    for row in grid:
        for cell in row:
            if cell != 0:
                return False
    return True


#checks if theres any group of 3+ you can pop
def has_valid_moves(grid):
    checked = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != 0 and (r, c) not in checked:
                group = get_connected_bubbles(grid, r, c)
                for pos in group:
                    checked.add(pos)
                if len(group) >= 3:
                    return True
    return False


#Phase 5

#checks if bubble is a stone
def is_stone(value):
    return value == 8


#checks if bubble is a bomb
def is_bomb(value):
    return 9 <= value <= 15


#gets the color of a bubble (works for bombs too)
def get_color(value):
    if value == 0 or value == 8:
        return 0
    if is_bomb(value):
        return value - 8
    return value


#returns all bubbles destroyed by a bomb explosion
def pop_bomb(grid, row, col):
    popped = [(row, col)]
    neighbors = get_neighbors(row, col, len(grid), len(grid[0]))
    for nr, nc in neighbors:
        if grid[nr][nc] != 0 and grid[nr][nc] != 8:
            popped.append((nr, nc))
    return popped
