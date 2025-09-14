#!/usr/bin/env python3
"""
Setup script for Library Management System
This script helps initialize the library system with sample data.
"""

import os
import json
from datetime import datetime, timedelta


def create_sample_data():
    """Create sample data for the library system."""
    print("🚀 Setting up Library Management System with sample data...")
    
    # Sample books data
    books_data = {
        "1": {
            "book_id": "1",
            "title": "Python Programming",
            "author": "John Doe",
            "genre": "Programming",
            "availability": True
        },
        "2": {
            "book_id": "2", 
            "title": "Data Structures and Algorithms",
            "author": "Jane Smith",
            "genre": "Computer Science",
            "availability": True
        },
        "3": {
            "book_id": "3",
            "title": "Machine Learning Basics",
            "author": "Bob Johnson",
            "genre": "AI",
            "availability": True
        },
        "4": {
            "book_id": "4",
            "title": "Web Development Guide",
            "author": "Alice Brown",
            "genre": "Programming",
            "availability": True
        },
        "5": {
            "book_id": "5",
            "title": "Database Design",
            "author": "Charlie Wilson",
            "genre": "Database",
            "availability": True
        },
        "6": {
            "book_id": "6",
            "title": "Software Engineering",
            "author": "Diana Lee",
            "genre": "Software Development",
            "availability": True
        },
        "7": {
            "book_id": "7",
            "title": "Computer Networks",
            "author": "Eve Davis",
            "genre": "Networking",
            "availability": True
        },
        "8": {
            "book_id": "8",
            "title": "Operating Systems",
            "author": "Frank Miller",
            "genre": "System Programming",
            "availability": True
        }
    }
    
    # Sample users data
    users_data = {
        "1": {
            "user_id": "1",
            "name": "Alice Johnson",
            "borrowed_books": []
        },
        "2": {
            "user_id": "2",
            "name": "Bob Smith",
            "borrowed_books": []
        },
        "3": {
            "user_id": "3",
            "name": "Carol Davis",
            "borrowed_books": []
        },
        "4": {
            "user_id": "4",
            "name": "David Wilson",
            "borrowed_books": []
        },
        "5": {
            "user_id": "5",
            "name": "Eve Brown",
            "borrowed_books": []
        }
    }
    
    # Sample borrowed books data (empty initially)
    borrowed_books_data = {}
    
    # Save data to files
    try:
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(books_data, f, indent=2, ensure_ascii=False)
        print("✅ Created books.json with 8 sample books")
        
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
        print("✅ Created users.json with 5 sample users")
        
        with open("borrowed_books.json", "w", encoding="utf-8") as f:
            json.dump(borrowed_books_data, f, indent=2, ensure_ascii=False)
        print("✅ Created borrowed_books.json (empty)")
        
        print("\n🎉 Setup completed successfully!")
        print("\n📚 Sample data includes:")
        print("   - 8 books across different genres")
        print("   - 5 sample users")
        print("   - Ready for borrowing operations")
        
        print("\n🚀 To start the Library Management System, run:")
        print("   python library_management.py")
        print("\n   Or on Windows:")
        print("   run_library.bat")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")


def main():
    """Main setup function."""
    print("=" * 60)
    print("📚 LIBRARY MANAGEMENT SYSTEM SETUP")
    print("=" * 60)
    
    # Check if data files already exist
    existing_files = []
    for file in ["books.json", "users.json", "borrowed_books.json"]:
        if os.path.exists(file):
            existing_files.append(file)
    
    if existing_files:
        print(f"\n⚠️  Found existing data files: {', '.join(existing_files)}")
        response = input("Do you want to overwrite them? (yes/no): ").strip().lower()
        if response != "yes":
            print("❌ Setup cancelled. Existing files preserved.")
            return
    
    create_sample_data()


if __name__ == "__main__":
    main()
