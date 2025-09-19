package com.library.management.service;

import com.library.management.model.*;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ReportService {
    private final LibraryService libraryService;

    public ReportService(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    public String generateBookReport() {
        List<Book> books = libraryService.getAllBooks();
        StringBuilder report = new StringBuilder();
        
        report.append("=== BOOK INVENTORY REPORT ===\n");
        report.append(String.format("%-15s %-40s %-25s %-15s %-10s %-10s\n", 
            "ISBN", "Title", "Author", "Category", "Available", "Total"));
        report.append("-".repeat(120)).append("\n");
        
        for (Book book : books) {
            report.append(String.format("%-15s %-40s %-25s %-15s %-10d %-10d\n",
                book.getIsbn(),
                truncate(book.getTitle(), 38),
                truncate(book.getAuthor(), 23),
                book.getCategory(),
                book.getAvailableCopies(),
                book.getTotalCopies()));
        }
        
        // Add summary
        report.append("\n=== SUMMARY ===\n");
        report.append(String.format("Total Books: %d\n", books.size()));
        report.append(String.format("Total Available: %d\n", 
            books.stream().filter(Book::isAvailable).count()));
        
        // Books by category
        Map<String, Long> booksByCategory = books.stream()
            .collect(Collectors.groupingBy(Book::getCategory, Collectors.counting()));
        
        if (!booksByCategory.isEmpty()) {
            report.append("\nBooks by Category:\n");
            booksByCategory.forEach((category, count) -> 
                report.append(String.format("- %-20s: %d\n", category, count)));
        }
        
        return report.toString();
    }

    public String generateMemberReport() {
        List<Member> members = libraryService.getAllMembers();
        StringBuilder report = new StringBuilder();
        
        report.append("=== MEMBER REPORT ===\n");
        report.append(String.format("%-10s %-30s %-25s %-15s %-10s\n", 
            "Member ID", "Name", "Email", "Phone", "Books Borrowed"));
        report.append("-".repeat(95)).append("\n");
        
        for (Member member : members) {
            report.append(String.format("%-10s %-30s %-25s %-15s %-10d\n",
                member.getMemberId(),
                truncate(member.getName(), 28),
                truncate(member.getEmail(), 23),
                member.getPhoneNumber(),
                member.getBorrowedBooksCount()));
        }
        
        // Add summary
        report.append("\n=== SUMMARY ===\n");
        report.append(String.format("Total Members: %d\n", members.size()));
        
        // Members with overdue books
        List<Transaction> overdueBooks = libraryService.getOverdueBooks();
        if (!overdueBooks.isEmpty()) {
            report.append("\nMEMBERS WITH OVERDUE BOOKS:\n");
            overdueBooks.forEach(transaction -> 
                report.append(String.format("- %s (Due: %s, Book: %s)\n",
                    transaction.getMember().getName(),
                    transaction.getDueDate(),
                    transaction.getBook().getTitle())));
        }
        
        return report.toString();
    }

    public String generateTransactionReport() {
        List<Transaction> transactions = libraryService.getTransactionHistory();
        if (transactions.isEmpty()) {
            return "No transactions found.";
        }
        
        StringBuilder report = new StringBuilder();
        report.append("=== TRANSACTION HISTORY ===\n");
        report.append(String.format("%-12s %-15s %-30s %-15s %-12s %-12s %-10s\n", 
            "TXN ID", "Type", "Book", "Member", "Issue Date", "Due Date", "Status"));
        report.append("-".repeat(120)).append("\n");
        
        for (Transaction txn : transactions) {
            String status = "";
            if (txn.getReturnDate() != null) {
                status = "Returned on " + txn.getReturnDate();
            } else if (txn.isOverdue()) {
                status = String.format("OVERDUE (Fine: $%.2f)", txn.getFineAmount());
            } else {
                status = "On Loan";
            }
            
            report.append(String.format("%-12s %-15s %-30s %-15s %-12s %-12s %-10s\n",
                txn.getTransactionId(),
                txn.getType(),
                truncate(txn.getBook().getTitle(), 28),
                txn.getMember().getName(),
                txn.getIssueDate(),
                txn.getDueDate(),
                status));
        }
        
        return report.toString();
    }
    
    public String generateOverdueReport() {
        List<Transaction> overdueBooks = libraryService.getOverdueBooks();
        if (overdueBooks.isEmpty()) {
            return "No overdue books found.";
        }
        
        StringBuilder report = new StringBuilder();
        report.append("=== OVERDUE BOOKS REPORT ===\n");
        report.append(String.format("%-30s %-20s %-15s %-12s %-10s\n", 
            "Book Title", "Borrower", "Member ID", "Due Date", "Days Overdue"));
        report.append("-".repeat(95)).append("\n");
        
        for (Transaction txn : overdueBooks) {
            long daysOverdue = java.time.temporal.ChronoUnit.DAYS.between(
                txn.getDueDate(), java.time.LocalDate.now());
            
            report.append(String.format("%-30s %-20s %-15s %-12s %-10d\n",
                truncate(txn.getBook().getTitle(), 28),
                truncate(txn.getMember().getName(), 18),
                txn.getMember().getMemberId(),
                txn.getDueDate(),
                daysOverdue));
        }
        
        // Calculate total fines
        double totalFines = overdueBooks.stream()
            .mapToDouble(Transaction::calculateFine)
            .sum();
            
        report.append("\nTotal Potential Fines: $").append(String.format("%.2f", totalFines));
        
        return report.toString();
    }
    
    private String truncate(String str, int maxLength) {
        if (str == null) return "";
        return str.length() > maxLength ? str.substring(0, maxLength - 3) + "..." : str;
    }
}
