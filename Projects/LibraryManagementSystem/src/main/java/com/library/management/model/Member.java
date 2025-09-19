package com.library.management.model;

import java.util.ArrayList;
import java.util.List;

public class Member {
    private String memberId;
    private String name;
    private String email;
    private String phoneNumber;
    private String address;
    private List<Book> borrowedBooks;
    private double fineAmount;

    public Member(String memberId, String name, String email, String phoneNumber, String address) {
        this.memberId = memberId;
        this.name = name;
        this.email = email;
        this.phoneNumber = phoneNumber;
        this.address = address;
        this.borrowedBooks = new ArrayList<>();
        this.fineAmount = 0.0;
    }

    // Getters and Setters
    public String getMemberId() {
        return memberId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public List<Book> getBorrowedBooks() {
        return new ArrayList<>(borrowedBooks);
    }

    public double getFineAmount() {
        return fineAmount;
    }

    // Business methods
    public void borrowBook(Book book) {
        if (book != null && book.isAvailable()) {
            borrowedBooks.add(book);
            book.issueBook();
        }
    }

    public void returnBook(Book book) {
        if (borrowedBooks.remove(book)) {
            book.returnBook();
            // Check for late return and calculate fine if needed
            // This is a simplified version - in a real app, you'd track due dates
        }
    }

    public void addFine(double amount) {
        if (amount > 0) {
            fineAmount += amount;
        }
    }

    public void payFine(double amount) {
        if (amount > 0 && amount <= fineAmount) {
            fineAmount -= amount;
        }
    }

    public int getBorrowedBooksCount() {
        return borrowedBooks.size();
    }

    @Override
    public String toString() {
        return String.format("""
            Member ID: %s
            Name: %s
            Email: %s
            Phone: %s
            Address: %s
            Books Borrowed: %d
            Current Fine: $%.2f""",
            memberId, name, email, phoneNumber, address, 
            borrowedBooks.size(), fineAmount);
    }
}
