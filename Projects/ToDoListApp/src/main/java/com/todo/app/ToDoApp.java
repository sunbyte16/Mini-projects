package com.todo.app;

import com.todo.app.model.Category;
import com.todo.app.model.Priority;
import com.todo.app.model.Task;
import com.todo.app.service.FileService;
import com.todo.app.service.TaskService;

import java.io.File;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Scanner;
import java.util.function.Predicate;

/**
 * Main application class for the To-Do List application.
 */
public class ToDoApp {
    private final TaskService taskService;
    private final FileService fileService;
    private final Scanner scanner;
    private boolean running;

    public ToDoApp() {
        this.taskService = new TaskService();
        this.fileService = new FileService();
        this.scanner = new Scanner(System.in);
        this.running = true;
    }

    public void start() {
        loadData();
        displayWelcome();
        
        while (running) {
            displayMainMenu();
            int choice = getIntInput("Enter your choice (1-9): ", 1, 9);
            handleMainMenuChoice(choice);
        }
        
        saveData();
        System.out.println("\nThank you for using the To-Do List App. Goodbye!");
        scanner.close();
    }

    private void loadData() {
        System.out.println("Loading data...");
        // Load tasks and categories from files here if needed
        System.out.println("Data loaded successfully!\n");
    }

    private void saveData() {
        System.out.println("\nSaving data...");
        // Save tasks and categories to files here
        System.out.println("Data saved successfully!");
    }

    private void displayWelcome() {
        System.out.println("""
            ===================================
                WELCOME TO TO-DO LIST APP
            ===================================
            Manage your tasks efficiently with this simple console application.
            """);
    }

    private void displayMainMenu() {
        System.out.println("\n=== MAIN MENU ===");
        System.out.println("1. View All Tasks");
        System.out.println("2. Add New Task");
        System.out.println("3. Edit Task");
        System.out.println("4. Delete Task");
        System.out.println("5. View Tasks by Status");
        System.out.println("6. View Tasks by Category");
        System.out.println("7. View Tasks by Priority");
        System.out.println("8. View Statistics");
        System.out.println("9. Exit");
    }

    private void handleMainMenuChoice(int choice) {
        switch (choice) {
            case 1 -> viewAllTasks();
            case 2 -> addNewTask();
            case 3 -> editTask();
            case 4 -> deleteTask();
            case 5 -> viewTasksByStatus();
            case 6 -> viewTasksByCategory();
            case 7 -> viewTasksByPriority();
            case 8 -> showStatistics();
            case 9 -> running = false;
            default -> System.out.println("Invalid choice. Please try again.");
        }
    }

    private void viewAllTasks() {
        List<Task> tasks = taskService.getAllTasks();
        displayTasks("ALL TASKS", tasks);
    }

    private void addNewTask() {
        System.out.println("\n=== ADD NEW TASK ===");
        
        String title = getStringInput("Enter task title: ", false);
        String description = getStringInput("Enter task description (optional): ", true);
        
        LocalDate dueDate = null;
        if (getYesNoInput("Add due date? (y/n): ")) {
            dueDate = getDateInput("Enter due date (YYYY-MM-DD): ");
        }
        
        Priority priority = selectPriority();
        Category category = selectCategory(true);
        
        Task task = new Task(title, description, dueDate, priority, category);
        taskService.addTask(task);
        
        System.out.println("\n✅ Task added successfully!");
        displayTaskDetails(task);
    }

    private void editTask() {
        List<Task> tasks = taskService.getAllTasks();
        if (tasks.isEmpty()) {
            System.out.println("No tasks available to edit.");
            return;
        }
        
        displayTasks("SELECT TASK TO EDIT", tasks);
        int taskIndex = getIntInput("Enter task number to edit (0 to cancel): ", 0, tasks.size()) - 1;
        
        if (taskIndex == -1) {
            return; // User cancelled
        }
        
        Task task = tasks.get(taskIndex);
        boolean continueEditing = true;
        
        while (continueEditing) {
            System.out.println("\n=== EDIT TASK ===");
            displayTaskDetails(task);
            
            System.out.println("\nWhat would you like to edit?");
            System.out.println("1. Title");
            System.out.println("2. Description");
            System.out.println("3. Due Date");
            System.out.println("4. Priority");
            System.out.println("5. Category");
            System.out.println("6. Toggle Completion Status");
            System.out.println("7. Save Changes");
            System.out.println("8. Cancel");
            
            int choice = getIntInput("Enter your choice (1-8): ", 1, 8);
            
            switch (choice) {
                case 1 -> task.setTitle(getStringInput("Enter new title: ", false));
                case 2 -> task.setDescription(getStringInput("Enter new description: ", true));
                case 3 -> {
                    if (getYesNoInput("Remove due date? (y/n): ")) {
                        task.setDueDate(null);
                    } else {
                        task.setDueDate(getDateInput("Enter new due date (YYYY-MM-DD): "));
                    }
                }
                case 4 -> task.setPriority(selectPriority());
                case 5 -> task.setCategory(selectCategory(true));
                case 6 -> task.setCompleted(!task.isCompleted());
                case 7 -> {
                    taskService.updateTask(task.getId(), task);
                    System.out.println("\n✅ Task updated successfully!");
                    continueEditing = false;
                }
                case 8 -> {
                    System.out.println("Edit cancelled. Changes not saved.");
                    continueEditing = false;
                }
            }
        }
    }

