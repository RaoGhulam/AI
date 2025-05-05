def calculate_optimal_choice(card_sequence, start_idx, end_idx, is_maximizing, alpha, beta):
    if start_idx > end_idx:
        return 0

    if is_maximizing:
        best_value = float('-inf')
        left_value = card_sequence[start_idx] + calculate_optimal_choice(
            card_sequence, start_idx + 1, end_idx, False, alpha, beta)
        best_value = max(best_value, left_value)
        alpha = max(alpha, best_value)
        if beta <= alpha:
            return best_value

        right_value = card_sequence[end_idx] + calculate_optimal_choice(
            card_sequence, start_idx, end_idx - 1, False, alpha, beta)
        best_value = max(best_value, right_value)
        alpha = max(alpha, best_value)
        return best_value
    else:
        if card_sequence[start_idx] < card_sequence[end_idx]:
            return calculate_optimal_choice(card_sequence, start_idx + 1, end_idx, True, alpha, beta)
        else:
            return calculate_optimal_choice(card_sequence, start_idx, end_idx - 1, True, alpha, beta)

def determine_best_move(card_sequence):
    first = 0
    last = len(card_sequence) - 1
    optimal_value = float('-inf')
    selected_move = None

    left_score = card_sequence[first] + calculate_optimal_choice(
        card_sequence, first + 1, last, False, float('-inf'), float('inf'))
    if left_score > optimal_value:
        optimal_value = left_score
        selected_move = 'first'

    right_score = card_sequence[last] + calculate_optimal_choice(
        card_sequence, first, last - 1, False, float('-inf'), float('inf'))
    if right_score > optimal_value:
        optimal_value = right_score
        selected_move = 'last'

    return selected_move

def simulate_card_game(card_sequence):
    """Simulate the complete card game between two players"""
    print(f"Starting card sequence: {card_sequence}")
    player1_score = 0
    player2_score = 0
    current_turn = 'player1'

    while card_sequence:
        if current_turn == 'player1':
            move = determine_best_move(card_sequence)
            if move == 'first':
                selected_card = card_sequence.pop(0)
            else:
                selected_card = card_sequence.pop()
            player1_score += selected_card
            print(f"Player 1 selects {selected_card}, Remaining cards: {card_sequence}")
            current_turn = 'player2'
        else:
            if len(card_sequence) == 1 or card_sequence[0] < card_sequence[-1]:
                selected_card = card_sequence.pop(0)
            else:
                selected_card = card_sequence.pop()
            player2_score += selected_card
            print(f"Player 2 selects {selected_card}, Remaining cards: {card_sequence}")
            current_turn = 'player1'

    print(f"Final scores - Player 1: {player1_score}, Player 2: {player2_score}")
    if player1_score > player2_score:
        print("Player 1 wins!")
    elif player2_score > player1_score:
        print("Player 2 wins!")
    else:
        print("The game ends in a tie!")

if __name__ == "__main__":
    game_cards = [4, 10, 6, 2, 9, 5]
    simulate_card_game(game_cards.copy())