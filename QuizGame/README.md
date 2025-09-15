# Quiz Game

A Java console-based Quiz Game that tests your knowledge with multiple-choice questions across various categories.

## Features

- Multiple question categories (General Knowledge, Science, History, etc.)
- Score tracking and performance feedback
- Timer for each question
- Multiple difficulty levels
- Progress tracking
- Final score summary

## Prerequisites

- Java Development Kit (JDK) 8 or higher

## How to Run

1. Navigate to the project directory
2. Compile the Java files:
   ```
   javac src/main/java/com/quiz/game/*.java -d target/classes
   ```
3. Run the application:
   ```
   java -cp target/classes com.quiz.game.QuizGame
   ```

## Game Rules

- Each correct answer awards points based on difficulty
- Answer quickly to earn bonus points
- No negative marking for wrong answers
- View your final score and performance at the end

## Project Structure

```
src/main/java/com/quiz/game/
├── model/
│   ├── Question.java
│   ├── Quiz.java
│   └── Score.java
├── service/
│   ├── QuestionService.java
│   └── QuizService.java
└── QuizGame.java  # Main application class
```

## Categories

- General Knowledge
- Science
- History
- Geography
- Entertainment
- Sports
- Technology
- Mathematics

## Difficulty Levels

- Easy
- Medium
- Hard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
