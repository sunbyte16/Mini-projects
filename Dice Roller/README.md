<div align="center">

# 🎲 Python Dice Roller

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg?style=for-the-badge)](https://github.com/sunbyte16)

*A comprehensive Python program that demonstrates random number generation and loops by simulating dice rolls*

[🚀 Features](#-features) • [📚 Learning](#-what-youll-learn) • [🛠️ Installation](#️-installation) • [💻 Usage](#-usage) • [📖 Examples](#-code-examples)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [📁 Project Structure](#-project-structure)
- [🎓 What You'll Learn](#-what-youll-learn)
- [🛠️ Installation](#️-installation)
- [💻 Usage](#-usage)
- [🚀 Features](#-features)
- [📖 Code Examples](#-code-examples)
- [🎯 Learning Objectives](#-learning-objectives)
- [⚙️ Requirements](#️-requirements)
- [🔧 Try These Variations](#-try-these-variations)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

## 🎯 Overview

This project provides two Python implementations of a dice roller program designed to teach fundamental programming concepts:

- **Random number generation** using Python's `random` module
- **Loop structures** including `for` and `while` loops
- **Function organization** and code structure
- **User interaction** and input validation

Perfect for beginners learning Python or anyone wanting to understand random number generation and loop concepts!

---

## 📁 Project Structure

```
📦 Dice Roller
├── 📄 dice_roller.py          # Full-featured version with menu system
├── 📄 simple_dice_roller.py   # Beginner-friendly version
├── 📄 README.md              # This file
└── 📄 LICENSE                # MIT License
```

---

## 🎓 What You'll Learn

### 🎲 Random Module
- `random.randint(1, 6)` - Generate random integers between 1 and 6
- `random.choice()` - Pick random items from a list
- List comprehensions with random numbers
- Probability and randomness concepts

### 🔄 Loops
- **For loops** - Roll dice a specific number of times
- **While loops** - Continue rolling until a condition is met
- **Interactive loops** - User-controlled rolling
- Loop control with `break` and `continue`

### 💻 Programming Concepts
- Function creation and organization
- Input validation and error handling
- User interface design
- Code documentation and comments
- Modular programming

---

## 🛠️ Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required

### Quick Start
```bash
# Clone the repository
git clone https://github.com/sunbyte16/dice-roller.git
cd dice-roller

# Run the program
python dice_roller.py
```

---

## 💻 Usage

### 🎮 Full Version (Recommended)
```bash
python dice_roller.py
```
**Features:**
- Interactive menu system
- Educational demonstrations
- Multiple rolling modes
- Statistics and analytics

### 🎯 Simple Version (Beginner)
```bash
python simple_dice_roller.py
```
**Features:**
- Step-by-step examples
- Clear code comments
- Perfect for learning basics

---

## 🚀 Features

### 🎲 Full Version (`dice_roller.py`)
- ✅ **Single Die Rolling** - Roll one die at a time
- ✅ **Multiple Dice** - Roll 1-10 dice simultaneously
- ✅ **Interactive Loops** - Continuous rolling with user control
- ✅ **Educational Mode** - Demonstrates random concepts
- ✅ **Statistics** - Total, average, and roll history
- ✅ **Beautiful UI** - Emojis and formatted output
- ✅ **Input Validation** - Robust error handling

### 🎯 Simple Version (`simple_dice_roller.py`)
- ✅ **Basic Examples** - Clear, commented code
- ✅ **For Loop Demo** - Roll multiple dice
- ✅ **While Loop Demo** - Roll until condition met
- ✅ **Interactive Mode** - User-controlled rolling
- ✅ **Learning Focus** - Perfect for beginners

---

## 📖 Code Examples

### 🎲 Basic Dice Roll
```python
import random

def roll_die():
    """Roll a single die and return 1-6"""
    return random.randint(1, 6)

result = roll_die()
print(f"🎲 You rolled: {result}")
```

### 🔄 Roll Multiple Dice
```python
# Using for loop
dice_results = []
for i in range(5):
    roll = random.randint(1, 6)
    dice_results.append(roll)
    print(f"Roll {i+1}: {roll}")

# Using list comprehension (more Pythonic)
dice_results = [random.randint(1, 6) for _ in range(5)]
print(f"All results: {dice_results}")
print(f"Total: {sum(dice_results)}")
```

### ⚡ Roll Until Condition
```python
attempts = 0
while True:
    attempts += 1
    roll = random.randint(1, 6)
    print(f"Attempt {attempts}: {roll}")
    if roll == 6:
        print(f"🎯 Got a 6 after {attempts} attempts!")
        break
```

### 🎮 Interactive Rolling
```python
while True:
    user_input = input("Press Enter to roll (or 'quit'): ")
    if user_input.lower() == 'quit':
        break
    result = random.randint(1, 6)
    print(f"🎲 You rolled: {result}")
```

---

## 🎯 Learning Objectives

| Objective | Status | Description |
|-----------|--------|-------------|
| ✅ Random Module | Complete | Understand `random.randint()` and `random.choice()` |
| ✅ For Loops | Complete | Learn to iterate a specific number of times |
| ✅ While Loops | Complete | Continue until conditions are met |
| ✅ Functions | Complete | Organize code with reusable functions |
| ✅ User Input | Complete | Handle user interaction and validation |
| ✅ Error Handling | Complete | Validate inputs and handle exceptions |
| ✅ Code Organization | Complete | Structure code for readability |

---

## ⚙️ Requirements

- **Python**: 3.6 or higher
- **Dependencies**: None (uses only built-in modules)
- **Operating System**: Cross-platform (Windows, macOS, Linux)

---

## 🔧 Try These Variations

### 🎯 Beginner Challenges
1. **🎲 Double Dice** - Roll two dice and add them together
2. **📊 Statistics** - Keep track of how many times each number appears
3. **🎯 Target Practice** - Roll until you get a specific number

### 🚀 Intermediate Challenges
4. **🎮 Cheat Mode** - Add a "cheat mode" that always rolls 6
5. **🎲 Custom Dice** - Create dice with different numbers of sides (4, 8, 12, 20)
6. **🎯 Probability** - Calculate the probability of rolling certain combinations

### 🏆 Advanced Challenges
7. **🎮 Game Integration** - Create a dice game like Yahtzee or Farkle
8. **📈 Data Visualization** - Graph the distribution of dice rolls
9. **🤖 AI Opponent** - Add computer players with different strategies

---

## 👨‍💻 Author

<div align="center">

**Created By ❤️Sunil Sharma❤️**

[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20My%20Site-FF5722?style=for-the-badge&logo=firefox&logoColor=white)](https://lively-dodol-cc397c.netlify.app)

*Passionate about creating educational programming projects that make learning fun and engaging!*

</div>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

**Happy Coding! 🚀**

</div>
