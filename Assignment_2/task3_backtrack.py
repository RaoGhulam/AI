import time
from copy import deepcopy
from collections import deque

def read_puzzles(filename):
    puzzles = []
    with open(filename, 'r') as f:
        grid = []
        for line in f:
            line = line.strip()
            if not line and grid:
                puzzles.append(grid)
                grid = []
            elif line:
                grid.append([int(ch) for ch in line])
        if grid:
            puzzles.append(grid)
    return puzzles

def get_variables_and_domains(grid):
    variables = []
    domains = {}
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                variables.append((r, c))
                domains[(r, c)] = list(range(1, 10))
            else:
                domains[(r, c)] = [grid[r][c]]
    return variables, domains

def get_neighbors(cell):
    r, c = cell
    neighbors = set()
    for i in range(9):
        if i != c:
            neighbors.add((r, i))
        if i != r:
            neighbors.add((i, c))
    start_r, start_c = (r // 3) * 3, (c // 3) * 3
    for i in range(start_r, start_r + 3):
        for j in range(start_c, start_c + 3):
            if (i, j) != (r, c):
                neighbors.add((i, j))
    return neighbors

def ac3(domains):
    queue = deque()
    for x in domains:
        for y in get_neighbors(x):
            if y in domains:
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        if revise(domains, x, y):
            if not domains[x]:
                return False
            for z in get_neighbors(x):
                if z != y and z in domains:
                    queue.append((z, x))
    return True

def revise(domains, x, y):
    revised = False
    x_vals = domains[x][:]
    for val in x_vals:
        if not any(val != other for other in domains[y]):
            domains[x].remove(val)
            revised = True
    return revised

def select_unassigned_variable(domains, grid):
    for var in domains:
        r, c = var
        if grid[r][c] == 0:
            return var
    return None

def backtrack(grid, domains):
    if all(grid[r][c] != 0 for r in range(9) for c in range(9)):
        return grid  # Solved

    var = select_unassigned_variable(domains, grid)
    if var is None:
        return grid

    r, c = var
    for val in domains[var]:
        if all(val != grid[nr][nc] for nr, nc in get_neighbors(var)):
            grid[r][c] = val
            saved_domains = deepcopy(domains)
            domains[var] = [val]

            if ac3(domains):
                result = backtrack(grid, domains)
                if result:
                    return result

            grid[r][c] = 0
            domains = saved_domains
    return None

puzzles = read_puzzles('puzzles.txt')

for i, puzzle in enumerate(puzzles):
    print(f"Solving Puzzle {i+1}")
    start_time = time.time()

    grid = deepcopy(puzzle)
    _, domains = get_variables_and_domains(grid)
    ac3(domains)
    solution = backtrack(grid, domains)

    end_time = time.time()
    runtime = end_time - start_time

    if solution:
        for row in solution:
            print(' '.join(str(num) for num in row))
    else:
        print("No solution found.")
    
    print(f"Time taken: {runtime:.4f} seconds\n")