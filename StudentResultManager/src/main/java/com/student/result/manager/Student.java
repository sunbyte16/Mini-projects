package com.student.result.manager;

public class Student {
    private String rollNumber;
    private String name;
    private int[] marks;
    private int totalMarks;
    private double percentage;
    private String grade;
    private static final String[] SUBJECTS = {"Math", "Science", "English", "History", "Computer Science"};
    private static final int MAX_MARKS_PER_SUBJECT = 100;

    public Student(String rollNumber, String name, int[] marks) {
        this.rollNumber = rollNumber;
        this.name = name;
        this.marks = marks;
        calculateResult();
    }

    private void calculateResult() {
        // Calculate total marks
        this.totalMarks = 0;
        for (int mark : marks) {
            this.totalMarks += mark;
        }
        
        // Calculate percentage
        this.percentage = (double) totalMarks / (marks.length * MAX_MARKS_PER_SUBJECT) * 100;
        
        // Determine grade
        if (percentage >= 90) {
            this.grade = "A+";
        } else if (percentage >= 80) {
            this.grade = "A";
        } else if (percentage >= 70) {
            this.grade = "B";
        } else if (percentage >= 60) {
            this.grade = "C";
        } else if (percentage >= 50) {
            this.grade = "D";
        } else {
            this.grade = "F";
        }
    }

    // Getters
    public String getRollNumber() {
        return rollNumber;
    }

    public String getName() {
        return name;
    }

    public int[] getMarks() {
        return marks;
    }

    public int getTotalMarks() {
        return totalMarks;
    }

    public double getPercentage() {
        return percentage;
    }

    public String getGrade() {
        return grade;
    }

    public static String[] getSubjects() {
        return SUBJECTS;
    }

    public static int getMaxMarks() {
        return MAX_MARKS_PER_SUBJECT;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("\n--- Student Result ---\n");
        sb.append(String.format("Roll Number: %s%n", rollNumber));
        sb.append(String.format("Name: %s%n", name));
        sb.append("\nSubject-wise Marks:\n");
        for (int i = 0; i < SUBJECTS.length; i++) {
            sb.append(String.format("%-15s: %d/%d%n", 
                SUBJECTS[i], marks[i], MAX_MARKS_PER_SUBJECT));
        }
        sb.append("\n");
        sb.append(String.format("Total Marks  : %d/%d%n", 
            totalMarks, SUBJECTS.length * MAX_MARKS_PER_SUBJECT));
        sb.append(String.format("Percentage   : %.2f%%%n", percentage));
        sb.append(String.format("Grade        : %s%n", grade));
        sb.append("----------------------\n");
        return sb.toString();
    }
}
