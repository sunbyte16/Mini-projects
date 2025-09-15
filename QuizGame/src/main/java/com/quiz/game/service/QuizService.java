package com.quiz.game.service;

import com.quiz.game.model.Question;
import com.quiz.game.model.Quiz;
import com.quiz.game.model.Score;
import java.util.List;
import java.util.Scanner;

public class QuizService {
    private final QuestionService questionService;
    private final ScoreService scoreService;
    private final Scanner scanner;

    public QuizService(QuestionService questionService, ScoreService scoreService) {
        this.questionService = questionService;
        this.scoreService = scoreService;
        this.scanner = new Scanner(System.in);
    }

    public void startNewQuiz(String playerName, String category, String difficulty, int numQuestions, long timeLimit) {
        // Get random questions based on filters
        List<Question> questions = questionService.getRandomQuestions(category, difficulty, numQuestions);
        
        if (questions.isEmpty()) {
            System.out.println("No questions available with the selected criteria. Please try different options.");
            return;
        }

        // Create and start the quiz
        Quiz quiz = new Quiz(playerName, questions, timeLimit);
        System.out.printf("\n=== Starting Quiz: %s (%s) ===\n", 
            category != null ? category : "All Categories",
            difficulty != null ? difficulty : "All Levels");
        
        long startTime = System.currentTimeMillis();
        
        // Main quiz loop
        while (!quiz.isCompleted() && !quiz.isTimeUp()) {
            Question currentQuestion = quiz.getCurrentQuestion();
            if (currentQuestion == null) break;
            
            // Display question and options
            System.out.printf("\nQuestion %d of %d\n", 
                quiz.getCurrentQuestionIndex() + 1, quiz.getTotalQuestions());
            System.out.println(currentQuestion.getFormattedQuestion());
            
            // Show time remaining if time limit is set
            if (timeLimit > 0) {
                int remaining = quiz.getRemainingTime();
                System.out.printf("Time remaining: %d seconds\n", remaining);
            }
            
            // Get user input
            System.out.print("Your answer (1-4, 0 to skip): ");
            int answer = -1;
            try {
                answer = Integer.parseInt(scanner.nextLine().trim());
                if (answer < 0 || answer > currentQuestion.getOptions().size()) {
                    System.out.println("Invalid option. Please try again.");
                    continue;
                }
                
                if (answer == 0) {
                    quiz.skipCurrentQuestion();
                    System.out.println("Question skipped!");
                } else {
                    boolean isCorrect = quiz.answerCurrentQuestion(answer - 1);
                    System.out.println(isCorrect ? "✅ Correct!" : "❌ Incorrect!");
                }
                
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
            }
            
            // Check if time's up after each question
            if (quiz.isTimeUp()) {
                System.out.println("\n⏰ Time's up!");
                break;
            }
        }
        
        // Calculate time taken
        long timeTaken = (System.currentTimeMillis() - startTime) / 1000;
        
        // Quiz completed, show results
        showQuizResults(quiz, timeTaken);
    }
    
    private void showQuizResults(Quiz quiz, long timeTaken) {
        System.out.println("\n=== QUIZ COMPLETED ===");
        System.out.printf("Player: %s\n", quiz.getPlayerName());
        System.out.printf("Score: %d/%d\n", quiz.getScore(), quiz.getTotalQuestions() * 10);
        System.out.printf("Correct Answers: %d/%d\n", 
            quiz.getCorrectAnswers(), quiz.getTotalQuestions());
        System.out.printf("Accuracy: %.1f%%\n", quiz.getPercentageScore());
        System.out.printf("Time Taken: %d seconds\n", timeTaken);
        
        // Save score
        Score score = new Score(
            quiz.getPlayerName(),
            quiz.getScore(),
            quiz.getTotalQuestions(),
            quiz.getCorrectAnswers(),
            "Mixed", // Category
            "Mixed", // Difficulty
            timeTaken
        );
        
        scoreService.addScore(score);
        
        // Show high scores
        showHighScores();
    }
    
    private void showHighScores() {
        System.out.println("\n=== TOP 5 HIGH SCORES ===");
        List<Score> topScores = scoreService.getTopScores(5);
        if (topScores.isEmpty()) {
            System.out.println("No high scores yet!");
            return;
        }
        
        for (int i = 0; i < topScores.size(); i++) {
            Score score = topScores.get(i);
            System.out.printf("%d. %s - %d points (%d/%d) - %s\n",
                i + 1, score.getPlayerName(), score.getScore(),
                score.getCorrectAnswers(), score.getTotalQuestions(),
                score.getFormattedDateTime());
        }
    }
    
    public void showPlayerStats(String playerName) {
        var stats = scoreService.getPlayerStats(playerName);
        
        System.out.println("\n=== PLAYER STATISTICS ===");
        System.out.printf("Player: %s\n", playerName);
        System.out.printf("Games Played: %d\n", stats.get("gamesPlayed"));
        System.out.printf("Total Score: %d\n", stats.get("totalScore"));
        System.out.printf("Average Score: %d\n", stats.get("averageScore"));
        System.out.printf("Best Score: %d\n", stats.get("bestScore"));
        System.out.printf("Best Category: %s\n", stats.get("bestCategory"));
        System.out.printf("Total Correct Answers: %d/%d (%.1f%%)\n",
            stats.get("totalCorrect"), stats.get("totalQuestions"),
            stats.get("totalQuestions") > 0 ? 
                (stats.get("totalCorrect") * 100.0) / stats.get("totalQuestions") : 0);
    }
}
