package com.library.management;

import com.library.management.model.*;
import com.library.management.service.*;
import java.util.*;

public class LibraryManagementSystem {
    private static final Scanner scanner = new Scanner(System.in);
    private static final LibraryService libraryService = new LibraryService();
    private static final ReportService reportService = new ReportService(libraryService);
    private static boolean isRunning = true;

    public static void main(String[] args) {
        System.out.println("=== Library Management System ===");
        
        while (isRunning) {
            displayMainMenu();
            int choice = getIntInput("Enter your choice (1-6): ", 1, 6);
            
            switch (choice) {
                case 1 -> handleBookOperations();
                case 2 -> handleMemberOperations();
                case 3 -> handleTransactionOperations();
                case 4 -> generateReports();
                case 5 -> displaySystemInfo();
                case 6 -> exitSystem();
                default -> System.out.println("Invalid choice. Please try again.");
            }
        }
        
        scanner.close();
    }

    private static void displayMainMenu() {
        System.out.println("\n=== MAIN MENU ===");
        System.out.println("1. Book Operations");
        System.out.println("2. Member Operations");
        System.out.println("3. Transaction Operations");
        System.out.println("4. Generate Reports");
        System.out.println("5. System Information");
        System.out.println("6. Exit");
    }

    // Book Operations
    private static void handleBookOperations() {
        while (true) {
            System.out.println("\n=== BOOK OPERATIONS ===");
            System.out.println("1. Add New Book");
            System.out.println("2. Search Books");
            System.out.println("3. View All Books");
            System.out.println("4. Update Book");
            System.out.println("5. Remove Book");
            System.out.println("6. Back to Main Menu");
            
            int choice = getIntInput("Enter your choice (1-6): ", 1, 6);
            
            switch (choice) {
                case 1 -> addNewBook();
                case 2 -> searchBooks();
                case 3 -> viewAllBooks();
                case 4 -> updateBook();
                case 5 -> removeBook();
                case 6 -> { return; }
            }
        }
    }

    private static void addNewBook() {
        System.out.println("\n=== ADD NEW BOOK ===");
        System.out.print("Enter ISBN: ");
        String isbn = scanner.nextLine().trim();
        
        if (libraryService.findBookByIsbn(isbn) != null) {
            System.out.println("A book with this ISBN already exists!");
            return;
        }
        
        System.out.print("Enter Title: ");
        String title = scanner.nextLine().trim();
        
        System.out.print("Enter Author: ");
        String author = scanner.nextLine().trim();
        
        System.out.print("Enter Publisher: ");
        String publisher = scanner.nextLine().trim();
        
        int year = getIntInput("Enter Publication Year: ", 1000, 2100);
        int copies = getIntInput("Enter Number of Copies: ", 1, 1000);
        
        System.out.print("Enter Category: ");
        String category = scanner.nextLine().trim();
        
        Book newBook = new Book(isbn, title, author, publisher, year, copies, category);
        libraryService.addBook(newBook);
        
        System.out.println("\nBook added successfully!");
        System.out.println(newBook);
    }

    private static void searchBooks() {
        System.out.print("\nEnter search term (title/author/ISBN): ");
        String query = scanner.nextLine().trim();
        
        List<Book> results = libraryService.searchBooks(query);
        
        if (results.isEmpty()) {
            System.out.println("No books found matching your search.");
            return;
        }
        
        System.out.println("\n=== SEARCH RESULTS ===");
        results.forEach(book -> {
            System.out.println(book);
            System.out.println("-".repeat(50));
        });
    }

    private static void viewAllBooks() {
        System.out.println(reportService.generateBookReport());
    }

