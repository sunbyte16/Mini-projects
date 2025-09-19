# Library Management System

A Java console application for managing library operations including book management, member management, and book lending/returning.

## Features

- **Book Management**
  - Add new books
  - Search for books
  - View all books
  - Update book details
  - Remove books

- **Member Management**
  - Add new members
  - View member details
  - Update member information
  - Remove members

- **Book Lending**
  - Issue books to members
  - Return books
  - View issued books
  - Calculate fines for late returns

- **Reports**
  - Generate book reports
  - Generate member reports
  - View transaction history

## Prerequisites

- Java Development Kit (JDK) 8 or higher

## How to Run

1. Navigate to the project directory
2. Compile the Java files:
   ```
   javac src/main/java/com/library/management/*.java -d target/classes
   ```
3. Run the application:
   ```
   java -cp target/classes com.library.management.LibraryManagementSystem
   ```

## Project Structure

```
src/main/java/com/library/management/
├── model/
│   ├── Book.java
│   ├── Member.java
│   └── Transaction.java
├── service/
│   ├── LibraryService.java
│   └── ReportService.java
└── LibraryManagementSystem.java  # Main application class
```

## Usage

1. Select an option from the main menu
2. Follow the on-screen instructions for each operation
3. Use the menu system to navigate between different functionalities

## Default Data

The system comes with sample data for testing:
- Books: 5 sample books
- Members: 3 sample members