    private void deleteTask() {
        List<Task> tasks = taskService.getAllTasks();
        if (tasks.isEmpty()) {
            System.out.println("No tasks available to delete.");
            return;
        }
        
        displayTasks("SELECT TASK TO DELETE", tasks);
        int taskIndex = getIntInput("Enter task number to delete (0 to cancel): ", 0, tasks.size()) - 1;
        
        if (taskIndex == -1) {
            return; // User cancelled
        }
        
        Task task = tasks.get(taskIndex);
        System.out.println("\nYou are about to delete this task:");
        displayTaskDetails(task);
        
        if (getYesNoInput("\nAre you sure you want to delete this task? (y/n): ")) {
            if (taskService.deleteTask(task.getId())) {
                System.out.println("\n✅ Task deleted successfully!");
            } else {
                System.out.println("\n❌ Failed to delete task.");
            }
        } else {
            System.out.println("\nDeletion cancelled.");
        }
    }

    private void viewTasksByStatus() {
        System.out.println("\n=== VIEW TASKS BY STATUS ===");
        System.out.println("1. All Tasks");
        System.out.println("2. Active Tasks");
        System.out.println("3. Completed Tasks");
        System.out.println("4. Overdue Tasks");
        
        int choice = getIntInput("Enter your choice (1-4): ", 1, 4);
        
        List<Task> tasks;
        String title;
        
        switch (choice) {
            case 1 -> {
                tasks = taskService.getAllTasks();
                title = "ALL TASKS";
            }
            case 2 -> {
                tasks = taskService.getTasksByCompletion(false);
                title = "ACTIVE TASKS";
            }
            case 3 -> {
                tasks = taskService.getTasksByCompletion(true);
                title = "COMPLETED TASKS";
            }
            case 4 -> {
                tasks = taskService.getOverdueTasks();
                title = "OVERDUE TASKS";
            }
            default -> {
                System.out.println("Invalid choice. Showing all tasks.");
                tasks = taskService.getAllTasks();
                title = "ALL TASKS";
            }
        }
        
        displayTasks(title, tasks);
    }

    private void viewTasksByCategory() {
        List<Category> categories = taskService.getAllCategories();
        if (categories.isEmpty()) {
            System.out.println("No categories available.");
            return;
        }
        
        System.out.println("\n=== SELECT CATEGORY ===");
        for (int i = 0; i < categories.size(); i++) {
            System.out.printf("%d. %s%n", i + 1, categories.get(i));
        }
        
        int choice = getIntInput("Enter category number (0 to cancel): ", 0, categories.size());
        if (choice == 0) {
            return; // User cancelled
        }
        
        Category selectedCategory = categories.get(choice - 1);
        List<Task> tasks = taskService.getTasksByCategory(selectedCategory.getName());
        
        displayTasks("TASKS IN CATEGORY: " + selectedCategory.getName().toUpperCase(), tasks);
    }

    private void viewTasksByPriority() {
        System.out.println("\n=== SELECT PRIORITY ===");
        System.out.println("1. High Priority");
        System.out.println("2. Medium Priority");
        System.out.println("3. Low Priority");
        
        int choice = getIntInput("Enter priority level (1-3, 0 to cancel): ", 0, 3);
        if (choice == 0) {
            return; // User cancelled
        }
        
        Priority priority = Priority.values()[choice - 1];
        List<Task> tasks = taskService.getTasksByPriority(priority);
        
        displayTasks("TASKS WITH PRIORITY: " + priority.getDisplayName().toUpperCase(), tasks);
    }

    private void showStatistics() {
        var stats = taskService.getTaskStatistics();
        
        System.out.println("\n=== TASK STATISTICS ===");
        System.out.printf("Total Tasks: %d%n", stats.get("totalTasks"));
        System.out.printf("Completed Tasks: %d%n", stats.get("completedTasks"));
        System.out.printf("Pending Tasks: %d%n", stats.get("pendingTasks"));
        System.out.printf("Overdue Tasks: %d%n", stats.get("overdueTasks"));
        System.out.printf("Completion Rate: %.1f%%%n", stats.get("completionRate"));
        
        @SuppressWarnings("unchecked")
        var tasksByPriority = (java.util.Map<Priority, Long>) stats.get("tasksByPriority");
        System.out.println("\nTasks by Priority:");
        tasksByPriority.forEach((priority, count) -> 
            System.out.printf("- %s: %d%n", priority.getDisplayName(), count));
        
        @SuppressWarnings("unchecked")
        var tasksByCategory = (java.util.Map<Category, Long>) stats.get("tasksByCategory");
        if (!tasksByCategory.isEmpty()) {
            System.out.println("\nTasks by Category:");
            tasksByCategory.forEach((category, count) -> 
                System.out.printf("- %s: %d%n", category.getName(), count));
        }
    }

