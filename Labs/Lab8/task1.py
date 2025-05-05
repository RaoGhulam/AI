def create_card_deck():
    card_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    card_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 
                  "Jack", "Queen", "King", "Ace"]
    return [(value, suit) for suit in card_suits for value in card_values]

def calculate_probabilities(card_deck):
    red_suits = ["Hearts", "Diamonds"]
    red_cards = [card for card in card_deck if card[1] in red_suits]
    prob_red = len(red_cards) / len(card_deck)
    
    hearts = [card for card in red_cards if card[1] == "Hearts"]
    prob_heart_if_red = len(hearts) / len(red_cards)
    
    face_values = ["Jack", "Queen", "King"]
    all_face_cards = [card for card in card_deck if card[0] in face_values]
    diamond_faces = [card for card in all_face_cards if card[1] == "Diamonds"]
    prob_diamond_if_face = len(diamond_faces) / len(all_face_cards)
    
    spade_faces = [card for card in all_face_cards if card[1] == "Spades"]
    queen_faces = [card for card in all_face_cards if card[0] == "Queen"]
    combined_set = set(spade_faces + queen_faces)
    prob_spade_or_queen_if_face = len(combined_set) / len(all_face_cards)
    
    return {
        "P(Red)": prob_red,
        "P(Heart|Red)": prob_heart_if_red,
        "P(Diamond|Face)": prob_diamond_if_face,
        "P(Spade_or_Queen|Face)": prob_spade_or_queen_if_face
    }

def display_probability_results(probabilities):
    print("Card Drawing Probabilities:")
    print(f"1. Probability of drawing a red card: {probabilities['P(Red)']:.4f}")
    print(f"2. Probability of heart given red: {probabilities['P(Heart|Red)']:.4f}")
    print(f"3. Probability of diamond given face card: {probabilities['P(Diamond|Face)']:.4f}")
    print(f"4. Probability of spade or queen given face card: {probabilities['P(Spade_or_Queen|Face)']:.4f}")

def main():
    playing_deck = create_card_deck()
    probability_results = calculate_probabilities(playing_deck)
    display_probability_results(probability_results)

if __name__ == "__main__":
    main()