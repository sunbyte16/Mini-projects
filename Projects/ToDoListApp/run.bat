@echo off
echo Building and running To-Do List App...

REM Check if Maven is installed
mvn -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Maven is not installed or not in PATH. Please install Maven first.
    pause
    exit /b 1
)

REM Clean and build the project
mvn clean package

if %ERRORLEVEL% neq 0 (
    echo Build failed. Please check the error messages above.
    pause
    exit /b 1
)

REM Run the application
java -cp "target/todo-list-app-1.0-SNAPSHOT-jar-with-dependencies.jar" com.todo.app.ToDoApp

pause
