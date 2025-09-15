import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
        self.categories = ["Personal", "Work", "Shopping", "Health", "Other"]
        self.priorities = ["High", "Medium", "Low"]
    
    def load_todos(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_todos(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=4)
    
    def add_task(self, task, category=None, priority="Medium", due_date=None):
        task_id = len(self.todos) + 1
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if category and category not in self.categories:
            self.categories.append(category)
        
        task_data = {
            "id": task_id,
            "task": task,
            "category": category or "Uncategorized",
            "priority": priority if priority in self.priorities else "Medium",
            "due_date": due_date,
            "completed": False,
            "created_at": created_at,
            "completed_at": None
        }
        
        self.todos.append(task_data)
        self.save_todos()
        return task_id
    
    def list_tasks(self, show_completed=False, category_filter=None, priority_filter=None):
        filtered_tasks = []
        
        for task in self.todos:
            if not show_completed and task["completed"]:
                continue
            if category_filter and task["category"] != category_filter:
                continue
            if priority_filter and task["priority"] != priority_filter:
                continue
            filtered_tasks.append(task)
        
        if not filtered_tasks:
            print("\nNo tasks found!")
            return
        
        print("\n{:<5} {:<40} {:<15} {:<10} {:<15} {:<10}".format(
            "ID", "Task", "Category", "Priority", "Due Date", "Status"))
        print("-" * 105)
        
        for task in filtered_tasks:
            status = "✅" if task["completed"] else "⏳"
            due_date = task.get("due_date", "No due date")
            
            print("{:<5} {:<40} {:<15} {:<10} {:<15} {:<10}".format(
                task["id"],
                task["task"][:37] + '...' if len(task["task"]) > 37 else task["task"],
                task["category"][:12] + '...' if len(task["category"]) > 12 else task["category"],
                task["priority"],
                due_date,
                status
            ))
    
    def complete_task(self, task_id):
        for task in self.todos:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_todos()
                return True
        return False
    
    def delete_task(self, task_id):
        for i, task in enumerate(self.todos):
            if task["id"] == task_id:
                del self.todos[i]
                # Reassign IDs
                for j in range(i, len(self.todos)):
                    self.todos[j]["id"] = j + 1
                self.save_todos()
                return True
        return False
    
    def get_stats(self):
        total = len(self.todos)
        completed = sum(1 for task in self.todos if task["completed"])
        pending = total - completed
        
        print("\n=== Task Statistics ===")
        print(f"Total tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        
        if total > 0:
            completion_rate = (completed / total) * 100
            print(f"Completion rate: {completion_rate:.1f}%")
        
        # Category distribution
        if self.todos:
            print("\nTasks by category:")
            for category in self.categories:
                count = sum(1 for task in self.todos if task["category"] == category)
                if count > 0:
                    print(f"- {category}: {count} tasks")

def display_menu():
    print("\n=== To-Do List Manager ===")
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. Mark Task as Complete")
    print("5. Delete Task")
    print("6. View Statistics")
    print("7. Exit")

def get_valid_input(prompt, input_type=str, valid_options=None):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and valid_options is None:
                return None
                
            if input_type == int:
                user_input = int(user_input)
            
            if valid_options and user_input not in valid_options:
                print(f"Please enter one of: {', '.join(map(str, valid_options))}")
                continue
                
            return user_input
            
        except ValueError:
            print("Invalid input. Please try again.")

def main():
    todo_list = TodoList()
    
    while True:
        display_menu()
        choice = get_valid_input("\nEnter your choice (1-7): ", int, range(1, 8))
        
        if choice == 1:  # Add New Task
            print("\n=== Add New Task ===")
            task = input("Enter task description: ").strip()
            
            print("\nAvailable categories:")
            for i, category in enumerate(todo_list.categories, 1):
                print(f"{i}. {category}")
            print(f"{len(todo_list.categories) + 1}. Add new category")
            
            cat_choice = get_valid_input(
                f"\nSelect category (1-{len(todo_list.categories) + 1}): ",
                int, range(1, len(todo_list.categories) + 2)
            )
            
            if cat_choice == len(todo_list.categories) + 1:
                category = input("Enter new category name: ").strip()
            else:
                category = todo_list.categories[cat_choice - 1]
            
            print("\nSelect priority:")
            for i, priority in enumerate(todo_list.priorities, 1):
                print(f"{i}. {priority}")
            
            pri_choice = get_valid_input(
                f"\nSelect priority (1-{len(todo_list.priorities)}): ",
                int, range(1, len(todo_list.priorities) + 1)
            )
            priority = todo_list.priorities[pri_choice - 1]
            
            due_date = input("\nEnter due date (YYYY-MM-DD, or press Enter for none): ").strip()
            
            task_id = todo_list.add_task(task, category, priority, due_date or None)
            print(f"\n✅ Task added successfully with ID: {task_id}")
            
        elif choice == 2:  # View All Tasks
            print("\n=== All Tasks ===")
            todo_list.list_tasks(show_completed=True)
            
        elif choice == 3:  # View Pending Tasks
            print("\n=== Pending Tasks ===")
            todo_list.list_tasks(show_completed=False)
            
        elif choice == 4:  # Mark Task as Complete
            task_id = get_valid_input("\nEnter task ID to mark as complete: ", int)
            if todo_list.complete_task(task_id):
                print("\n✅ Task marked as complete!")
            else:
                print("\n❌ Task not found!")
                
        elif choice == 5:  # Delete Task
            task_id = get_valid_input("\nEnter task ID to delete: ", int)
            if todo_list.delete_task(task_id):
                print("\n🗑️  Task deleted successfully!")
            else:
                print("\n❌ Task not found!")
                
        elif choice == 6:  # View Statistics
            todo_list.get_stats()
            
        elif choice == 7:  # Exit
            print("\nThank you for using the To-Do List Manager!")
            break

if __name__ == "__main__":
    main()
