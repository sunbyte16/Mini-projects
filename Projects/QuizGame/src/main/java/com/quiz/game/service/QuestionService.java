package com.quiz.game.service;

import com.quiz.game.model.Question;
import java.util.*;
import java.util.stream.Collectors;

public class QuestionService {
    private List<Question> questions;
    private Map<String, List<Question>> questionsByCategory;
    private Map<String, List<Question>> questionsByDifficulty;

    public QuestionService() {
        this.questions = new ArrayList<>();
        this.questionsByCategory = new HashMap<>();
        this.questionsByDifficulty = new HashMap<>();
        initializeSampleQuestions();
    }

    private void initializeSampleQuestions() {
        // Add sample questions for different categories and difficulties
        addQuestion(new Question("Q1", "General Knowledge", "EASY",
                "What is the capital of France?",
                Arrays.asList("London", "Berlin", "Paris", "Madrid"),
                2, "Paris is the capital of France.", 5));

        addQuestion(new Question("Q2", "Science", "MEDIUM",
                "What is the chemical symbol for water?",
                Arrays.asList("CO2", "H2O", "O2", "N2"),
                1, "H2O is the chemical formula for water.", 10));

        addQuestion(new Question("Q3", "History", "HARD",
                "In which year did World War II end?",
                Arrays.asList("1943", "1945", "1947", "1950"),
                1, "World War II ended in 1945.", 15));

        // Add more sample questions...
    }

    public void addQuestion(Question question) {
        questions.add(question);
        
        // Update category index
        questionsByCategory
            .computeIfAbsent(question.getCategory().toLowerCase(), k -> new ArrayList<>())
            .add(question);
            
        // Update difficulty index
        questionsByDifficulty
            .computeIfAbsent(question.getDifficulty().toLowerCase(), k -> new ArrayList<>())
            .add(question);
    }

    public List<Question> getQuestionsByCategory(String category) {
        return new ArrayList<>(questionsByCategory.getOrDefault(category.toLowerCase(), new ArrayList<>()));
    }

    public List<Question> getQuestionsByDifficulty(String difficulty) {
        return new ArrayList<>(questionsByDifficulty.getOrDefault(difficulty.toLowerCase(), new ArrayList<>()));
    }

    public List<Question> getQuestionsByCategoryAndDifficulty(String category, String difficulty) {
        return questions.stream()
            .filter(q -> q.getCategory().equalsIgnoreCase(category) && 
                        q.getDifficulty().equalsIgnoreCase(difficulty))
            .collect(Collectors.toList());
    }

    public List<String> getAllCategories() {
        return new ArrayList<>(questionsByCategory.keySet());
    }

    public List<String> getAllDifficulties() {
        return Arrays.asList("EASY", "MEDIUM", "HARD");
    }

    public List<Question> getRandomQuestions(int count) {
        if (count >= questions.size()) {
            return new ArrayList<>(questions);
        }
        
        List<Question> shuffled = new ArrayList<>(questions);
        Collections.shuffle(shuffled);
        return shuffled.subList(0, count);
    }

    public List<Question> getRandomQuestions(String category, String difficulty, int count) {
        List<Question> filtered = questions.stream()
            .filter(q -> (category == null || q.getCategory().equalsIgnoreCase(category)) &&
                        (difficulty == null || q.getDifficulty().equalsIgnoreCase(difficulty)))
            .collect(Collectors.toList());
            
        if (count >= filtered.size()) {
            return filtered;
        }
        
        Collections.shuffle(filtered);
        return filtered.subList(0, count);
    }
}
