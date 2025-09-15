package com.todo.app.service;

import com.todo.app.model.Category;
import com.todo.app.model.Priority;
import com.todo.app.model.Task;

import java.time.LocalDate;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/**
 * Service class for managing tasks in the To-Do List application.
 */
public class TaskService {
    private final Map<String, Task> tasks;
    private final Map<String, Category> categories;

    public TaskService() {
        this.tasks = new HashMap<>();
        this.categories = new HashMap<>();
        initializeDefaultCategories();
    }

    private void initializeDefaultCategories() {
        // Add some default categories
        addCategory(new Category("Personal", "Personal tasks", "\u001B[36m"));
        addCategory(new Category("Work", "Work-related tasks", "\u001B[35m"));
        addCategory(new Category("Shopping", "Shopping list items", "\u001B[33m"));
        addCategory(new Category("Health", "Health and fitness", "\u001B[32m"));
    }

    // Category Management
    public void addCategory(Category category) {
        if (category != null) {
            categories.putIfAbsent(category.getName().toLowerCase(), category);
        }
    }

    public List<Category> getAllCategories() {
        return new ArrayList<>(categories.values());
    }

    public Category getCategoryByName(String name) {
        return name != null ? categories.get(name.toLowerCase()) : null;
    }

    // Task CRUD Operations
    public void addTask(Task task) {
        if (task != null) {
            tasks.put(task.getId(), task);
        }
    }

    public Optional<Task> getTask(String id) {
        return Optional.ofNullable(tasks.get(id));
    }

    public List<Task> getAllTasks() {
        return new ArrayList<>(tasks.values());
    }

    public boolean updateTask(String id, Task updatedTask) {
        if (tasks.containsKey(id)) {
            tasks.put(id, updatedTask);
            return true;
        }
        return false;
    }

    public boolean deleteTask(String id) {
        return tasks.remove(id) != null;
    }

    // Task Query Methods
    public List<Task> getTasksByCompletion(boolean completed) {
        return tasks.values().stream()
            .filter(task -> task.isCompleted() == completed)
            .sorted()
            .collect(Collectors.toList());
    }

    public List<Task> getTasksByPriority(Priority priority) {
        return tasks.values().stream()
            .filter(task -> task.getPriority() == priority)
            .sorted()
            .collect(Collectors.toList());
    }

    public List<Task> getTasksByCategory(String categoryName) {
        return tasks.values().stream()
            .filter(task -> task.getCategory() != null && 
                           task.getCategory().getName().equalsIgnoreCase(categoryName))
            .sorted()
            .collect(Collectors.toList());
    }

    public List<Task> getOverdueTasks() {
        LocalDate today = LocalDate.now();
        return tasks.values().stream()
            .filter(task -> !task.isCompleted() && 
                           task.getDueDate() != null && 
                           task.getDueDate().isBefore(today))
            .sorted()
            .collect(Collectors.toList());
    }

    public List<Task> getTasksDueToday() {
        LocalDate today = LocalDate.now();
        return tasks.values().stream()
            .filter(task -> !task.isCompleted() && 
                           task.getDueDate() != null && 
                           task.getDueDate().isEqual(today))
            .sorted()
            .collect(Collectors.toList());
    }

    public List<Task> searchTasks(String query) {
        String searchQuery = query.toLowerCase();
        return tasks.values().stream()
            .filter(task -> task.getTitle().toLowerCase().contains(searchQuery) ||
                           task.getDescription().toLowerCase().contains(searchQuery))
            .sorted()
            .collect(Collectors.toList());
    }

    public List<Task> filterTasks(Predicate<Task> filter) {
        return tasks.values().stream()
            .filter(filter)
            .sorted()
            .collect(Collectors.toList());
    }

    // Task Operations
    public boolean toggleTaskCompletion(String taskId) {
        return getTask(taskId)
            .map(task -> {
                task.setCompleted(!task.isCompleted());
                return true;
            })
            .orElse(false);
    }

    public boolean updateTaskPriority(String taskId, Priority priority) {
        return getTask(taskId)
            .map(task -> {
                task.setPriority(priority);
                return true;
            })
            .orElse(false);
    }

    // Statistics
    public Map<String, Object> getTaskStatistics() {
        long totalTasks = tasks.size();
        long completedTasks = tasks.values().stream().filter(Task::isCompleted).count();
        long pendingTasks = totalTasks - completedTasks;
        long overdueTasks = getOverdueTasks().size();
        
        Map<Priority, Long> tasksByPriority = tasks.values().stream()
            .collect(Collectors.groupingBy(Task::getPriority, Collectors.counting()));
        
        Map<Category, Long> tasksByCategory = tasks.values().stream()
            .filter(task -> task.getCategory() != null)
            .collect(Collectors.groupingBy(Task::getCategory, Collectors.counting()));
        
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalTasks", totalTasks);
        stats.put("completedTasks", completedTasks);
        stats.put("pendingTasks", pendingTasks);
        stats.put("overdueTasks", overdueTasks);
        stats.put("completionRate", totalTasks > 0 ? (completedTasks * 100.0) / totalTasks : 0);
        stats.put("tasksByPriority", tasksByPriority);
        stats.put("tasksByCategory", tasksByCategory);
        
        return stats;
    }

    // Data Management
    public void clearAllTasks() {
        tasks.clear();
    }

    public void addSampleTasks() {
        // Add some sample tasks for demonstration
        Category personal = getCategoryByName("Personal");
        Category work = getCategoryByName("Work");
        
        addTask(new Task("Buy groceries", "Milk, eggs, bread", 
            LocalDate.now().plusDays(1), Priority.HIGH, personal));
            
        addTask(new Task("Finish project", "Complete the project documentation", 
            LocalDate.now().plusDays(3), Priority.HIGH, work));
            
        addTask(new Task("Call mom", "Wish her happy birthday", 
            LocalDate.now().minusDays(1), Priority.MEDIUM, personal));
            
        addTask(new Task("Schedule meeting", "With the development team", 
            LocalDate.now().plusDays(2), Priority.MEDIUM, work));
            
        addTask(new Task("Read book", "Chapter 5-6", 
            null, Priority.LOW, personal));
    }
}
