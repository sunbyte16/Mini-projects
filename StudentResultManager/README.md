# Student Result Manager

A simple Java console application for managing student results, calculating grades, and generating reports.

## Features

- Add student details and marks for multiple subjects
- Calculate total marks and percentage
- Determine grade based on percentage
- Generate detailed student result reports
- View all student records
- Simple and intuitive console interface

## Prerequisites

- Java Development Kit (JDK) 8 or higher
- Maven (for building the project)

## How to Run

1. Clone the repository
2. Navigate to the project directory
3. Compile the Java files:
   ```
   javac src/main/java/com/student/result/manager/*.java -d target/classes
   ```
4. Run the application:
   ```
   java -cp target/classes com.student.result.manager.StudentResultManager
   ```

## Usage

1. Select an option from the main menu
2. Add student details and marks when prompted
3. View results and reports
4. Exit when done

## Project Structure

```
src/main/java/com/student/result/manager/
├── Student.java           # Student entity class
├── ResultCalculator.java  # Logic for calculations
└── StudentResultManager.java  # Main application class
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
