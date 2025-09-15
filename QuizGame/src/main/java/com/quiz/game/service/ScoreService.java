package com.quiz.game.service;

import com.quiz.game.model.Score;
import java.io.*;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

public class ScoreService {
    private static final String SCORES_FILE = "scores.csv";
    private List<Score> scores;

    public ScoreService() {
        this.scores = new ArrayList<>();
        loadScores();
    }

    public void addScore(Score score) {
        scores.add(score);
        saveScores();
    }

    public List<Score> getTopScores(int limit) {
        return scores.stream()
            .sorted()
            .limit(limit)
            .collect(Collectors.toList());
    }

    public List<Score> getTopScores(String category, String difficulty, int limit) {
        return scores.stream()
            .filter(score -> (category == null || score.getCategory().equalsIgnoreCase(category)) &&
                           (difficulty == null || score.getDifficulty().equalsIgnoreCase(difficulty)))
            .sorted()
            .limit(limit)
            .collect(Collectors.toList());
    }

    public List<Score> getPlayerScores(String playerName) {
        return scores.stream()
            .filter(score -> score.getPlayerName().equalsIgnoreCase(playerName))
            .sorted()
            .collect(Collectors.toList());
    }

    private void loadScores() {
        try {
            if (Files.exists(Paths.get(SCORES_FILE))) {
                List<String> lines = Files.readAllLines(Paths.get(SCORES_FILE));
                if (!lines.isEmpty() && lines.get(0).equals(Score.getCsvHeader())) {
                    lines.remove(0); // Skip header
                }
                
                scores = lines.stream()
                    .map(Score::fromCsv)
                    .filter(Objects::nonNull)
                    .collect(Collectors.toList());
            }
        } catch (IOException e) {
            System.err.println("Error loading scores: " + e.getMessage());
        }
    }

    private void saveScores() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(SCORES_FILE))) {
            writer.println(Score.getCsvHeader());
            scores.stream()
                .map(Score::toCsv)
                .forEach(writer::println);
        } catch (IOException e) {
            System.err.println("Error saving scores: " + e.getMessage());
        }
    }

    public void clearAllScores() {
        scores.clear();
        saveScores();
    }

    public int getPlayerRank(Score score) {
        List<Score> allScores = new ArrayList<>(scores);
        allScores.sort(Collections.reverseOrder());
        return allScores.indexOf(score) + 1;
    }

    public Map<String, Integer> getPlayerStats(String playerName) {
        List<Score> playerScores = getPlayerScores(playerName);
        if (playerScores.isEmpty()) {
            return Map.of(
                "gamesPlayed", 0,
                "totalScore", 0,
                "averageScore", 0,
                "bestScore", 0,
                "bestCategory", "N/A",
                "totalCorrect", 0,
                "totalQuestions", 0
            );
        }

        int totalScore = playerScores.stream().mapToInt(Score::getScore).sum();
        int bestScore = playerScores.stream().mapToInt(Score::getScore).max().orElse(0);
        int totalCorrect = playerScores.stream().mapToInt(Score::getCorrectAnswers).sum();
        int totalQuestions = playerScores.stream().mapToInt(Score::getTotalQuestions).sum();
        
        String bestCategory = playerScores.stream()
            .collect(Collectors.groupingBy(Score::getCategory, Collectors.summingInt(Score::getScore)))
            .entrySet().stream()
            .max(Map.Entry.comparingByValue())
            .map(Map.Entry::getKey)
            .orElse("N/A");

        return Map.of(
            "gamesPlayed", playerScores.size(),
            "totalScore", totalScore,
            "averageScore", totalScore / playerScores.size(),
            "bestScore", bestScore,
            "bestCategory", bestCategory,
            "totalCorrect", totalCorrect,
            "totalQuestions", totalQuestions,
            "accuracy", totalQuestions > 0 ? (totalCorrect * 100) / totalQuestions : 0
        );
    }
}
