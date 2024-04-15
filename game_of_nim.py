import random

# Prompt the user to enter the initial number of balls
def prompt_user():
    while True:
        try:
            number_of_balls = int(input("Enter the number of balls (15 or more): "))
            if number_of_balls >= 15:
                return number_of_balls
            else:
                print("Please enter a number of 15 or more.")
        except ValueError:
            print("Please enter a valid integer.")

# Validate the input during the human player's turn
def validate_input(prompt, min_val=1, max_val=4):
    while True:
        try:
            user_input = int(input(prompt))
            if min_val <= user_input <= max_val:
                return user_input
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid integer.")

# This function handles the human player's turn
def human_turn(total_balls):
    print(f"\nThere are {total_balls} balls remaining.")
    balls_to_remove = validate_input("How many balls would you like to remove (1-4)? ")
    return balls_to_remove

# This function handles the computer's turn.
def computer_turn(total_balls):
    # Choose a random number of balls to remove, ensuring it's not more than the remaining
    balls_to_remove = random.randint(1, min(4, total_balls))
    print(f"\nThe computer removes {balls_to_remove} ball(s).")
    return balls_to_remove

# Check if there is a winner
def check_winner(total_balls, last_player):
    if total_balls <= 0:
        if last_player == "human":
            print("\nCongratulations! You've won the game!")
        else:
            print("\nThe computer has won the game. Better luck next time!")
        return True
    return False

# Manage a round of the game
def game_round(total_balls):
    while total_balls > 0:
        # THis is the human's turn
        total_balls -= human_turn(total_balls)
        if check_winner(total_balls, "human"):
            break
        # This is the computer's turn
        total_balls -= computer_turn(total_balls)
        if check_winner(total_balls, "computer"):
            break

# This is the main function controlling the flow of the game
def main():
    print("Welcome to the game of Nim!")
    total_balls = prompt_user()  # Initial setup
    game_round(total_balls)  # Start the game rounds

if __name__ == "__main__":
    main()