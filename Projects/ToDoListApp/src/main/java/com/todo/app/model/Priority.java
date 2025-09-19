package com.todo.app.model;

/**
 * Represents the priority level of a task.
 */
public enum Priority {
    HIGH("High", 1, "[31m"),    // Red
    MEDIUM("Medium", 2, "[33m"),  // Yellow
    LOW("Low", 3, "[32m");      // Green

    private final String displayName;
    private final int value;
    private final String colorCode;

    Priority(String displayName, int value, String colorCode) {
        this.displayName = displayName;
        this.value = value;
        this.colorCode = colorCode;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getValue() {
        return value;
    }

    public String getColorCode() {
        return colorCode;
    }

    public static Priority fromValue(int value) {
        for (Priority priority : Priority.values()) {
            if (priority.value == value) {
                return priority;
            }
        }
        return Priority.MEDIUM; // Default to MEDIUM if invalid value
    }

    @Override
    public String toString() {
        return colorCode + displayName + "[0m"; // Reset color after display name
    }
}
