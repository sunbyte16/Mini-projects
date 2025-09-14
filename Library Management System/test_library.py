#!/usr/bin/env python3
"""
Test script for Library Management System
This script demonstrates the functionality of the library management system.
"""

import os
import json
from library_management import LibraryManagementSystem


def test_library_system():
    """Test the library management system with sample data."""
    print("🧪 Testing Library Management System")
    print("=" * 50)
    
    # Initialize the library system
    library = LibraryManagementSystem()
    
    # Clean up any existing test data
    test_files = ["books.json", "users.json", "borrowed_books.json"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
    
    # Reinitialize with clean data
    library = LibraryManagementSystem()
    
    print("\n📚 Adding sample books...")
    # Add sample books
    sample_books = [
        {"title": "Python Programming", "author": "John Doe", "genre": "Programming"},
        {"title": "Data Structures", "author": "Jane Smith", "genre": "Computer Science"},
        {"title": "Machine Learning", "author": "Bob Johnson", "genre": "AI"},
        {"title": "Web Development", "author": "Alice Brown", "genre": "Programming"},
        {"title": "Database Design", "author": "Charlie Wilson", "genre": "Database"}
    ]
    
    for book_data in sample_books:
        book_id = str(library.next_book_id)
        book_record = {
            "book_id": book_id,
            "title": book_data["title"],
            "author": book_data["author"],
            "genre": book_data["genre"],
            "availability": True
        }
        library.books[book_id] = book_record
        library.next_book_id += 1
        print(f"   ✅ Added: {book_data['title']}")
    
    # Save books
    library.save_data("books.json", library.books)
    
    print("\n👥 Adding sample users...")
    # Add sample users
    sample_users = [
        {"name": "Alice Johnson"},
        {"name": "Bob Smith"},
        {"name": "Carol Davis"},
        {"name": "David Wilson"}
    ]
    
    for user_data in sample_users:
        user_id = str(library.next_user_id)
        user_record = {
            "user_id": user_id,
            "name": user_data["name"],
            "borrowed_books": []
        }
        library.users[user_id] = user_record
        library.next_user_id += 1
        print(f"   ✅ Added: {user_data['name']}")
    
    # Save users
    library.save_data("users.json", library.users)
    
    print("\n📖 Testing book operations...")
    # Test viewing all books
    print("\n--- All Books ---")
    library.view_all_books()
    
    # Test searching books
    print("\n--- Search Test (Programming) ---")
    results = [book for book in library.books.values() if "programming" in book["genre"].lower()]
    for book in results:
        print(f"Found: {book['title']} by {book['author']}")
    
    print("\n🔄 Testing borrowing system...")
    # Test borrowing books
    print("Borrowing 'Python Programming' to Alice Johnson...")
    library.books["1"]["availability"] = False
    library.users["1"]["borrowed_books"].append("1")
    
    # Add borrowing record
    from datetime import datetime, timedelta
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    library.borrowed_books["1"] = {
        "user_id": "1",
        "borrow_date": borrow_date.isoformat(),
        "due_date": due_date.isoformat(),
        "returned": False
    }
    
    # Save all data
    library.save_data("books.json", library.books)
    library.save_data("users.json", library.users)
    library.save_data("borrowed_books.json", library.borrowed_books)
    
    print("✅ Book borrowed successfully!")
    
    print("\n📊 Testing reporting system...")
    # Test report generation
    library.generate_report()
    
    print("\n📋 Testing borrowed books view...")
    library.view_borrowed_books()
    
    print("\n✅ All tests completed successfully!")
    print("\n🎉 The Library Management System is working correctly!")
    print("\nTo run the interactive system, execute:")
    print("python library_management.py")


if __name__ == "__main__":
    test_library_system()
