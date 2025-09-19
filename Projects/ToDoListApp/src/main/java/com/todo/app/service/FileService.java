package com.todo.app.service;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.todo.app.model.Category;
import com.todo.app.model.Task;

import java.io.*;
import java.lang.reflect.Type;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Handles file operations for saving and loading application data.
 */
public class FileService {
    private static final String DATA_DIR = "data";
    private static final String TASKS_FILE = "tasks.json";
    private static final String CATEGORIES_FILE = "categories.json";
    private static final Gson gson = new GsonBuilder()
            .setPrettyPrinting()
            .registerTypeAdapter(LocalDate.class, new LocalDateAdapter())
            .registerTypeAdapter(LocalDateTime.class, new LocalDateTimeAdapter())
            .create();

    static {
        // Create data directory if it doesn't exist
        try {
            Files.createDirectories(Paths.get(DATA_DIR));
        } catch (IOException e) {
            System.err.println("Failed to create data directory: " + e.getMessage());
        }
    }

    /**
     * Saves tasks to a JSON file.
     *
     * @param tasks List of tasks to save
     * @return true if successful, false otherwise
     */
    public boolean saveTasks(List<Task> tasks) {
        try (Writer writer = new FileWriter(getFilePath(TASKS_FILE))) {
            gson.toJson(tasks, writer);
            return true;
        } catch (IOException e) {
            System.err.println("Error saving tasks: " + e.getMessage());
            return false;
        }
    }

    /**
     * Loads tasks from a JSON file.
     *
     * @return List of loaded tasks, or empty list if none found or error occurred
     */
    public List<Task> loadTasks() {
        Path filePath = getFilePath(TASKS_FILE);
        if (!Files.exists(filePath)) {
            return new ArrayList<>();
        }

        try (Reader reader = new FileReader(filePath.toFile())) {
            Type taskListType = new TypeToken<ArrayList<Task>>() {}.getType();
            return gson.fromJson(reader, taskListType);
        } catch (IOException e) {
            System.err.println("Error loading tasks: " + e.getMessage());
            return new ArrayList<>();
        }
    }

    /**
     * Saves categories to a JSON file.
     *
     * @param categories Map of categories to save
     * @return true if successful, false otherwise
     */
    public boolean saveCategories(Map<String, Category> categories) {
        try (Writer writer = new FileWriter(getFilePath(CATEGORIES_FILE))) {
            gson.toJson(categories.values(), writer);
            return true;
        } catch (IOException e) {
            System.err.println("Error saving categories: " + e.getMessage());
            return false;
        }
    }

    /**
     * Loads categories from a JSON file.
     *
     * @return Map of loaded categories, or empty map if none found or error occurred
     */
    public Map<String, Category> loadCategories() {
        Path filePath = getFilePath(CATEGORIES_FILE);
        if (!Files.exists(filePath)) {
            return Map.of();
        }

        try (Reader reader = new FileReader(filePath.toFile())) {
            Type categoryListType = new TypeToken<ArrayList<Category>>() {}.getType();
            List<Category> categoryList = gson.fromJson(reader, categoryListType);
            
            Map<String, Category> categories = new java.util.HashMap<>();
            if (categoryList != null) {
                for (Category category : categoryList) {
                    categories.put(category.getName().toLowerCase(), category);
                }
            }
            return categories;
        } catch (IOException e) {
            System.err.println("Error loading categories: " + e.getMessage());
            return Map.of();
        }
    }

    /**
     * Exports tasks to a text file in a human-readable format.
     *
     * @param tasks List of tasks to export
     * @param filePath Path to the output file
     * @return true if successful, false otherwise
     */
    public boolean exportToTextFile(List<Task> tasks, String filePath) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath))) {
            writer.println("=== TO-DO LIST EXPORT ===");
            writer.println("Generated on: " + LocalDateTime.now());
            writer.println("Total tasks: " + tasks.size());
            writer.println("\n" + "=".repeat(50) + "\n");

            for (int i = 0; i < tasks.size(); i++) {
                Task task = tasks.get(i);
                writer.printf("%d. [%s] %s%n", i + 1, 
                    task.isCompleted() ? "X" : " ", 
                    task.getTitle());
                
                if (!task.getDescription().isEmpty()) {
                    writer.println("   Description: " + task.getDescription());
                }
                
                if (task.getDueDate() != null) {
                    writer.println("   Due: " + task.getDueDate());
                }
                
                writer.println("   Priority: " + task.getPriority().getDisplayName());
                
                if (task.getCategory() != null) {
                    writer.println("   Category: " + task.getCategory().getName());
                }
                
                writer.println();
            }
            
            return true;
        } catch (IOException e) {
            System.err.println("Error exporting tasks: " + e.getMessage());
            return false;
        }
    }

    /**
     * Imports tasks from a CSV file.
     *
     * @param filePath Path to the CSV file
     * @return List of imported tasks, or empty list if error occurred
     */
    public List<Task> importFromCsv(String filePath) {
        List<Task> importedTasks = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            boolean firstLine = true;
            
            while ((line = reader.readLine()) != null) {
                if (firstLine) {
                    firstLine = false;
                    continue; // Skip header
                }
                
                String[] parts = line.split(",", -1); // -1 to keep trailing empty strings
                if (parts.length >= 3) {
                    String title = parts[0].trim();
                    String description = parts[1].trim();
                    String dueDateStr = parts[2].trim();
                    
                    Task task = new Task(title, description, null, Priority.MEDIUM, null);
                    
                    if (!dueDateStr.isEmpty()) {
                        try {
                            task.setDueDate(LocalDate.parse(dueDateStr));
                        } catch (Exception e) {
                            System.err.println("Invalid date format in CSV: " + dueDateStr);
                        }
                    }
                    
                    if (parts.length > 3 && !parts[3].trim().isEmpty()) {
                        try {
                            task.setPriority(Priority.valueOf(parts[3].trim().toUpperCase()));
                        } catch (IllegalArgumentException e) {
                            System.err.println("Invalid priority in CSV: " + parts[3]);
                        }
                    }
                    
                    importedTasks.add(task);
                }
            }
            
            return importedTasks;
        } catch (IOException e) {
            System.err.println("Error importing tasks from CSV: " + e.getMessage());
            return List.of();
        }
    }

    private Path getFilePath(String filename) {
        return Paths.get(DATA_DIR, filename);
    }
}
