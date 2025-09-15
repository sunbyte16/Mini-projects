package com.todo.app.model;

import java.util.Objects;

/**
 * Represents a category for organizing tasks.
 */
public class Category {
    private String id;
    private String name;
    private String description;
    private String colorCode; // ANSI color code for console display

    public Category(String name) {
        this.id = generateId();
        this.name = name;
        this.description = "";
        this.colorCode = "\u001B[36m"; // Default to cyan
    }

    public Category(String name, String description, String colorCode) {
        this.id = generateId();
        this.name = name;
        this.description = description != null ? description : "";
        this.colorCode = colorCode != null ? colorCode : "\u001B[36m";
    }

    private String generateId() {
        return "CAT_" + System.currentTimeMillis() + "_" + (int)(Math.random() * 1000);
    }

    // Getters and Setters
    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getColorCode() {
        return colorCode;
    }

    public void setColorCode(String colorCode) {
        this.colorCode = colorCode;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Category category = (Category) o;
        return id.equals(category.id) || 
              (name != null && name.equalsIgnoreCase(category.name));
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name.toLowerCase());
    }

    @Override
    public String toString() {
        return colorCode + name + "\u001B[0m"; // Reset color after name
    }
    
    public String toFormattedString() {
        return String.format("""
            Category: %s
            ID: %s
            Description: %s""",
            this, id, description);
    }
}