    private static void updateBook() {
        System.out.print("\nEnter ISBN of the book to update: ");
        String isbn = scanner.nextLine().trim();
        
        Book book = libraryService.findBookByIsbn(isbn);
        if (book == null) {
            System.out.println("Book not found!");
            return;
        }
        
        System.out.println("\nCurrent Book Details:");
        System.out.println(book);
        
        System.out.println("\nEnter new details (press Enter to keep current value):");
        
        System.out.print("Title [" + book.getTitle() + "]: ");
        String title = scanner.nextLine().trim();
        if (!title.isEmpty()) book.setTitle(title);
        
        System.out.print("Author [" + book.getAuthor() + "]: ");
        String author = scanner.nextLine().trim();
        if (!author.isEmpty()) book.setAuthor(author);
        
        System.out.print("Publisher [" + book.getPublisher() + "]: ");
        String publisher = scanner.nextLine().trim();
        if (!publisher.isEmpty()) book.setPublisher(publisher);
        
        System.out.print("Year [" + book.getPublicationYear() + "]: ");
        String yearStr = scanner.nextLine().trim();
        if (!yearStr.isEmpty()) {
            book.setPublicationYear(Integer.parseInt(yearStr));
        }
        
        System.out.print("Total Copies [" + book.getTotalCopies() + "]: ");
        String copiesStr = scanner.nextLine().trim();
        if (!copiesStr.isEmpty()) {
            book.setTotalCopies(Integer.parseInt(copiesStr));
        }
        
        System.out.print("Category [" + book.getCategory() + "]: ");
        String category = scanner.nextLine().trim();
        if (!category.isEmpty()) book.setCategory(category);
        
        System.out.println("\nBook updated successfully!");
        System.out.println(book);
    }

    private static void removeBook() {
        System.out.print("\nEnter ISBN of the book to remove: ");
        String isbn = scanner.nextLine().trim();
        
        if (libraryService.removeBook(isbn)) {
            System.out.println("Book removed successfully!");
        } else {
            System.out.println("Book not found or could not be removed!");
        }
    }

    // Member Operations
    private static void handleMemberOperations() {
        while (true) {
            System.out.println("\n=== MEMBER OPERATIONS ===");
            System.out.println("1. Add New Member");
            System.out.println("2. Search Members");
            System.out.println("3. View All Members");
            System.out.println("4. Update Member");
            System.out.println("5. Remove Member");
            System.out.println("6. Back to Main Menu");
            
            int choice = getIntInput("Enter your choice (1-6): ", 1, 6);
            
            switch (choice) {
                case 1 -> addNewMember();
                case 2 -> searchMembers();
                case 3 -> viewAllMembers();
                case 4 -> updateMember();
                case 5 -> removeMember();
                case 6 -> { return; }
            }
        }
    }

    private static void addNewMember() {
        System.out.println("\n=== ADD NEW MEMBER ===");
        
        System.out.print("Enter Member ID: ");
        String memberId = scanner.nextLine().trim().toUpperCase();
        
        if (libraryService.findMemberById(memberId) != null) {
            System.out.println("A member with this ID already exists!");
            return;
        }
        
        System.out.print("Enter Full Name: ");
        String name = scanner.nextLine().trim();
        
        System.out.print("Enter Email: ");
        String email = scanner.nextLine().trim();
        
        System.out.print("Enter Phone Number: ");
        String phone = scanner.nextLine().trim();
        
        System.out.print("Enter Address: ");
        String address = scanner.nextLine().trim();
        
        Member newMember = new Member(memberId, name, email, phone, address);
        libraryService.addMember(newMember);
        
        System.out.println("\nMember added successfully!");
        System.out.println(newMember);
    }

    private static void searchMembers() {
        System.out.print("\nEnter search term (name/member ID): ");
        String query = scanner.nextLine().trim();
        
        List<Member> results = libraryService.searchMembers(query);
        
        if (results.isEmpty()) {
            System.out.println("No members found matching your search.");
            return;
        }
        
        System.out.println("\n=== SEARCH RESULTS ===");
        results.forEach(member -> {
            System.out.println(member);
            System.out.println("-".repeat(50));
        });
    }

    private static void viewAllMembers() {
        System.out.println(reportService.generateMemberReport());
    }

    private static void updateMember() {
        System.out.print("\nEnter Member ID to update: ");
        String memberId = scanner.nextLine().trim().toUpperCase();
        
        Member member = libraryService.findMemberById(memberId);
        if (member == null) {
            System.out.println("Member not found!");
            return;
        }
        
        System.out.println("\nCurrent Member Details:");
        System.out.println(member);
        
        System.out.println("\nEnter new details (press Enter to keep current value):");
        
        System.out.print("Name [" + member.getName() + "]: ");
        String name = scanner.nextLine().trim();
        if (!name.isEmpty()) member.setName(name);
        
        System.out.print("Email [" + member.getEmail() + "]: ");
        String email = scanner.nextLine().trim();
        if (!email.isEmpty()) member.setEmail(email);
        
        System.out.print("Phone [" + member.getPhoneNumber() + "]: ");
        String phone = scanner.nextLine().trim();
        if (!phone.isEmpty()) member.setPhoneNumber(phone);
        
        System.out.print("Address [" + member.getAddress() + "]: ");
        String address = scanner.nextLine().trim();
        if (!address.isEmpty()) member.setAddress(address);
        
        System.out.println("\nMember updated successfully!");
        System.out.println(member);
    }

