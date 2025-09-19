package com.quiz.game.model;

import java.util.*;

public class Quiz {
    private String id;
    private String playerName;
    private List<Question> questions;
    private Map<String, Integer> answers; // questionId -> selectedOptionIndex
    private int currentQuestionIndex;
    private int score;
    private long startTime;
    private long timeLimit; // in seconds, 0 for no time limit
    private boolean isCompleted;

    public Quiz(String playerName, List<Question> questions, long timeLimit) {
        this.id = UUID.randomUUID().toString();
        this.playerName = playerName;
        this.questions = new ArrayList<>(questions);
        this.answers = new HashMap<>();
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.startTime = System.currentTimeMillis();
        this.timeLimit = timeLimit * 1000; // convert to milliseconds
        this.isCompleted = false;
    }

    // Getters
    public String getId() { return id; }
    public String getPlayerName() { return playerName; }
    public List<Question> getQuestions() { return new ArrayList<>(questions); }
    public int getCurrentQuestionIndex() { return currentQuestionIndex; }
    public int getScore() { return score; }
    public boolean isCompleted() { return isCompleted; }
    public int getTotalQuestions() { return questions.size(); }
    public int getAnsweredQuestions() { return answers.size(); }

    // Business methods
    public Question getCurrentQuestion() {
        if (isCompleted || currentQuestionIndex >= questions.size()) {
            return null;
        }
        return questions.get(currentQuestionIndex);
    }

    public boolean answerCurrentQuestion(int selectedOptionIndex) {
        if (isCompleted || currentQuestionIndex >= questions.size()) {
            return false;
        }

        Question currentQuestion = questions.get(currentQuestionIndex);
        answers.put(currentQuestion.getId(), selectedOptionIndex);

        if (currentQuestion.isCorrect(selectedOptionIndex)) {
            score += currentQuestion.getPoints();
        }

        // Move to next question or complete quiz
        if (++currentQuestionIndex >= questions.size()) {
            completeQuiz();
        }

        return true;
    }

    public void skipCurrentQuestion() {
        if (!isCompleted && currentQuestionIndex < questions.size()) {
            currentQuestionIndex++;
            if (currentQuestionIndex >= questions.size()) {
                completeQuiz();
            }
        }
    }

    public int getRemainingTime() {
        if (timeLimit <= 0) {
            return -1; // No time limit
        }
        
        long elapsed = (System.currentTimeMillis() - startTime) / 1000;
        return (int) Math.max(0, timeLimit / 1000 - elapsed);
    }

    public boolean isTimeUp() {
        return timeLimit > 0 && (System.currentTimeMillis() - startTime) >= timeLimit;
    }

    public void completeQuiz() {
        if (!isCompleted) {
            isCompleted = true;
            // Any cleanup or final calculations can go here
        }
    }

    public Map<String, Boolean> getResults() {
        Map<String, Boolean> results = new HashMap<>();
        for (Question q : questions) {
            Integer answer = answers.get(q.getId());
            results.put(q.getId(), answer != null && q.isCorrect(answer));
        }
        return results;
    }

    public int getCorrectAnswers() {
        return (int) getResults().values().stream().filter(Boolean::booleanValue).count();
    }

    public double getPercentageScore() {
        return questions.isEmpty() ? 0 : (getCorrectAnswers() * 100.0) / questions.size();
    }

    public String getSummary() {
        return String.format("""
            === QUIZ SUMMARY ===
            Player: %s
            Questions: %d/%d answered
            Correct Answers: %d
            Score: %d
            Accuracy: %.1f%%""",
            playerName, getAnsweredQuestions(), getTotalQuestions(),
            getCorrectAnswers(), score, getPercentageScore());
    }
}
