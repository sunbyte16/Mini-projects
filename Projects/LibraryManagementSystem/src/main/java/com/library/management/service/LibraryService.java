package com.library.management.service;

import com.library.management.model.*;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

public class LibraryService {
    private Map<String, Book> books;
    private Map<String, Member> members;
    private List<Transaction> transactions;
    private int transactionCounter;

    public LibraryService() {
        this.books = new HashMap<>();
        this.members = new HashMap<>();
        this.transactions = new ArrayList<>();
        this.transactionCounter = 1000;
        initializeSampleData();
    }

    private void initializeSampleData() {
        // Add sample books
        addBook(new Book("978-0134685991", "Effective Java", "Joshua Bloch", "Addison-Wesley", 2018, 5, "Programming"));
        addBook(new Book("978-0201633610", "Design Patterns", "Erich Gamma", "Addison-Wesley", 1994, 3, "Computer Science"));
        addBook(new Book("978-0132350884", "Clean Code", "Robert C. Martin", "Prentice Hall", 2008, 4, "Software Engineering"));
        addBook(new Book("978-0596007126", "Head First Java", "Kathy Sierra", "O'Reilly Media", 2005, 2, "Programming"));
        addBook(new Book("978-1617297571", "Spring in Action", "Craig Walls", "Manning", 2020, 3, "Web Development"));

        // Add sample members
        addMember(new Member("M001", "John Doe", "john@example.com", "1234567890", "123 Main St"));
        addMember(new Member("M002", "Jane Smith", "jane@example.com", "0987654321", "456 Oak Ave"));
        addMember(new Member("M003", "Bob Johnson", "bob@example.com", "1122334455", "789 Pine Blvd"));
    }

    // Book related methods
    public void addBook(Book book) {
        books.put(book.getIsbn(), book);
    }

    public Book findBookByIsbn(String isbn) {
        return books.get(isbn);
    }

    public List<Book> searchBooks(String query) {
        String lowerQuery = query.toLowerCase();
        return books.values().stream()
            .filter(book -> book.getTitle().toLowerCase().contains(lowerQuery) ||
                           book.getAuthor().toLowerCase().contains(lowerQuery) ||
                           book.getIsbn().toLowerCase().contains(lowerQuery))
            .collect(Collectors.toList());
    }

    public List<Book> getAllBooks() {
        return new ArrayList<>(books.values());
    }

    public boolean updateBook(String isbn, Book updatedBook) {
        if (books.containsKey(isbn)) {
            books.put(isbn, updatedBook);
            return true;
        }
        return false;
    }

    public boolean removeBook(String isbn) {
        return books.remove(isbn) != null;
    }

    // Member related methods
    public void addMember(Member member) {
        members.put(member.getMemberId(), member);
    }

    public Member findMemberById(String memberId) {
        return members.get(memberId);
    }

    public List<Member> searchMembers(String query) {
        String lowerQuery = query.toLowerCase();
        return members.values().stream()
            .filter(member -> member.getName().toLowerCase().contains(lowerQuery) ||
                            member.getMemberId().toLowerCase().contains(lowerQuery))
            .collect(Collectors.toList());
    }

    public List<Member> getAllMembers() {
        return new ArrayList<>(members.values());
    }

    public boolean updateMember(String memberId, Member updatedMember) {
        if (members.containsKey(memberId)) {
            members.put(memberId, updatedMember);
            return true;
        }
        return false;
    }

    public boolean removeMember(String memberId) {
        return members.remove(memberId) != null;
    }

    // Transaction related methods
    public boolean issueBook(String memberId, String isbn) {
        Member member = findMemberById(memberId);
        Book book = findBookByIsbn(isbn);

        if (member == null || book == null || !book.isAvailable()) {
            return false;
        }

        // Check if member has reached the maximum allowed books (e.g., 5)
        if (member.getBorrowedBooksCount() >= 5) {
            return false;
        }

        // Create a new transaction
        String transactionId = "TXN" + (++transactionCounter);
        LocalDate issueDate = LocalDate.now();
        LocalDate dueDate = issueDate.plusWeeks(2); // 2 weeks loan period

        Transaction transaction = new Transaction(
            transactionId, book, member, issueDate, dueDate, 
            Transaction.TransactionType.ISSUE
        );

        // Update book and member
        member.borrowBook(book);
        transactions.add(transaction);

        return true;
    }

    public boolean returnBook(String memberId, String isbn) {
        Member member = findMemberById(memberId);
        Book book = findBookByIsbn(isbn);

        if (member == null || book == null) {
            return false;
        }

        // Find the most recent issue transaction for this book and member
        Optional<Transaction> transactionOpt = transactions.stream()
            .filter(t -> t.getBook().getIsbn().equals(isbn) &&
                        t.getMember().getMemberId().equals(memberId) &&
                        t.getReturnDate() == null)
            .findFirst();

        if (!transactionOpt.isPresent()) {
            return false;
        }

        Transaction transaction = transactionOpt.get();
        transaction.setReturnDate(LocalDate.now());
        
        // Calculate fine if book is returned late
        if (transaction.isOverdue()) {
            double fine = transaction.calculateFine();
            member.addFine(fine);
            transaction.setFineAmount(fine);
        }

        // Update book and member
        member.returnBook(book);
        transaction.setType(Transaction.TransactionType.RETURN);

        return true;
    }

    public List<Transaction> getTransactionHistory() {
        return new ArrayList<>(transactions);
    }

    public List<Book> getBorrowedBooks(String memberId) {
        Member member = findMemberById(memberId);
        return member != null ? member.getBorrowedBooks() : Collections.emptyList();
    }

    public List<Transaction> getOverdueBooks() {
        return transactions.stream()
            .filter(Transaction::isOverdue)
            .collect(Collectors.toList());
    }

    // Utility methods
    public int getTotalBooks() {
        return books.size();
    }

    public int getAvailableBooks() {
        return (int) books.values().stream()
            .filter(Book::isAvailable)
            .count();
    }

    public int getTotalMembers() {
        return members.size();
    }
}
