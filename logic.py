"""
Logic module

This handles all the functions that deal with game mechanics - 
finding connected bubbles, checking what's attached to ceiling, generating levels, etc.
"""

import random
from settings import BASE_ROWS, BASE_COLS, MAX_ROWS, MAX_COLS, MAX_COLORS


#Phase 1

def get_neighbors(row, col, row_max, col_max):
    """
    Get the 6 neighbor positions for a bubble in hex grid.
    
    The offset is different for even/odd rows because of the
    hexagonal stagger layout we're using.
    
    Args:
        row: Row index of the bubble
        col: Column index of the bubble  
        row_max: Total rows in grid
        col_max: Total columns in grid
        
    Returns:
        List of valid (row, col) neighbor positions
    """
    neighbors = []

    # even rows shift left, odd rows shift right
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
    
    # filter out invalid positions
    for r, c in potential_moves:
        if r % 2 == 0:
            if 0 <= r < row_max and 0 <= c < col_max:
                neighbors.append((r, c))
        else:
            # odd rows have one less column
            if 0 <= r < row_max and 0 <= c < col_max - 1:
                neighbors.append((r, c))
    
    return neighbors


def get_connected_bubbles(grid, start_row, start_col):
    """
    Find all bubbles of same color connected to starting position.
    
    Uses BFS to search outward from the clicked bubble.
    Stones (value 8) block the search path.
    
    Args:
        grid: 2D list representing the game board
        start_row: The row of the clicked bubble
        start_col: The column of the clicked bubble
        
    Returns:
        List of (row, col) tuples for connected bubbles
    """
    val = grid[start_row][start_col]
    
    # cant match empty cells or stones
    if val == 0 or val is None or val == 8:
        return []
    
    target = get_color(val)
    
    bubbles = []
    queue = [(start_row, start_col)]
    seen = set()
    seen.add((start_row, start_col))

    while queue:
        curr_r, curr_c = queue.pop()
        bubbles.append((curr_r, curr_c))

        # check all neighbors
        for nr, nc in get_neighbors(curr_r, curr_c, len(grid), len(grid[0])):
            if (nr, nc) not in seen:
                neighbor_val = grid[nr][nc]
                # skip empty and stones
                if neighbor_val != 0 and neighbor_val != 8:
                    if get_color(neighbor_val) == target:
                        seen.add((nr, nc))
                        queue.append((nr, nc))
    
    return bubbles


#Phase 3: pooping n falling

def pop_bubbles(grid, bubbles):
    """
    Remove bubbles from grid if there's 3 or more.
    
    Args:
        grid: Game board to modify
        bubbles: List of (row,col) to try popping
        
    Returns:
        True if we popped them, False if group too small
    """
    if len(bubbles) >= 3:
        for r, c in bubbles:
            grid[r][c] = 0
        return True
    return False


def get_attached_to_ceiling(grid):
    """
    Find all bubbles that are still connected to the top row.
    
    Starts BFS from row 0 and marks everything reachable.
    Anything not marked will fall.
    
    Args:
        grid: Game board
        
    Returns:
        Set of (row, col) positions attached to ceiling
    """
    attached = set()
    queue = []
    
    # start with top row bubbles
    for c in range(len(grid[0])):
        if grid[0][c] != 0:
            queue.append((0, c))
            attached.add((0, c))
    
    # BFS to find everything connected
    while queue:
        r, c = queue.pop()
        for nr, nc in get_neighbors(r, c, len(grid), len(grid[0])):
            if (nr, nc) not in attached and grid[nr][nc] != 0:
                attached.add((nr, nc))
                queue.append((nr, nc))
    
    return attached


def get_floating_bubbles(grid):
    """
    Find bubbles that aren't connected to ceiling (should fall).
    
    Args:
        grid: Game board
        
    Returns:
        List of (row, col) for floating bubbles
    """
    attached = get_attached_to_ceiling(grid)
    floating = []
    
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != 0 and (r, c) not in attached:
                floating.append((r, c))
    
    return floating


