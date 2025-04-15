import time
from ortools.sat.python import cp_model

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

def solve_with_ortools(puzzle):
    model = cp_model.CpModel()
    
    cell = {}
    for i in range(9):
        for j in range(9):
            cell[(i, j)] = model.NewIntVar(1, 9, f'cell_{i}_{j}')

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                model.Add(cell[(i, j)] == puzzle[i][j])
    
    for i in range(9):
        model.AddAllDifferent([cell[(i, j)] for j in range(9)])
        model.AddAllDifferent([cell[(j, i)] for j in range(9)])
    
    for block_row in range(3):
        for block_col in range(3):
            cells = []
            for i in range(3):
                for j in range(3):
                    row = block_row * 3 + i
                    col = block_col * 3 + j
                    cells.append(cell[(row, col)])
            model.AddAllDifferent(cells)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        return [[solver.Value(cell[(i, j)]) for j in range(9)] for i in range(9)]
    else:
        return None

def solve_puzzles_ortools(puzzles):
    for i, puzzle in enumerate(puzzles):
        print(f"Solving Puzzle {i+1} (OR-Tools)")
        start_time = time.time()

        solution = solve_with_ortools(puzzle)

        end_time = time.time()
        runtime = end_time - start_time

        if solution:
            for row in solution:
                print(' '.join(str(num) for num in row))
        else:
            print("No solution found.")
        print(f"Time taken: {runtime:.4f} seconds\n")

puzzles = read_puzzles('puzzles.txt')
solve_puzzles_ortools(puzzles)