#!/usr/bin/env python3
"""
Simple Dice Roller - Beginner Version
A basic Python program to learn random numbers and loops.
"""

import random

# Simple function to roll one die
def roll_die():
    """Roll a single die and return a number from 1 to 6."""
    return random.randint(1, 6)

# Main program
print("🎲 Simple Dice Roller 🎲")
print("This program rolls dice with random numbers from 1 to 6!")

# Example 1: Roll a single die
print("\n--- Example 1: Roll a single die ---")
result = roll_die()
print(f"You rolled: {result}")

# Example 2: Roll multiple dice using a for loop
print("\n--- Example 2: Roll 5 dice using a for loop ---")
dice_results = []
for i in range(5):
    roll = roll_die()
    dice_results.append(roll)
    print(f"Roll {i+1}: {roll}")

print(f"All results: {dice_results}")
print(f"Total: {sum(dice_results)}")

# Example 3: Roll dice until you get a 6 (while loop)
print("\n--- Example 3: Roll until you get a 6 (while loop) ---")
attempts = 0
while True:
    attempts += 1
    roll = roll_die()
    print(f"Attempt {attempts}: {roll}")
    if roll == 6:
        print(f"Got a 6 after {attempts} attempts!")
        break

# Example 4: Interactive dice rolling
print("\n--- Example 4: Interactive rolling ---")
while True:
    user_input = input("\nPress Enter to roll a die (or type 'quit' to exit): ")
    
    if user_input.lower() == 'quit':
        print("Thanks for playing!")
        break
    else:
        result = roll_die()
        print(f"🎲 You rolled: {result}")

print("\n🎲 Program finished! You've learned about:")
print("- random.randint() for generating random numbers")
print("- for loops for repeating actions")
print("- while loops for continuing until a condition is met")
print("- functions for organizing code")
