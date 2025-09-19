package com.student.result.manager;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class StudentResultManager {
    private static List<Student> students = new ArrayList<>();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        boolean running = true;
        
        System.out.println("=== Student Result Manager ===");
        
        while (running) {
            displayMenu();
            int choice = getIntInput("Enter your choice (1-5): ", 1, 5);
            
            switch (choice) {
                case 1:
                    addStudent();
                    break;
                case 2:
                    viewAllStudents();
                    break;
                case 3:
                    searchStudent();
                    break;
                case 4:
                    System.out.println("\nThank you for using Student Result Manager!");
                    running = false;
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
        
        scanner.close();
    }
    
    private static void displayMenu() {
        System.out.println("\n--- Main Menu ---");
        System.out.println("1. Add Student Result");
        System.out.println("2. View All Results");
        System.out.println("3. Search Student Result");
        System.out.println("4. Exit");
    }
    
    private static void addStudent() {
        System.out.println("\n--- Add New Student Result ---");
        
        System.out.print("Enter Roll Number: ");
        String rollNumber = scanner.nextLine();
        
        System.out.print("Enter Student Name: ");
        String name = scanner.nextLine();
        
        int[] marks = new int[Student.getSubjects().length];
        System.out.println("\nEnter marks out of " + Student.getMaxMarks() + " for each subject:");
        
        for (int i = 0; i < Student.getSubjects().length; i++) {
            marks[i] = getIntInput(Student.getSubjects()[i] + ": ", 0, Student.getMaxMarks());
        }
        
        Student student = new Student(rollNumber, name, marks);
        students.add(student);
        
        System.out.println("\nStudent result added successfully!");
        System.out.println(student);
    }
    
    private static void viewAllStudents() {
        if (students.isEmpty()) {
            System.out.println("\nNo student records found!");
            return;
        }
        
        System.out.println("\n--- All Student Results ---");
        for (Student student : students) {
            System.out.println(student);
        }
    }
    
    private static void searchStudent() {
        if (students.isEmpty()) {
            System.out.println("\nNo student records found!");
            return;
        }
        
        System.out.print("\nEnter Roll Number to search: ");
        String rollNumber = scanner.nextLine();
        
        boolean found = false;
        for (Student student : students) {
            if (student.getRollNumber().equalsIgnoreCase(rollNumber)) {
                System.out.println("\n--- Student Found ---");
                System.out.println(student);
                found = true;
                break;
            }
        }
        
        if (!found) {
            System.out.println("\nNo student found with roll number: " + rollNumber);
        }
    }
    
    private static int getIntInput(String prompt, int min, int max) {
        while (true) {
            try {
                System.out.print(prompt);
                int value = Integer.parseInt(scanner.nextLine());
                if (value >= min && value <= max) {
                    return value;
                }
                System.out.printf("Please enter a number between %d and %d.\n", min, max);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid number.");
            }
        }
    }
}