    // Helper methods for input handling
    private String getStringInput(String prompt, boolean optional) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();
            
            if (!input.isEmpty() || optional) {
                return input;
            }
            System.out.println("This field is required. Please try again.");
        }
    }

    private int getIntInput(String prompt, int min, int max) {
        while (true) {
            try {
                System.out.print(prompt);
                String input = scanner.nextLine().trim();
                
                if (input.isEmpty()) {
                    System.out.printf("Please enter a number between %d and %d.%n", min, max);
                    continue;
                }
                
                int value = Integer.parseInt(input);
                if (value >= min && value <= max) {
                    return value;
                }
                
                System.out.printf("Please enter a number between %d and %d.%n", min, max);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid number.");
            }
        }
    }

    private boolean getYesNoInput(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim().toLowerCase();
            
            if (input.equals("y") || input.equals("yes")) {
                return true;
            } else if (input.equals("n") || input.equals("no")) {
                return false;
            }
            
            System.out.println("Please enter 'y' for yes or 'n' for no.");
        }
    }

    private LocalDate getDateInput(String prompt) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        
        while (true) {
            try {
                System.out.print(prompt);
                String input = scanner.nextLine().trim();
                
                if (input.isEmpty()) {
                    return null;
                }
                
                return LocalDate.parse(input, formatter);
            } catch (DateTimeParseException e) {
                System.out.println("Invalid date format. Please use YYYY-MM-DD format.");
            }
        }
    }

    private Priority selectPriority() {
        System.out.println("\nSelect priority:");
        for (Priority p : Priority.values()) {
            System.out.printf("%d. %s%n", p.getValue(), p);
        }
        
        int choice = getIntInput("Enter priority (1-3): ", 1, 3);
        return Priority.fromValue(choice);
    }

    private Category selectCategory(boolean includeNone) {
        List<Category> categories = taskService.getAllCategories();
        
        if (categories.isEmpty()) {
            return null;
        }
        
        System.out.println("\nSelect category:");
        int startIndex = 1;
        
        if (includeNone) {
            System.out.println("0. No category");
            startIndex = 1;
        }
        
        for (int i = 0; i < categories.size(); i++) {
            System.out.printf("%d. %s%n", i + startIndex, categories.get(i));
        }
        
        int maxChoice = includeNone ? categories.size() : categories.size() - 1;
        int choice = getIntInput(
            String.format("Enter category number (%s-%d): ", 
                includeNone ? "0" : "1", 
                includeNone ? categories.size() : categories.size() - 1),
            includeNone ? 0 : 1,
            includeNone ? categories.size() : categories.size() - 1
        );
        
        if (includeNone && choice == 0) {
            return null;
        }
        
        return categories.get(choice - startIndex);
    }

    // Helper methods for displaying data
    private void displayTasks(String title, List<Task> tasks) {
        System.out.printf("\n=== %s (%d) ===%n", title, tasks.size());
        
        if (tasks.isEmpty()) {
            System.out.println("No tasks found.");
            return;
        }
        
        System.out.printf("%-4s %-40s %-12s %-10s %-15s %s%n", 
            "#", "TITLE", "DUE DATE", "PRIORITY", "CATEGORY", "STATUS");
        System.out.println("-".repeat(100));
        
        for (int i = 0; i < tasks.size(); i++) {
            Task task = tasks.get(i);
            String dueDate = task.getDueDate() != null ? 
                task.getDueDate().format(DateTimeFormatter.ISO_LOCAL_DATE) : "-";
            
            System.out.printf("%-4d %-40s %-12s %-10s %-15s %s%n",
                i + 1,
                truncate(task.getTitle(), 38),
                dueDate,
                task.getPriority(),
                task.getCategory() != null ? 
                    truncate(task.getCategory().getName(), 13) : "-",
                task.getStatus());
        }
    }

    private void displayTaskDetails(Task task) {
        System.out.println("\n=== TASK DETAILS ===");
        System.out.println("Title:       " + task.getTitle());
        System.out.println("Description: " + 
            (task.getDescription().isEmpty() ? "No description" : task.getDescription()));
        System.out.println("Due Date:    " + 
            (task.getDueDate() != null ? 
                task.getDueDate().format(DateTimeFormatter.ISO_LOCAL_DATE) : "No due date"));
        System.out.println("Priority:    " + task.getPriority());
        System.out.println("Category:    " + 
            (task.getCategory() != null ? task.getCategory() : "No category"));
        System.out.println("Status:      " + task.getStatus());
        System.out.println("Created:     " + 
            task.getCreatedAt().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        System.out.println("Last Updated: " + 
            task.getUpdatedAt().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        if (task.isCompleted() && task.getCompletedAt() != null) {
            System.out.println("Completed:   " + 
                task.getCompletedAt().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        }
    }

    private String truncate(String text, int maxLength) {
        if (text == null) {
            return "";
        }
        return text.length() <= maxLength ? text : text.substring(0, maxLength - 3) + "...";
    }

    // Main method
    public static void main(String[] args) {
        new ToDoApp().start();
    }
}
