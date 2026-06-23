import random

class PokerGame:
    def __init__(self):
        self.ranks = '23456789TJQKA'
        self.values = {r: i for i, r in enumerate(self.ranks, 2)}
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.reset_deck()
        
        self.player_stack = 200  # 100 Big Blinds (200 units)
        self.computer_stack = 200
        self.blind = 2
        self.pot = 0

    def reset_deck(self):
        self.deck = [(r, s) for r in self.ranks for s in self.suits]
        random.shuffle(self.deck)

    def deal(self, n):
        cards = self.deck[:n]
        del self.deck[:n]
        return cards

    def evaluate_strength(self, hand, board):
        # Combines hole cards and board to return a strength score (0-8)
        combined = hand + board
        scores = sorted([self.values[c[0]] for c in combined], reverse=True)
        counts = {x: scores.count(x) for x in set(scores)}
        is_flush = len(set(c[1] for c in combined)) >= 5
        
        if is_flush: return 5
        if 3 in counts.values(): return 3
        if list(counts.values()).count(2) >= 1: return 1
        return 0

    def betting_round(self, player_hand, computer_hand, board, street_name):
        print(f"\n--- {street_name} | Pot: {self.pot} ---")
        current_bet = 0
        
        # Player Turn
        print(f"Your Hand: {player_hand} | Board: {board}")
        action = input("Action: [C]heck/Call, [F]old, or Enter Bet Amount: ").upper()

        if action == 'F':
            return "FOLD_PLAYER"
        
        bet_amount = int(action) if action.isdigit() else 0
        self.player_stack -= bet_amount
        self.pot += bet_amount
        current_bet = bet_amount

        # Computer AI Logic
        comp_strength = self.evaluate_strength(computer_hand, board)
        
        if current_bet > self.computer_stack: # AI Fold if it can't afford
             return "FOLD_COMPUTER"

        if comp_strength >= 3: # AI Raises or Calls
            ai_action = current_bet + 10 if comp_strength > 4 else current_bet
            print(f"Computer calls/raises: {ai_action}")
            self.computer_stack -= ai_action
            self.pot += ai_action
        elif comp_strength >= 1 or current_bet == 0:
            print("Computer Checks/Calls.")
            self.computer_stack -= current_bet
            self.pot += current_bet
        else:
            print("Computer Folds.")
            return "FOLD_COMPUTER"
        
        return "CONTINUE"

    def play_hand(self):
        self.reset_deck()
        self.pot = self.blind + (self.blind // 2)
        self.player_stack -= self.blind
        self.computer_stack -= self.blind // 2
        
        player_hand = self.deal(2)
        computer_hand = self.deal(2)
        board = []

        # Betting Streets
        for street in ["Pre-Flop", "Flop", "Turn", "River"]:
            if street == "Flop": board += self.deal(3)
            elif street != "Pre-Flop": board += self.deal(1)
            
            result = self.betting_round(player_hand, computer_hand, board, street)
            if result == "FOLD_PLAYER":
                print("You folded. Computer takes the pot.")
                self.computer_stack += self.pot
                return
            if result == "FOLD_COMPUTER":
                print("Computer folded. You take the pot!")
                self.player_stack += self.pot
                return

        # Showdown (Simplified)
        print(f"\nShowdown! Computer had: {computer_hand}")
        # Re-use your hand_rank logic here to determine winner
        winner = "Player" # Placeholder for winner logic
        print(f"{winner} wins the pot of {self.pot}!")
        self.player_stack += self.pot

    def main_loop(self):
        while self.player_stack > 0 and self.computer_stack > 0:
            print(f"\nStacks -> You: {self.player_stack} | Computer: {self.computer_stack}")
            self.play_hand()
        print("Game Over!")

if __name__ == "__main__":
    game = PokerGame()
    game.main_loop()