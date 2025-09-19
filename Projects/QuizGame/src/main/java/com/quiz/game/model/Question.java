package com.quiz.game.model;

import java.util.List;
import java.util.Objects;

public class Question {
    private String id;
    private String category;
    private String difficulty; // EASY, MEDIUM, HARD
    private String questionText;
    private List<String> options;
    private int correctOptionIndex;
    private String explanation;
    private int points;

    public Question(String id, String category, String difficulty, String questionText, 
                   List<String> options, int correctOptionIndex, String explanation, int points) {
        this.id = id;
        this.category = category;
        this.difficulty = difficulty.toUpperCase();
        this.questionText = questionText;
        this.options = options;
        this.correctOptionIndex = correctOptionIndex;
        this.explanation = explanation;
        this.points = points;
    }

    // Getters
    public String getId() { return id; }
    public String getCategory() { return category; }
    public String getDifficulty() { return difficulty; }
    public String getQuestionText() { return questionText; }
    public List<String> getOptions() { return options; }
    public int getCorrectOptionIndex() { return correctOptionIndex; }
    public String getExplanation() { return explanation; }
    public int getPoints() { return points; }

    // Business methods
    public boolean isCorrect(int selectedOption) {
        return selectedOption == correctOptionIndex;
    }

    public String getFormattedQuestion() {
        StringBuilder sb = new StringBuilder();
        sb.append("\n").append(questionText).append("\n");
        for (int i = 0; i < options.size(); i++) {
            sb.append(String.format("%d. %s%n", i + 1, options.get(i)));
        }
        return sb.toString();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Question question = (Question) o;
        return id.equals(question.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return String.format("""
            [%s] %s
            Category: %s | Difficulty: %s | Points: %d
            Options: %s
            Correct Answer: %d. %s
            Explanation: %s""",
            id, questionText, category, difficulty, points,
            options, correctOptionIndex + 1, options.get(correctOptionIndex),
            explanation);
    }
}
