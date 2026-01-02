import random
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


def pop_bubbles(grid, bubbles):
    if len(bubbles) >= 3:
        for r, c in bubbles:
            grid[r][c] = 0
        return True
    return False


#def apply_gravity()