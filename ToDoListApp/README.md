# To-Do List Application

A Java console-based To-Do List application that helps you manage your tasks efficiently with a clean, intuitive interface.

## 🚀 Features

- **Task Management**
  - ✅ Add, edit, and delete tasks
  - ✅ Mark tasks as complete/incomplete
  - ✅ Set due dates and reminders
  - ✅ Organize with priorities (High, Medium, Low)
  - ✅ Categorize tasks for better organization

- **Smart Organization**
  - 📂 Categorize tasks (Work, Personal, Shopping, etc.)
  - ⏰ Due date tracking with overdue indicators
  - 🏷️ Priority levels with color coding
  - 🔍 Search and filter functionality

- **Data Management**
  - 💾 Automatic saving of tasks
  - 📊 Task statistics and completion rates
  - 📤 Export tasks to text file
  - 📥 Import tasks from CSV

- **User Experience**
  - 🎨 Colorful console interface
  - 📱 Keyboard-friendly navigation
  - 📝 Detailed task views
  - 📈 Progress tracking

## 🛠️ Prerequisites

- Java Development Kit (JDK) 11 or higher
- Maven 3.6.0 or higher (for building from source)
- Git (optional, for cloning the repository)

## 🚀 Quick Start

### Option 1: Using Pre-built JAR (Recommended)

1. Download the latest `todo-list-app-1.0-SNAPSHOT-jar-with-dependencies.jar` from the releases page
2. Open a terminal in the download directory
3. Run: `java -jar todo-list-app-1.0-SNAPSHOT-jar-with-dependencies.jar`

### Option 2: Build from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-list-app.git
   cd todo-list-app
   ```

2. Build the project:
   ```bash
   mvn clean package
   ```

3. Run the application:
   ```bash
   # On Windows
   .\run.bat
   
   # On Linux/Mac
   chmod +x run.sh
   ./run.sh
   ```
   
   Or directly with Maven:
   ```bash
   mvn exec:java
   ```

## 📂 Project Structure

```
src/main/java/com/todo/app/
├── model/
│   ├── Task.java        # Task data model
│   ├── Category.java    # Task categories
│   └── Priority.java    # Priority levels (High, Medium, Low)
├── service/
│   ├── TaskService.java # Business logic for task management
│   └── FileService.java # File I/O operations
└── ToDoApp.java         # Main application class
```

## 🎯 Usage Guide

### Main Menu
```
=== MAIN MENU ===
1. View All Tasks
2. Add New Task
3. Edit Task
4. Delete Task
5. View Tasks by Status
6. View Tasks by Category
7. View Tasks by Priority
8. View Statistics
9. Exit
```

### Task Management
- **Add Task**: Create new tasks with title, description, due date, priority, and category
- **Edit Task**: Modify any aspect of an existing task
- **Delete Task**: Remove tasks you no longer need
- **Mark Complete**: Toggle task completion status

### Viewing Tasks
- **All Tasks**: View your complete task list
- **By Status**: Filter by active, completed, or overdue tasks
- **By Category**: Group tasks by their categories
- **By Priority**: Focus on high-priority items

### Statistics
- Task completion rates
- Tasks by priority distribution
- Category-wise task breakdown
- Overdue task count

## 💾 Data Storage

Your tasks are automatically saved to `data/tasks.json` in the application directory. 
This file is created automatically when you save tasks and loaded when the application starts.

## 📝 Export/Import

- **Export**: Save your tasks to a text file
- **Import**: Load tasks from a CSV file (format: title,description,due_date,priority,category)

## 🛠️ Development

### Building
```bash
mvn clean package
```

### Running Tests
```bash
mvn test
```

### Creating a Fat JAR
```bash
mvn clean compile assembly:single
```

The output JAR will be in `target/todo-list-app-1.0-SNAPSHOT-jar-with-dependencies.jar`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Java 11 and Maven
- Uses Gson for JSON processing
- Inspired by productivity enthusiasts everywhere
