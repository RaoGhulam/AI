import copy
import math

CELL_EMPTY = '.'
PLAYER_WHITE = 'W'
PLAYER_BLACK = 'B'

GRID_DIMENSION = 8

def initialize_game_board():
    game_grid = [[CELL_EMPTY for _ in range(GRID_DIMENSION)] for _ in range(GRID_DIMENSION)]
    
    for i in range(3):
        for j in range(GRID_DIMENSION):
            if (i + j) % 2 == 1:
                game_grid[i][j] = PLAYER_BLACK
                
    for i in range(5, 8):
        for j in range(GRID_DIMENSION):
            if (i + j) % 2 == 1:
                game_grid[i][j] = PLAYER_WHITE
                
    return game_grid

def display_board(game_board):
    for i in range(GRID_DIMENSION):
        print(f"{i}: ", ' '.join(game_board[i]))
    print("   ", ' '.join(map(str, range(GRID_DIMENSION))))

def find_possible_moves(game_board, current_player):
    move_directions = [(-1, -1), (-1, 1)] if current_player == PLAYER_WHITE else [(1, -1), (1, 1)]
    valid_moves = []
    
    for i in range(GRID_DIMENSION):
        for j in range(GRID_DIMENSION):
            if game_board[i][j] == current_player:
                for di, dj in move_directions:
                    new_i, new_j = i + di, j + dj
                    
                    if 0 <= new_i < GRID_DIMENSION and 0 <= new_j < GRID_DIMENSION:
                        if game_board[new_i][new_j] == CELL_EMPTY:
                            valid_moves.append(((i, j), (new_i, new_j)))
                            
                    capture_i, capture_j = i + 2 * di, j + 2 * dj
                    if (0 <= capture_i < GRID_DIMENSION and 0 <= capture_j < GRID_DIMENSION and
                        game_board[new_i][new_j] not in [current_player, CELL_EMPTY] and
                        game_board[capture_i][capture_j] == CELL_EMPTY):
                            valid_moves.append(((i, j), (capture_i, capture_j)))
                            
    return valid_moves

def execute_move(game_board, move):
    start_pos, end_pos = move
    start_i, start_j = start_pos
    end_i, end_j = end_pos
    
    updated_board = copy.deepcopy(game_board)
    updated_board[end_i][end_j] = updated_board[start_i][start_j]
    updated_board[start_i][start_j] = CELL_EMPTY
    
    if abs(end_i - start_i) == 2:
        captured_i = (start_i + end_i) // 2
        captured_j = (start_j + end_j) // 2
        updated_board[captured_i][captured_j] = CELL_EMPTY
        
    return updated_board

def calculate_board_score(game_board):
    white_count = sum(row.count(PLAYER_WHITE) for row in game_board)
    black_count = sum(row.count(PLAYER_BLACK) for row in game_board)
    return black_count - white_count

def find_best_move(game_board, search_depth, is_maximizing, alpha, beta):
    current_player = PLAYER_BLACK if is_maximizing else PLAYER_WHITE
    possible_moves = find_possible_moves(game_board, current_player)
    
    if search_depth == 0 or not possible_moves:
        return calculate_board_score(game_board), None
        
    optimal_move = None
    
    if is_maximizing:
        best_value = -math.inf
        for move in possible_moves:
            new_board = execute_move(game_board, move)
            value, _ = find_best_move(new_board, search_depth - 1, False, alpha, beta)
            if value > best_value:
                best_value = value
                optimal_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best_value, optimal_move
    else:
        best_value = math.inf
        for move in possible_moves:
            new_board = execute_move(game_board, move)
            value, _ = find_best_move(new_board, search_depth - 1, True, alpha, beta)
            if value < best_value:
                best_value = value
                optimal_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_value, optimal_move

def run_game():
    current_board = initialize_game_board()
    display_board(current_board)
    
    while True:
        player_moves = find_possible_moves(current_board, PLAYER_WHITE)
        if not player_moves:
            print("AI wins! No available moves for player.")
            break
            
        print("Enter your move (format: start_row start_col end_row end_col): ")
        try:
            sr, sc, er, ec = map(int, input().split())
            if ((sr, sc), (er, ec)) in player_moves:
                current_board = execute_move(current_board, ((sr, sc), (er, ec)))
                print(f"Player moved: ({sr},{sc}) to ({er},{ec})")
            else:
                print("Invalid move. Please try again.")
                continue
        except ValueError:
            print("Please enter four numbers separated by spaces.")
            continue
            
        display_board(current_board)
        
        ai_moves = find_possible_moves(current_board, PLAYER_BLACK)
        if not ai_moves:
            print("Player wins! No available moves for AI.")
            break
            
        _, ai_move = find_best_move(current_board, 4, True, -math.inf, math.inf)
        if ai_move:
            current_board = execute_move(current_board, ai_move)
            (sr, sc), (er, ec) = ai_move
            print(f"AI moved: ({sr},{sc}) to ({er},{ec})")
        display_board(current_board)

if __name__ == "__main__":
    run_game()