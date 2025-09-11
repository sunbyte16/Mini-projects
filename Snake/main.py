'''
Snake-Water-Gun Game

Game Rules:
🐍 Snake vs Water → Snake drinks Water, Snake wins
💧 Water vs Gun → Water drowns Gun, Water wins
🔫 Gun vs Snake → Gun kills Snake, Gun wins

Coding values:
1 for snake
-1 for water
0 for gun
'''

import random
import os
import time

def clear_screen():
    """Clear the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    """Display welcome message and game rules."""
    print("\n" + "=" * 50)
    print("🎮 Welcome to Snake-Water-Gun Game! 🎮".center(50))
    print("=" * 50)
    print("\nGame Rules:")
    print("🐍 Snake vs Water → Snake drinks Water, Snake wins")
    print("💧 Water vs Gun → Water drowns Gun, Water wins")
    print("🔫 Gun vs Snake → Gun kills Snake, Gun wins")
    print("\nHow to play:")
    print("- Enter 's' for Snake 🐍")
    print("- Enter 'w' for Water 💧")
    print("- Enter 'g' for Gun 🔫")
    print("- Enter 'q' to quit the game")
    print("=" * 50 + "\n")

def get_user_choice():
    """Get and validate user's choice."""
    while True:
        choice = input("\nEnter your choice (s/w/g) or 'q' to quit: ").lower()
        if choice in ['s', 'w', 'g', 'q']:
            return choice
        print("❌ Invalid choice! Please enter 's' for Snake, 'w' for Water, 'g' for Gun, or 'q' to quit.")

def get_computer_choice():
    """Generate computer's choice."""
    return random.choice([1, -1, 0])  # 1 for snake, -1 for water, 0 for gun

def determine_winner(user, computer):
    """Determine the winner based on the game rules."""
    if user == computer:
        return "draw"
    
    # Using the mathematical relationship from Shortened_Code.py
    if (computer - user) == -1 or (computer - user) == 2:
        return "user"
    else:
        return "computer"

def display_result(user_choice, computer_choice, result):
    """Display the game result with visual elements."""
    choice_dict = {1: "Snake 🐍", -1: "Water 💧", 0: "Gun 🔫"}
    
    print("\n" + "-" * 50)
    print(f"You chose: {choice_dict[user_choice]}")
    print(f"Computer chose: {choice_dict[computer_choice]}")
    
    if result == "draw":
        print("\n🤝 It's a Draw! 🤝")
    elif result == "user":
        print("\n🎉 You Win! 🎉")
    else:
        print("\n😢 You Lose! 😢")
    print("-" * 50)

def play_game():
    """Main game function."""
    clear_screen()
    display_welcome()
    
    user_score = 0
    computer_score = 0
    rounds_played = 0
    
    choice_mapping = {"s": 1, "w": -1, "g": 0}  # Map user input to game values
    
    while True:
        user_input = get_user_choice()
        
        if user_input == 'q':
            break
        
        user_choice = choice_mapping[user_input]
        computer_choice = get_computer_choice()
        rounds_played += 1
        
        result = determine_winner(user_choice, computer_choice)
        display_result(user_choice, computer_choice, result)
        
        if result == "user":
            user_score += 1
        elif result == "computer":
            computer_score += 1
        
        print(f"\nScore: You {user_score} - {computer_score} Computer (Rounds: {rounds_played})")
        print("\nPress Enter to continue...")
        input()
    
    # Display final score
    if rounds_played > 0:
        clear_screen()
        print("\n" + "=" * 50)
        print("🏆 Game Over - Final Results 🏆".center(50))
        print("=" * 50)
        print(f"\nRounds Played: {rounds_played}")
        print(f"Your Score: {user_score}")
        print(f"Computer's Score: {computer_score}")
        
        if user_score > computer_score:
            print("\n🎉🎉🎉 Congratulations! You Won The Game! 🎉🎉🎉")
        elif computer_score > user_score:
            print("\n😢 Better luck next time! Computer Won The Game! 😢")
        else:
            print("\n🤝 It's a Tie! 🤝")
        print("\nThanks for playing!")
        print("=" * 50)

# Start the game
if __name__ == "__main__":
    play_game()