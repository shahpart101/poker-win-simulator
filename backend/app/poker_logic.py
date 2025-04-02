from treys import Deck, Evaluator, Card

evaluator = Evaluator()

def simulate_win_probability(hole_cards, community_cards, num_simulations=1000):
    wins = 0
    ties = 0

    known_cards = hole_cards + community_cards

    for _ in range(num_simulations):
        deck = Deck()
        for card in known_cards:
            deck.cards.remove(card)  # remove known cards from the deck

        opponent_hole = deck.draw(2)
        remaining_board = deck.draw(5 - len(community_cards))
        full_board = community_cards + remaining_board

        your_score = evaluator.evaluate(hole_cards, full_board)
        opp_score = evaluator.evaluate(opponent_hole, full_board)

        if your_score < opp_score:
            wins += 1
        elif your_score == opp_score:
            ties += 1

    return {
        "win_rate": round((wins / num_simulations) * 100, 2),
        "tie_rate": round((ties / num_simulations) * 100, 2)
    }