    private static void removeMember() {
        System.out.print("\nEnter Member ID to remove: ");
        String memberId = scanner.nextLine().trim().toUpperCase();
        
        if (libraryService.removeMember(memberId)) {
            System.out.println("Member removed successfully!");
        } else {
            System.out.println("Member not found or could not be removed!");
        }
    }

    // Transaction Operations
    private static void handleTransactionOperations() {
        while (true) {
            System.out.println("\n=== TRANSACTION OPERATIONS ===");
            System.out.println("1. Issue Book");
            System.out.println("2. Return Book");
            System.out.println("3. View Transaction History");
            System.out.println("4. View Overdue Books");
            System.out.println("5. Back to Main Menu");
            
            int choice = getIntInput("Enter your choice (1-5): ", 1, 5);
            
            switch (choice) {
                case 1 -> issueBook();
                case 2 -> returnBook();
                case 3 -> viewTransactionHistory();
                case 4 -> viewOverdueBooks();
                case 5 -> { return; }
            }
        }
    }

    private static void issueBook() {
        System.out.println("\n=== ISSUE BOOK ===");
        
        System.out.print("Enter Member ID: ");
        String memberId = scanner.nextLine().trim().toUpperCase();
        
        Member member = libraryService.findMemberById(memberId);
        if (member == null) {
            System.out.println("Member not found!");
            return;
        }
        
        System.out.print("Enter Book ISBN: ");
        String isbn = scanner.nextLine().trim();
        
        if (libraryService.issueBook(memberId, isbn)) {
            System.out.println("Book issued successfully!");
        } else {
            System.out.println("Failed to issue book. Check if the book is available or if the member has reached the limit.");
        }
    }

    private static void returnBook() {
        System.out.println("\n=== RETURN BOOK ===");
        
        System.out.print("Enter Member ID: ");
        String memberId = scanner.nextLine().trim().toUpperCase();
        
        Member member = libraryService.findMemberById(memberId);
        if (member == null) {
            System.out.println("Member not found!");
            return;
        }
        
        System.out.print("Enter Book ISBN: ");
        String isbn = scanner.nextLine().trim();
        
        if (libraryService.returnBook(memberId, isbn)) {
            System.out.println("Book returned successfully!");
        } else {
            System.out.println("Failed to return book. Check if the book was actually issued to this member.");
        }
    }

    private static void viewTransactionHistory() {
        System.out.println(reportService.generateTransactionReport());
    }

    private static void viewOverdueBooks() {
        System.out.println(reportService.generateOverdueReport());
    }

    // Reports
    private static void generateReports() {
        while (true) {
            System.out.println("\n=== GENERATE REPORTS ===");
            System.out.println("1. Books Report");
            System.out.println("2. Members Report");
            System.out.println("3. Transactions Report");
            System.out.println("4. Overdue Books Report");
            System.out.println("5. Back to Main Menu");
            
            int choice = getIntInput("Enter your choice (1-5): ", 1, 5);
            
            switch (choice) {
                case 1 -> System.out.println(reportService.generateBookReport());
                case 2 -> System.out.println(reportService.generateMemberReport());
                case 3 -> System.out.println(reportService.generateTransactionReport());
                case 4 -> System.out.println(reportService.generateOverdueReport());
                case 5 -> { return; }
            }
            
            System.out.println("\nPress Enter to continue...");
            scanner.nextLine();
        }
    }

    // System Information
    private static void displaySystemInfo() {
        System.out.println("\n=== SYSTEM INFORMATION ===");
        System.out.println("Library Management System v1.0");
        System.out.println("Total Books: " + libraryService.getAllBooks().size());
        System.out.println("Total Members: " + libraryService.getAllMembers().size());
        System.out.println("Total Transactions: " + libraryService.getTransactionHistory().size());
        System.out.println("Overdue Books: " + libraryService.getOverdueBooks().size());
    }

    private static void exitSystem() {
        System.out.println("\nThank you for using Library Management System. Goodbye!");
        isRunning = false;
    }

    // Utility Methods
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
