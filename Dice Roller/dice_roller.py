#!/usr/bin/env python3
"""
Dice Roller Program
A Python program that simulates rolling dice with random numbers (1-6).
Demonstrates the use of the random module and loops.
"""

import random
import time

def roll_single_die():
    """
    Roll a single die and return a random number between 1 and 6.
    
    Returns:
        int: A random number between 1 and 6
    """
    return random.randint(1, 6)

def roll_multiple_dice(num_dice):
    """
    Roll multiple dice and return a list of results.
    
    Args:
        num_dice (int): Number of dice to roll
        
    Returns:
        list: List of random numbers between 1 and 6
    """
    return [roll_single_die() for _ in range(num_dice)]

def display_dice_results(results):
    """
    Display dice results in a nice format.
    
    Args:
        results (list): List of dice roll results
    """
    print("🎲 Dice Results:")
    for i, result in enumerate(results, 1):
        print(f"  Die {i}: {result}")
    
    if len(results) > 1:
        total = sum(results)
        print(f"  Total: {total}")
        print(f"  Average: {total/len(results):.1f}")

def get_user_choice():
    """
    Get user's choice for what to do next.
    
    Returns:
        str: User's choice
    """
    print("\n" + "="*50)
    print("What would you like to do?")
    print("1. Roll a single die")
    print("2. Roll multiple dice")
    print("3. Roll dice in a loop")
    print("4. Exit")
    print("="*50)
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")

def roll_in_loop():
    """
    Demonstrate rolling dice in a loop with user control.
    """
    print("\n🔄 Rolling dice in a loop!")
    print("Press Enter to roll, type 'stop' to end, or 'auto' for automatic rolling")
    
    roll_count = 0
    
    while True:
        user_input = input("\nPress Enter to roll (or 'stop'/'auto'): ").strip().lower()
        
        if user_input == 'stop':
            print(f"Stopped after {roll_count} rolls. Thanks for playing!")
            break
        elif user_input == 'auto':
            # Automatic rolling for demonstration
            num_rolls = input("How many automatic rolls? (1-20): ").strip()
            try:
                num_rolls = int(num_rolls)
                if 1 <= num_rolls <= 20:
                    print(f"\n🎲 Rolling {num_rolls} dice automatically...")
                    for i in range(num_rolls):
                        result = roll_single_die()
                        print(f"  Roll {i+1}: {result}")
                        time.sleep(0.5)  # Small delay for effect
                        roll_count += 1
                else:
                    print("Please enter a number between 1 and 20.")
            except ValueError:
                print("Please enter a valid number.")
        elif user_input == '' or user_input == 'roll':
            # Single roll
            result = roll_single_die()
            roll_count += 1
            print(f"🎲 Roll {roll_count}: {result}")
        else:
            print("Invalid input! Press Enter to roll, 'stop' to end, or 'auto' for automatic rolling.")

def main():
    """
    Main function that runs the dice roller program.
    """
    print("🎲 Welcome to the Python Dice Roller! 🎲")
    print("This program demonstrates random number generation and loops.")
    
    while True:
        choice = get_user_choice()
        
        if choice == '1':
            # Roll a single die
            print("\n🎲 Rolling a single die...")
            result = roll_single_die()
            print(f"Result: {result}")
            
        elif choice == '2':
            # Roll multiple dice
            while True:
                try:
                    num_dice = int(input("\nHow many dice would you like to roll? (1-10): "))
                    if 1 <= num_dice <= 10:
                        break
                    else:
                        print("Please enter a number between 1 and 10.")
                except ValueError:
                    print("Please enter a valid number.")
            
            print(f"\n🎲 Rolling {num_dice} dice...")
            results = roll_multiple_dice(num_dice)
            display_dice_results(results)
            
        elif choice == '3':
            # Roll dice in a loop
            roll_in_loop()
            
        elif choice == '4':
            # Exit
            print("\n🎲 Thanks for using the Dice Roller! Goodbye! 🎲")
            break

def demonstrate_random_concepts():
    """
    Demonstrate various random concepts for learning purposes.
    """
    print("\n" + "="*60)
    print("📚 RANDOM MODULE DEMONSTRATION")
    print("="*60)
    
    # Demonstrate random.randint()
    print("\n1. random.randint(1, 6) - generates random integers between 1 and 6:")
    for i in range(5):
        print(f"   Roll {i+1}: {random.randint(1, 6)}")
    
    # Demonstrate random.choice()
    print("\n2. random.choice() - picks a random item from a list:")
    dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    print("   Dice faces:", dice_faces)
    for i in range(3):
        print(f"   Random face {i+1}: {random.choice(dice_faces)}")
    
    # Demonstrate list comprehension with random
    print("\n3. List comprehension with random - generate multiple rolls:")
    rolls = [random.randint(1, 6) for _ in range(10)]
    print(f"   10 random rolls: {rolls}")
    print(f"   Sum of all rolls: {sum(rolls)}")
    print(f"   Average roll: {sum(rolls)/len(rolls):.2f}")
    
    # Demonstrate loops
    print("\n4. For loop - rolling dice 5 times:")
    for i in range(5):
        result = random.randint(1, 6)
        print(f"   Iteration {i+1}: {result}")
    
    print("\n5. While loop - rolling until we get a 6:")
    attempts = 0
    while True:
        attempts += 1
        result = random.randint(1, 6)
        print(f"   Attempt {attempts}: {result}")
        if result == 6:
            print(f"   Got a 6 after {attempts} attempts!")
            break

if __name__ == "__main__":
    # Ask if user wants to see the demonstration
    demo_choice = input("Would you like to see a demonstration of random concepts first? (y/n): ").strip().lower()
    if demo_choice in ['y', 'yes']:
        demonstrate_random_concepts()
    
    # Run the main program
    main()
