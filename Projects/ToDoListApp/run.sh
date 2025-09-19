#!/bin/bash
echo "Building and running To-Do List App..."

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo "Maven is not installed or not in PATH. Please install Maven first."
    exit 1
fi

# Clean and build the project
mvn clean package

if [ $? -ne 0 ]; then
    echo "Build failed. Please check the error messages above."
    exit 1
fi

# Run the application
java -cp "target/todo-list-app-1.0-SNAPSHOT-jar-with-dependencies.jar" com.todo.app.ToDoApp
