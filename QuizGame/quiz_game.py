import random
import time

class Question:
    def __init__(self, question, options, correct_answer, difficulty):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.difficulty = difficulty  # 1: Easy, 2: Medium, 3: Hard
        self.points = difficulty * 10

class QuizGame:
    def __init__(self):
        self.questions = [
            Question(
                "What is the capital of France?",
                ["London", "Berlin", "Paris", "Madrid"],
                2,  # Paris is at index 2 (0-based)
                1   # Easy
            ),
            Question(
                "Which planet is known as the Red Planet?",
                ["Venus", "Mars", "Jupiter", "Saturn"],
                1,  # Mars
                1
            ),
            Question(
                "What is 2^8?",
                ["128", "256", "512", "1024"],
                1,  # 256
                2   # Medium
            ),
            Question(
                "Who painted the Mona Lisa?",
                ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                2,  # Leonardo da Vinci
                1
            ),
            Question(
                "What is the largest mammal in the world?",
                ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
                1,  # Blue Whale
                1
            ),
            Question(
                "In which year did World War II end?",
                ["1943", "1945", "1947", "1950"],
                1,  # 1945
                2
            ),
            Question(
                "What is the chemical symbol for gold?",
                ["Go", "Gd", "Au", "Ag"],
                2,  # Au
                1
            ),
            Question(
                "Which language has the most native speakers?",
                ["English", "Hindi", "Spanish", "Mandarin"],
                3,  # Mandarin
                2
            ),
            Question(
                "What is the square root of 144?",
                ["10", "11", "12", "13"],
                2,  # 12
                2
            ),
            Question(
                "Who wrote 'To Kill a Mockingbird'?",
                ["Harper Lee", "Mark Twain", "J.K. Rowling", "Ernest Hemingway"],
                0,  # Harper Lee
                2
            )
        ]
        self.score = 0
        self.level = 1
        self.level_thresholds = [100, 200, 300]  # Points needed to reach levels 2, 3, and 4
    
    def start_quiz(self):
        print("\n=== Welcome to the Python Quiz Game! ===")
        print("Answer questions to earn points and level up!")
        print("Each question has a difficulty level (1-3) that determines its point value.")
        print("Let's begin!\n")
        
        # Sort questions by difficulty (easier questions first)
        sorted_questions = sorted(self.questions, key=lambda x: x.difficulty)
        
        for i, question in enumerate(sorted_questions, 1):
            print(f"\nQuestion {i} (Level {question.difficulty}, {question.points} points):")
            print(question.question)
            
            # Display options with letters (A, B, C, D)
            for idx, option in enumerate(question.options):
                print(f"{chr(65 + idx)}. {option}")
            
            # Get and validate user's answer
            while True:
                user_answer = input("\nYour answer (A/B/C/D): ").upper()
                if user_answer in ['A', 'B', 'C', 'D']:
                    break
                print("Please enter A, B, C, or D.")
            
            # Check if answer is correct
            if ord(user_answer) - 65 == question.correct_answer:
                self.score += question.points
                print(f"✅ Correct! +{question.points} points")
                
                # Check for level up
                if self.level <= len(self.level_thresholds) and self.score >= self.level_thresholds[self.level - 1]:
                    self.level += 1
                    print(f"\n🎉 Level up! You're now at level {self.level}!")
            else:
                correct_letter = chr(65 + question.correct_answer)
                print(f"❌ Incorrect! The correct answer was {correct_letter}. {question.options[question.correct_answer]}")
            
            # Show current score and level
            print(f"Current Score: {self.score} | Level: {self.level}")
            
            # Ask if user wants to continue after every 5 questions
            if i % 5 == 0 and i < len(sorted_questions):
                cont = input("\nDo you want to continue to the next set of questions? (yes/no): ").lower()
                if cont != 'yes':
                    break
        
        # Game over summary
        print("\n=== Quiz Complete! ===")
        print(f"Final Score: {self.score}")
        print(f"You reached Level {self.level}")
        
        # Performance feedback
        max_score = sum(q.points for q in sorted_questions[:i])
        percentage = (self.score / max_score) * 100
        
        if percentage >= 80:
            print("🎖️ Excellent performance! You're a quiz master!")
        elif percentage >= 60:
            print("👍 Good job! You know your stuff!")
        elif percentage >= 40:
            print("👌 Not bad! Keep learning and improving!")
        else:
            print("💪 Keep practicing! You'll get better with time!")

if __name__ == "__main__":
    while True:
        game = QuizGame()
        game.start_quiz()
        
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("\nThank you for playing the Python Quiz Game! Goodbye!")
            break
