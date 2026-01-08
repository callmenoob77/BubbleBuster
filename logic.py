#This is the py file for mainly backend stuff, like checking the groups and stuff like that

import random

#Phase 1
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


def get_connected_bubbles(grid, start_row, start_col):
    target = grid[start_row][start_col]
    if target == 0 or target is None:
        return []
    
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
                if grid[nbrs_r][nbrs_c] == target:
                    visited.add((nbrs_r, nbrs_c))
                    to_visit.append((nbrs_r, nbrs_c))
    return bubbles



#Phase 3

def pop_bubbles(grid, bubbles):
    if len(bubbles) >= 3:
        for r, c in bubbles:
            grid[r][c] = 0
        return True
    return False

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


def get_floating_bubbles(grid):
    attached = get_attached_to_ceiling(grid)
    floating = []
    
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != 0 and (r, c) not in attached:
                floating.append((r, c))
    
    return floating


def remove_floating_bubbles(grid, floating):
    for r, c in floating:
        grid[r][c] = 0


#Phase 4

def generate_level(level_num):
    grid = []
    num_colors = min(3 + ((level_num - 1) // 3), 7)
    
    base_rows = 5
    base_cols = 6
    extra_rows = (level_num - 1) // 2
    extra_cols = level_num // 2
    
    num_rows = min(base_rows + extra_rows, 12)
    num_cols = min(base_cols + extra_cols, 10)
    
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
            
            if random.randint(1, 10) < 3 and nbs_colors:
                color = random.choice(nbs_colors)
                current_row.append(color)
            else:
                current_row.append(random.randint(1, num_colors))
        grid.append(current_row)
    
    return grid, num_rows, num_cols


def is_board_clear(grid):
    for row in grid:
        for cell in row:
            if cell != 0:
                return False
    return True


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
