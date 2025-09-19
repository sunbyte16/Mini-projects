package com.library.management.model;

import java.time.LocalDate;

public class Transaction {
    private String transactionId;
    private Book book;
    private Member member;
    private LocalDate issueDate;
    private LocalDate dueDate;
    private LocalDate returnDate;
    private double fineAmount;
    private TransactionType type;

    public enum TransactionType {
        ISSUE,
        RETURN,
        RENEWAL,
        FINE
    }

    public Transaction(String transactionId, Book book, Member member, 
                      LocalDate issueDate, LocalDate dueDate, TransactionType type) {
        this.transactionId = transactionId;
        this.book = book;
        this.member = member;
        this.issueDate = issueDate;
        this.dueDate = dueDate;
        this.type = type;
        this.fineAmount = 0.0;
    }

    // Getters and Setters
    public String getTransactionId() {
        return transactionId;
    }

    public Book getBook() {
        return book;
    }

    public Member getMember() {
        return member;
    }

    public LocalDate getIssueDate() {
        return issueDate;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }

    public LocalDate getReturnDate() {
        return returnDate;
    }

    public void setReturnDate(LocalDate returnDate) {
        this.returnDate = returnDate;
    }

    public double getFineAmount() {
        return fineAmount;
    }

    public void setFineAmount(double fineAmount) {
        this.fineAmount = fineAmount;
    }

    public TransactionType getType() {
        return type;
    }

    public void setType(TransactionType type) {
        this.type = type;
    }

    // Business methods
    public boolean isOverdue() {
        return LocalDate.now().isAfter(dueDate) && returnDate == null;
    }

    public double calculateFine() {
        if (!isOverdue() || returnDate == null) {
            return 0.0;
        }
        
        long daysOverdue = java.time.temporal.ChronoUnit.DAYS.between(dueDate, returnDate);
        if (daysOverdue <= 0) {
            return 0.0;
        }
        
        // Example fine calculation: $0.50 per day overdue
        double fineRate = 0.50;
        return daysOverdue * fineRate;
    }

    @Override
    public String toString() {
        return String.format("""
            Transaction ID: %s
            Book: %s
            Member: %s
            Type: %s
            Issue Date: %s
            Due Date: %s
            Return Date: %s
            Fine: $%.2f""",
            transactionId,
            book.getTitle(),
            member.getName(),
            type,
            issueDate,
            dueDate,
            returnDate != null ? returnDate.toString() : "Not returned",
            fineAmount);
    }
}
