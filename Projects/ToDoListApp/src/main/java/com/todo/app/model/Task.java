package com.todo.app.model;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Objects;
import java.util.UUID;

/**
 * Represents a task in the To-Do List application.
 */
public class Task implements Comparable<Task> {
    private String id;
    private String title;
    private String description;
    private LocalDate dueDate;
    private Priority priority;
    private Category category;
    private boolean completed;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime completedAt;

    public Task(String title) {
        this.id = UUID.randomUUID().toString();
        this.title = title;
        this.description = "";
        this.dueDate = null;
        this.priority = Priority.MEDIUM;
        this.category = null;
        this.completed = false;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = this.createdAt;
        this.completedAt = null;
    }

    public Task(String title, String description, LocalDate dueDate, 
               Priority priority, Category category) {
        this(title);
        this.description = description != null ? description : "";
        this.dueDate = dueDate;
        this.priority = priority != null ? priority : Priority.MEDIUM;
        this.category = category;
    }

    // Getters and Setters
    public String getId() { return id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { 
        this.title = title; 
        this.updatedAt = LocalDateTime.now();
    }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { 
        this.description = description;
        this.updatedAt = LocalDateTime.now();
    }
    
    public LocalDate getDueDate() { return dueDate; }
    public void setDueDate(LocalDate dueDate) { 
        this.dueDate = dueDate;
        this.updatedAt = LocalDateTime.now();
    }
    
    public Priority getPriority() { return priority; }
    public void setPriority(Priority priority) { 
        this.priority = priority != null ? priority : Priority.MEDIUM;
        this.updatedAt = LocalDateTime.now();
    }
    
    public Category getCategory() { return category; }
    public void setCategory(Category category) { 
        this.category = category;
        this.updatedAt = LocalDateTime.now();
    }
    
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) {
        this.completed = completed;
        this.updatedAt = LocalDateTime.now();
        this.completedAt = completed ? LocalDateTime.now() : null;
    }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public LocalDateTime getCompletedAt() { return completedAt; }

    // Business methods
    public boolean isOverdue() {
        return !completed && dueDate != null && dueDate.isBefore(LocalDate.now());
    }

    public String getStatus() {
        if (completed) {
            return "\u001B[32mCompleted\u001B[0m"; // Green
        } else if (isOverdue()) {
            return "\u001B[31mOverdue\u001B[0m"; // Red
        } else {
            return "\u001B[33mPending\u001B[0m"; // Yellow
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Task task = (Task) o;
        return id.equals(task.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public int compareTo(Task other) {
        // Sort by: 1. Completion status (incomplete first), 2. Due date (earlier first), 3. Priority (high first)
        if (this.completed != other.completed) {
            return Boolean.compare(this.completed, other.completed);
        }
        
        if (this.dueDate != null && other.dueDate != null) {
            int dateCompare = this.dueDate.compareTo(other.dueDate);
            if (dateCompare != 0) return dateCompare;
        } else if (this.dueDate != null) {
            return -1; // Tasks with due dates come first
        } else if (other.dueDate != null) {
            return 1;
        }
        
        return Integer.compare(this.priority.getValue(), other.priority.getValue());
    }

    @Override
    public String toString() {
        return String.format("""
            %s [%s] %s
            %s
            Due: %s | Priority: %s | Category: %s
            Created: %s | Last Updated: %s""",
            completed ? "[✓]" : "[ ]", 
            id.substring(0, 8), // Short ID for display
            title,
            description.isEmpty() ? "No description" : description,
            dueDate != null ? dueDate.format(DateTimeFormatter.ISO_LOCAL_DATE) : "No due date",
            priority,
            category != null ? category.getName() : "Uncategorized",
            formatDateTime(createdAt),
            formatDateTime(updatedAt)
        );
    }

    public String toShortString() {
        return String.format("%s %s [%s] %s - %s | Due: %s | %s",
            completed ? "[✓]" : "[ ]",
            priority,
            id.substring(0, 8),
            title,
            getStatus(),
            dueDate != null ? dueDate.format(DateTimeFormatter.ISO_LOCAL_DATE) : "No due date",
            category != null ? category.getName() : "Uncategorized"
        );
    }

    private String formatDateTime(LocalDateTime dateTime) {
        if (dateTime == null) return "N/A";
        return dateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
    }
}
