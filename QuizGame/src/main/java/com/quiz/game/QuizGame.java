package com.quiz.game;

import com.quiz.game.model.Question;
import com.quiz.game.model.Score;
import com.quiz.game.service.QuestionService;
import com.quiz.game.service.QuizService;
import com.quiz.game.service.ScoreService;

import java.util.*;

public class QuizGame {
    private final Scanner scanner;
    private final QuestionService questionService;
    private final ScoreService scoreService;
    private final QuizService quizService;
    private String currentPlayer;

    public QuizGame() {
        this.scanner = new Scanner(System.in);
        this.questionService = new QuestionService();
        this.scoreService = new ScoreService();
        this.quizService = new QuizService(questionService, scoreService);
        this.currentPlayer = "Guest";
    }

    public void start() {
        System.out.println("\n=== WELCOME TO THE QUIZ GAME ===");
        
        // Main game loop
        boolean running = true;
        while (running) {
            displayMainMenu();
            int choice = getIntInput("Enter your choice (1-5): ", 1, 5);
            
            switch (choice) {
                case 1 -> startNewQuiz();
                case 2 -> viewHighScores();
                case 3 -> viewPlayerStats();
                case 4 -> changePlayer();
                case 5 -> running = false;
                default -> System.out.println("Invalid choice. Please try again.");
            }
            
            if (running) {
                System.out.println("\nPress Enter to continue...");
                scanner.nextLine();
            }
        }
        
        System.out.println("\nThank you for playing! Goodbye!");
        scanner.close();
    }
    
    private void displayMainMenu() {
        System.out.println("\n=== MAIN MENU ===");
        System.out.printf("Current Player: %s%n", currentPlayer);
        System.out.println("1. Start New Quiz");
        System.out.println("2. View High Scores");
        System.out.println("3. View My Stats");
        System.out.println("4. Change Player");
        System.out.println("5. Exit");
    }
    
    private void startNewQuiz() {
        System.out.println("\n=== NEW QUIZ ===");
        
        // Get quiz preferences
        String category = selectCategory();
        String difficulty = selectDifficulty();
        int numQuestions = getNumberOfQuestions();
        long timeLimit = getTimeLimit();
        
        // Start the quiz with selected options
        quizService.startNewQuiz(currentPlayer, category, difficulty, numQuestions, timeLimit);
    }
    
    private String selectCategory() {
        List<String> categories = questionService.getAllCategories();
        categories.add(0, "All Categories");
        
        System.out.println("\nSelect a category:");
        for (int i = 0; i < categories.size(); i++) {
            System.out.printf("%d. %s%n", i + 1, categories.get(i));
        }
        
        int choice = getIntInput("Enter your choice (1-" + categories.size() + "): ", 1, categories.size());
        return choice == 1 ? null : categories.get(choice - 1);
    }
    
    private String selectDifficulty() {
        List<String> difficulties = questionService.getAllDifficulties();
        difficulties.add(0, "All Levels");
        
        System.out.println("\nSelect difficulty:");
        for (int i = 0; i < difficulties.size(); i++) {
            System.out.printf("%d. %s%n", i + 1, difficulties.get(i));
        }
        
        int choice = getIntInput("Enter your choice (1-" + difficulties.size() + "): ", 1, difficulties.size());
        return choice == 1 ? null : difficulties.get(choice - 1);
    }
    
    private int getNumberOfQuestions() {
        return getIntInput("\nEnter number of questions (5-20): ", 5, 20);
    }
    
    private long getTimeLimit() {
        System.out.println("\nSelect time limit:");
        System.out.println("1. No time limit");
        System.out.println("2. 30 seconds per question");
        System.out.println("3. 1 minute per question");
        System.out.println("4. 2 minutes per question");
        
        int choice = getIntInput("Enter your choice (1-4): ", 1, 4);
        return switch (choice) {
            case 2 -> 30;
            case 3 -> 60;
            case 4 -> 120;
            default -> 0; // No time limit
        };
    }
    
    private void viewHighScores() {
        System.out.println("\n=== HIGH SCORES ===");
        System.out.println("1. All-time High Scores");
        System.out.println("2. High Scores by Category");
        System.out.println("3. High Scores by Difficulty");
        
        int choice = getIntInput("Enter your choice (1-3): ", 1, 3);
        
        switch (choice) {
            case 1 -> displayTopScores(null, null);
            case 2 -> {
                String category = selectCategory();
                displayTopScores(category, null);
            }
            case 3 -> {
                String difficulty = selectDifficulty();
                displayTopScores(null, difficulty);
            }
        }
    }
    
    private void displayTopScores(String category, String difficulty) {
        List<Score> topScores = scoreService.getTopScores(category, difficulty, 10);
        
        if (topScores.isEmpty()) {
            System.out.println("No scores found for the selected criteria.");
            return;
        }
        
        System.out.println("\n=== TOP SCORES ===");
        System.out.printf("%-4s %-20s %-8s %-10s %-10s %-15s%n",
            "#", "Player", "Score", "Correct", "Time", "Date");
        System.out.println("-".repeat(70));
        
        for (int i = 0; i < topScores.size(); i++) {
            Score score = topScores.get(i);
            System.out.printf("%-4d %-20s %-8d %-10d %-10s %-15s%n",
                i + 1,
                score.getPlayerName(),
                score.getScore(),
                score.getCorrectAnswers(),
                score.getFormattedTimeTaken(),
                score.getDateTime().toLocalDate());
        }
    }
    
    private void viewPlayerStats() {
        quizService.showPlayerStats(currentPlayer);
    }
    
    private void changePlayer() {
        System.out.print("\nEnter your name: ");
        String name = scanner.nextLine().trim();
        if (!name.isEmpty()) {
            currentPlayer = name;
            System.out.println("Player changed to: " + currentPlayer);
        } else {
            System.out.println("Name cannot be empty.");
        }
    }
    
    private int getIntInput(String prompt, int min, int max) {
        while (true) {
            try {
                System.out.print(prompt);
                int value = Integer.parseInt(scanner.nextLine().trim());
                if (value >= min && value <= max) {
                    return value;
                }
                System.out.printf("Please enter a number between %d and %d.%n", min, max);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid number.");
            }
        }
    }
    
    public static void main(String[] args) {
        new QuizGame().start();
    }
}