def remove_floating_bubbles(grid, floating):
    """
    Clear floating bubbles from the grid.
    
    Args:
        grid: Game board to modify
        floating: List of positions to clear
    """
    for r, c in floating:
        grid[r][c] = 0


#Phase 4: Level generation

def generate_level(level_num):
    """
    Generate a new level with appropriate difficulty.
    
    Higher levels get more rows, columns, and colors. There's a 30% chance 
    bubbles copy neighbor colors to create better matchable groups.
    
    Args:
        level_num: Which level (1-20)
        
    Returns:
        Tuple of (grid, num_rows, num_cols)
    """
    grid = []
    
    # more colors as we progress
    num_colors = min(3 + ((level_num - 1) // 3), MAX_COLORS)
    
    # grid grows with level
    extra_rows = (level_num - 1) // 2
    extra_cols = level_num // 2
    num_rows = min(BASE_ROWS + extra_rows, MAX_ROWS)
    num_cols = min(BASE_COLS + extra_cols, MAX_COLS)
    
    for r in range(num_rows):
        row = []
        # odd rows have one less bubble
        cols = num_cols if r % 2 == 0 else num_cols - 1
        
        for c in range(cols):
            # check the neighbors colors
            nbs_colors = []
            for (nr, nc) in get_neighbors(r, c, num_rows, num_cols):
                if nr < len(grid) and nc < len(grid[nr]):
                    if grid[nr][nc] != 0:
                        nbs_colors.append(grid[nr][nc])
            
            # 30% chance to copy neighbor color for better clusters
            if random.randint(1, 10) < 4 and nbs_colors:
                row.append(random.choice(nbs_colors))
            else:
                row.append(random.randint(1, num_colors))
        
        grid.append(row)
    
    # add some stones
    max_stones = (num_rows + num_cols) // 4
    if level_num >= 16:
        max_stones += (level_num - 15)
    
    for _ in range(max_stones):
        r = random.randint(0, num_rows - 1)
        max_c = num_cols if r % 2 == 0 else num_cols - 1
        c = random.randint(0, max_c - 1)
        grid[r][c] = 8
    
    return grid, num_rows, num_cols


def is_board_clear(grid):
    """
    Check if all bubbles are gone.
    
    Args:
        grid: Game board
        
    Returns:
        True if board is empty
    """
    for row in grid:
        for cell in row:
            if cell != 0:
                return False
    return True



#Phase 5: Bubbles with supa powers#

def is_stone(value):
    """
    Check if value is a stone blocker.
    
    Args:
        value: Bubble value to check
        
    Returns:
        True if it's a stone (value 8)
    """
    return value == 8


def is_bomb(value):
    """
    Check if value is a bomb bubble.
    
    Bombs are encoded as color + 8 (so 9-15).
    
    Args:
        value: Bubble value to check
        
    Returns:
        True if it's a bomb
    """
    return 9 <= value <= 15


def get_color(value):
    """
    Get the base color from a bubble value.
    
    Works for regular bubbles (1-7) and bombs (9-15).
    
    Args:
        value: Bubble value
        
    Returns:
        Color number 1-7, or 0 for empty/stone
    """
    if value == 0 or value == 8:
        return 0
    if is_bomb(value):
        return value - 8
    return value


def pop_bomb(grid, row, col):
    """
    Get all positions destroyed by bomb explosion.
    
    Bomb destroys itself plus all adjacent bubbles.
    Stones survive the explosion.
    
    Args:
        grid: Game board
        row: Bomb row position
        col: Bomb column position
        
    Returns:
        List of (row, col) positions that get destroyed
    """
    popped = [(row, col)]
    
    for nr, nc in get_neighbors(row, col, len(grid), len(grid[0])):
        # don't destroy empty or stones
        if grid[nr][nc] != 0 and grid[nr][nc] != 8:
            popped.append((nr, nc))
    
    return popped
