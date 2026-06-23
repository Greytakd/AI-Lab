import random, sys
valid_choices = ['rock', 'paper', 'scissors']
wins = 0
losses = 0
ties = 0
end_game = False
while end_game != True:
    user_value = input("Enter your choice (rock, paper, scissors): ").lower()
    if user_value not in valid_choices:
        print("Invalid choice. Please choose rock, paper, or scissors.")
        sys.exit()
    comp_value = random.choice(valid_choices)
    print(f"Computer chose: {comp_value}")
    if user_value == comp_value:
        print("It's a tie!")
        ties += 1
    elif (user_value == 'rock' and comp_value == 'scissors') or \
            (user_value == 'paper' and comp_value == 'rock') or \
            (user_value == 'scissors' and comp_value == 'paper'):
        print("You win!")
        wins += 1
    else:
        print("You lose!")
        losses += 1
    print(f"Score -> Wins: {wins}, Losses: {losses}, Ties: {ties}")
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        end_game = True
        print("Thanks for playing!")