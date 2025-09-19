package com.quiz.game.model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Score implements Comparable<Score> {
    private String playerName;
    private int score;
    private int totalQuestions;
    private int correctAnswers;
    private String category;
    private String difficulty;
    private LocalDateTime dateTime;
    private long timeTaken; // in seconds

    public Score(String playerName, int score, int totalQuestions, int correctAnswers, 
                String category, String difficulty, long timeTaken) {
        this.playerName = playerName;
        this.score = score;
        this.totalQuestions = totalQuestions;
        this.correctAnswers = correctAnswers;
        this.category = category;
        this.difficulty = difficulty.toUpperCase();
        this.dateTime = LocalDateTime.now();
        this.timeTaken = timeTaken;
    }

    // Getters
    public String getPlayerName() { return playerName; }
    public int getScore() { return score; }
    public int getTotalQuestions() { return totalQuestions; }
    public int getCorrectAnswers() { return correctAnswers; }
    public String getCategory() { return category; }
    public String getDifficulty() { return difficulty; }
    public LocalDateTime getDateTime() { return dateTime; }
    public long getTimeTaken() { return timeTaken; }

    // Derived properties
    public double getAccuracy() {
        return totalQuestions > 0 ? (correctAnswers * 100.0) / totalQuestions : 0;
    }

    public String getFormattedDateTime() {
        return dateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
    }

    public String getFormattedTimeTaken() {
        long hours = timeTaken / 3600;
        long minutes = (timeTaken % 3600) / 60;
        long seconds = timeTaken % 60;
        
        if (hours > 0) {
            return String.format("%d:%02d:%02d", hours, minutes, seconds);
        } else {
            return String.format("%d:%02d", minutes, seconds);
        }
    }

    @Override
    public int compareTo(Score other) {
        // Higher scores come first, then by time taken (faster is better)
        if (this.score != other.score) {
            return Integer.compare(other.score, this.score);
        }
        return Long.compare(this.timeTaken, other.timeTaken);
    }

    @Override
    public String toString() {
        return String.format("""
            Player: %s
            Score: %d/%d (%.1f%%)
            Category: %s | Difficulty: %s
            Time Taken: %s
            Date: %s""",
            playerName, score, totalQuestions * 10, getAccuracy(),
            category, difficulty, getFormattedTimeTaken(), getFormattedDateTime());
    }
    
    public String toCsv() {
        return String.format("%s,%d,%d,%d,%s,%s,%d,%s",
            playerName, score, totalQuestions, correctAnswers,
            category, difficulty, timeTaken, getFormattedDateTime());
    }
    
    public static String getCsvHeader() {
        return "Player,Score,Total Questions,Correct Answers,Category,Difficulty,Time Taken,Date";
    }
    
    public static Score fromCsv(String csvLine) {
        try {
            String[] parts = csvLine.split(",");
            if (parts.length < 8) return null;
            
            String playerName = parts[0];
            int score = Integer.parseInt(parts[1]);
            int totalQuestions = Integer.parseInt(parts[2]);
            int correctAnswers = Integer.parseInt(parts[3]);
            String category = parts[4];
            String difficulty = parts[5];
            long timeTaken = Long.parseLong(parts[6]);
            
            Score s = new Score(playerName, score, totalQuestions, correctAnswers, 
                              category, difficulty, timeTaken);
            // Parse the date back if needed
            return s;
        } catch (Exception e) {
            return null;
        }
    }
}
