<div align="center">

# 🎮 Memory Game (Card Flip)

### *A Classic Memory Challenge in C Language* 🧠

[![C](https://img.shields.io/badge/Language-C-blue.svg)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Version](https://img.shields.io/badge/Version-1.0.0-red.svg)]()

*Test your memory skills with this engaging card matching game!*

</div>

---

## 🎯 **Game Overview**

A beautifully crafted memory game where players flip cards to discover matching pairs. Built with pure C language for optimal performance and cross-platform compatibility.

## ✨ **Key Features**

🎲 **4×4 Grid Layout** - 16 strategically placed cards  
🔢 **8 Unique Pairs** - Numbers 1-8, each appearing twice  
🎮 **Turn-Based Gameplay** - Flip 2 cards per turn  
🧠 **Memory Challenge** - Cards hide after each unsuccessful match  
🏆 **Victory Condition** - Match all 8 pairs to win  
✅ **Input Validation** - Robust error handling system  
🎨 **Clean Interface** - Clear visual feedback and instructions  
🎊 **Personalized Experience** - Custom welcome messages  

## 🕹️ **How to Play**

> 🎯 **Objective**: Find all matching pairs by remembering card positions!

1. 👀 View the 4×4 grid of hidden cards (displayed as `##`)
2. 🔢 Each card contains a number from 1 to 8
3. 🎲 Each number appears exactly twice on the board
4. 🎮 Flip 2 cards per turn by entering row and column coordinates
5. ✅ Matching cards stay revealed permanently
6. ❌ Non-matching cards get hidden again
7. 🏆 Continue until all pairs are successfully matched!

## 🔧 **Installation & Setup**

### 🚀 **Quick Start**
```bash
# Clone and navigate to directory
cd memory-game

# Compile the game
gcc -Wall -Wextra -std=c99 -o memory_game main.c

# Run and enjoy!
./memory_game
```

### 🛠️ **Compilation Options**

**Using GCC (Recommended):**
```bash
gcc -Wall -Wextra -std=c99 -o memory_game main.c
./memory_game
```

**Using Makefile:**
```bash
make          # Build the game
make run      # Build and run
make clean    # Clean build files
```

**Windows (PowerShell/CMD):**
```cmd
gcc -o memory_game.exe main.c
memory_game.exe
```

## 🎮 **Game Controls**

| Input | Action |
|-------|--------|
| `1-4` | Row selection (when prompted) |
| `1-4` | Column selection (when prompted) |
| `Enter` | Continue after viewing flipped cards |
| `Ctrl+C` | Exit game |

> 💡 **Tip**: Invalid inputs are automatically rejected with helpful error messages!

## 🎨 **Game Board Visualization**

**Hidden Cards:**
```
     1   2   3   4
 1  ## ## ## ##
 2  ## ## ## ##  
 3  ## ## ## ##
 4  ## ## ## ##
```

**Revealed Cards:**
```
     1   2   3   4
 1   3 ##  7 ##
 2  ## ## ##  7
 3   3 ## ## ##
 4  ## ## ## ##
```

## 🏗️ **Technical Architecture**

### 📁 **Project Structure**
```
memory-game/
├── 📄 main.c          # Core game implementation
├── 📄 Makefile        # Build configuration
├── 📄 README.md       # Documentation
├── 📄 test.bat        # Windows test script
└── 📄 memory_game.exe # Compiled executable
```

### 🔧 **Code Components**

- **🎯 Card Structure**: Value storage, flip state, and match tracking
- **🎲 Board Management**: 4×4 array with intelligent shuffling algorithm
- **🔄 Game Loop**: Input handling, card flipping, and match validation
- **🎨 Display Engine**: Clean board visualization and user feedback
- **✅ Input Validation**: Comprehensive error handling and user guidance

## 📋 **System Requirements**

| Component | Requirement |
|-----------|-------------|
| 💻 **Compiler** | GCC 4.8+ (or compatible C99 compiler) |
| 📚 **Libraries** | Standard C Library |
| 🖥️ **Platform** | Windows, Linux, macOS |
| 💾 **Memory** | < 1MB RAM |
| 📺 **Display** | Console/Terminal support |

## 🎊 **Screenshots**

*Experience the clean, intuitive interface that makes memory training enjoyable!*

---

<div align="center">

## 👨‍💻 **Created By Sunil Sharma** ❤️

### *Passionate Developer | Problem Solver | Tech Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-@sunbyte16-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20Now-FF6B6B?style=for-the-badge&logo=firefox&logoColor=white)](https://lively-dodol-cc397c.netlify.app)

*"Building innovative solutions, one line of code at a time"* 💻✨

---

### 🌟 **Connect With Me**

**🔗 Links:**  
🐙 **GitHub**: [@sunbyte16](https://github.com/sunbyte16)  
💼 **LinkedIn**: [Sunil Kumar](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)  
🌐 **Portfolio**: [Visit My Work](https://lively-dodol-cc397c.netlify.app)  

---

**⭐ If you enjoyed this game, please give it a star!**

*Happy Gaming! 🎮*

</div>