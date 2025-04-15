import time
import copy

def read_puzzles(filename):
    """Read multiple Sudoku puzzles from a file"""
    puzzles = []
    with open(filename, 'r') as f:
        grid = []
        for line in f:
            line = line.strip()
            if not line and grid:  # Empty line indicates puzzle end
                puzzles.append(grid)
                grid = []
            elif line:  # Puzzle row
                grid.append([int(ch) for ch in line])
        if grid:  # Add the last puzzle if file doesn't end with empty line
            puzzles.append(grid)
    return puzzles

def print_sudoku(board):
    """Print the Sudoku board in a readable format"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()

def is_valid(board, row, col, num):
    """Check if placing 'num' at (row,col) is valid"""
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def brute_force_solver(board):
    """Solve Sudoku using backtracking"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if brute_force_solver(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False  # Trigger backtracking
    return True  # Puzzle solved

def solve_and_print_puzzles(puzzles):
    """Solve each puzzle and print results with timing"""
    total_puzzles = len(puzzles)
    start_time = time.time()
    
    for i, puzzle in enumerate(puzzles, 1):
        print(f"\nPuzzle {i}/{total_puzzles}:")
        print("Original:")
        print_sudoku(puzzle)
        
        # Create a deep copy to solve
        solution = copy.deepcopy(puzzle)
        solve_start = time.time()
        solved = brute_force_solver(solution)
        solve_time = time.time() - solve_start
        
        if solved:
            print("\nSolution:")
            print_sudoku(solution)
            print(f"Solved in {solve_time:.4f} seconds")
        else:
            print("\nNo solution exists for this puzzle")
    
    total_time = time.time() - start_time
    print(f"\nAll puzzles solved in {total_time:.4f} seconds")
    print(f"Average time per puzzle: {total_time/total_puzzles:.4f} seconds")

if __name__ == "__main__":
    input_file = "puzzles.txt"
    
    try:
        puzzles = read_puzzles(input_file)
        if not puzzles:
            print(f"No puzzles found in {input_file}")
        else:
            print(f"Loaded {len(puzzles)} puzzles from {input_file}")
            solve_and_print_puzzles(puzzles)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")