#!/usr/bin/env python3
"""
Library Management System
A command-line interface for managing books and users in a library.
"""

import json
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sys


class LibraryManagementSystem:
    """Main class for the Library Management System."""
    
    def __init__(self):
        """Initialize the library management system."""
        self.books_file = "books.json"
        self.users_file = "users.json"
        self.borrowed_books_file = "borrowed_books.json"
        self.late_fee_per_day = 10  # ₹10 per day
        self.borrow_duration_days = 14  # 14 days borrowing period
        
        # Initialize data files
        self.books = self.load_data(self.books_file, {})
        self.users = self.load_data(self.users_file, {})
        self.borrowed_books = self.load_data(self.borrowed_books_file, {})
        
        # Generate IDs if files are empty
        if not self.books:
            self.next_book_id = 1
        else:
            self.next_book_id = max(int(k) for k in self.books.keys()) + 1 if self.books else 1
            
        if not self.users:
            self.next_user_id = 1
        else:
            self.next_user_id = max(int(k) for k in self.users.keys()) + 1 if self.users else 1

    def load_data(self, filename: str, default: dict) -> dict:
        """Load data from JSON file."""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return default
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load {filename}: {e}")
            return default

    def save_data(self, filename: str, data: dict) -> bool:
        """Save data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False

    def add_book(self) -> None:
        """Add a new book to the library."""
        print("\n" + "="*50)
        print("ADD NEW BOOK")
        print("="*50)
        
        try:
            title = input("Enter book title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                return
                
            author = input("Enter author name: ").strip()
            if not author:
                print("❌ Author cannot be empty!")
                return
                
            genre = input("Enter genre: ").strip()
            if not genre:
                print("❌ Genre cannot be empty!")
                return
            
            book_id = str(self.next_book_id)
            book_data = {
                "book_id": book_id,
                "title": title,
                "author": author,
                "genre": genre,
                "availability": True
            }
            
            self.books[book_id] = book_data
            self.next_book_id += 1
            
            if self.save_data(self.books_file, self.books):
                print(f"✅ Book added successfully! Book ID: {book_id}")
            else:
                print("❌ Failed to save book data!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error adding book: {e}")

    def view_all_books(self) -> None:
        """Display all books in the library."""
        print("\n" + "="*80)
        print("ALL BOOKS IN LIBRARY")
        print("="*80)
        
        if not self.books:
            print("📚 No books found in the library!")
            return
        
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Genre':<15} {'Status'}")
        print("-" * 80)
        
        for book in self.books.values():
            status = "✅ Available" if book["availability"] else "❌ Borrowed"
            print(f"{book['book_id']:<5} {book['title']:<30} {book['author']:<20} {book['genre']:<15} {status}")

    def search_books(self) -> None:
        """Search books by title, author, or genre."""
        print("\n" + "="*50)
        print("SEARCH BOOKS")
        print("="*50)
        
        if not self.books:
            print("📚 No books found in the library!")
            return
        
        print("Search by:")
        print("1. Title")
        print("2. Author")
        print("3. Genre")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            search_term = input("Enter search term: ").strip().lower()
            
            if not search_term:
                print("❌ Search term cannot be empty!")
                return
            
            results = []
            
            if choice == "1":
                results = [book for book in self.books.values() 
                          if search_term in book["title"].lower()]
            elif choice == "2":
                results = [book for book in self.books.values() 
                          if search_term in book["author"].lower()]
            elif choice == "3":
                results = [book for book in self.books.values() 
                          if search_term in book["genre"].lower()]
            else:
                print("❌ Invalid choice!")
                return
            
            if results:
                print(f"\n🔍 Found {len(results)} book(s):")
                print("-" * 80)
                print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Genre':<15} {'Status'}")
                print("-" * 80)
                
                for book in results:
                    status = "✅ Available" if book["availability"] else "❌ Borrowed"
                    print(f"{book['book_id']:<5} {book['title']:<30} {book['author']:<20} {book['genre']:<15} {status}")
            else:
                print("❌ No books found matching your search!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error searching books: {e}")

    def register_user(self) -> None:
        """Register a new user."""
        print("\n" + "="*50)
        print("REGISTER NEW USER")
        print("="*50)
        
        try:
            name = input("Enter user name: ").strip()
            if not name:
                print("❌ Name cannot be empty!")
                return
            
            user_id = str(self.next_user_id)
            user_data = {
                "user_id": user_id,
                "name": name,
                "borrowed_books": []
            }
            
            self.users[user_id] = user_data
            self.next_user_id += 1
            
            if self.save_data(self.users_file, self.users):
                print(f"✅ User registered successfully! User ID: {user_id}")
            else:
                print("❌ Failed to save user data!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error registering user: {e}")

    def borrow_book(self) -> None:
        """Allow a user to borrow a book."""
        print("\n" + "="*50)
        print("BORROW BOOK")
        print("="*50)
        
        try:
            user_id = input("Enter user ID: ").strip()
            if user_id not in self.users:
                print("❌ User not found!")
                return
            
            book_id = input("Enter book ID: ").strip()
            if book_id not in self.books:
                print("❌ Book not found!")
                return
            
            if not self.books[book_id]["availability"]:
                print("❌ Book is not available!")
                return
            
            # Check if user has already borrowed this book
            if book_id in self.users[user_id]["borrowed_books"]:
                print("❌ User has already borrowed this book!")
                return
            
            # Update book availability
            self.books[book_id]["availability"] = False
            
            # Add to user's borrowed books
            self.users[user_id]["borrowed_books"].append(book_id)
            
            # Record borrowing details
            borrow_date = datetime.now()
            due_date = borrow_date + timedelta(days=self.borrow_duration_days)
            
            self.borrowed_books[book_id] = {
                "user_id": user_id,
                "borrow_date": borrow_date.isoformat(),
                "due_date": due_date.isoformat(),
                "returned": False
            }
            
            if (self.save_data(self.books_file, self.books) and 
                self.save_data(self.users_file, self.users) and 
                self.save_data(self.borrowed_books_file, self.borrowed_books)):
                
                print(f"✅ Book borrowed successfully!")
                print(f"📅 Due date: {due_date.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("❌ Failed to save borrowing data!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error borrowing book: {e}")

    def return_book(self) -> None:
        """Allow a user to return a book."""
        print("\n" + "="*50)
        print("RETURN BOOK")
        print("="*50)
        
        try:
            user_id = input("Enter user ID: ").strip()
            if user_id not in self.users:
                print("❌ User not found!")
                return
            
            book_id = input("Enter book ID: ").strip()
            if book_id not in self.books:
                print("❌ Book not found!")
                return
            
            if book_id not in self.users[user_id]["borrowed_books"]:
                print("❌ User has not borrowed this book!")
                return
            
            # Calculate late fee
            late_fee = self.calculate_late_fee(book_id)
            
            # Update book availability
            self.books[book_id]["availability"] = True
            
            # Remove from user's borrowed books
            self.users[user_id]["borrowed_books"].remove(book_id)
            
            # Mark as returned
            if book_id in self.borrowed_books:
                self.borrowed_books[book_id]["returned"] = True
                self.borrowed_books[book_id]["return_date"] = datetime.now().isoformat()
            
            if (self.save_data(self.books_file, self.books) and 
                self.save_data(self.users_file, self.users) and 
                self.save_data(self.borrowed_books_file, self.borrowed_books)):
                
                print(f"✅ Book returned successfully!")
                if late_fee > 0:
                    print(f"💰 Late fee: ₹{late_fee}")
                else:
                    print("✅ No late fee - returned on time!")
            else:
                print("❌ Failed to save return data!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error returning book: {e}")

    def calculate_late_fee(self, book_id: str) -> int:
        """Calculate late fee for a book."""
        if book_id not in self.borrowed_books:
            return 0
        
        borrow_record = self.borrowed_books[book_id]
        due_date = datetime.fromisoformat(borrow_record["due_date"])
        current_date = datetime.now()
        
        if current_date > due_date:
            days_late = (current_date - due_date).days
            return days_late * self.late_fee_per_day
        
        return 0

    def delete_book(self) -> None:
        """Delete a book from the library."""
        print("\n" + "="*50)
        print("DELETE BOOK")
        print("="*50)
        
        try:
            book_id = input("Enter book ID to delete: ").strip()
            if book_id not in self.books:
                print("❌ Book not found!")
                return
            
            if not self.books[book_id]["availability"]:
                print("❌ Cannot delete book that is currently borrowed!")
                return
            
            book_title = self.books[book_id]["title"]
            confirm = input(f"Are you sure you want to delete '{book_title}'? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                del self.books[book_id]
                if self.save_data(self.books_file, self.books):
                    print("✅ Book deleted successfully!")
                else:
                    print("❌ Failed to save changes!")
            else:
                print("❌ Deletion cancelled!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error deleting book: {e}")

    def delete_user(self) -> None:
        """Delete a user from the system."""
        print("\n" + "="*50)
        print("DELETE USER")
        print("="*50)
        
        try:
            user_id = input("Enter user ID to delete: ").strip()
            if user_id not in self.users:
                print("❌ User not found!")
                return
            
            if self.users[user_id]["borrowed_books"]:
                print("❌ Cannot delete user who has borrowed books!")
                return
            
            user_name = self.users[user_id]["name"]
            confirm = input(f"Are you sure you want to delete user '{user_name}'? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                del self.users[user_id]
                if self.save_data(self.users_file, self.users):
                    print("✅ User deleted successfully!")
                else:
                    print("❌ Failed to save changes!")
            else:
                print("❌ Deletion cancelled!")
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        except Exception as e:
            print(f"❌ Error deleting user: {e}")

    def view_borrowed_books(self) -> None:
        """Display all borrowed books with user details."""
        print("\n" + "="*80)
        print("BORROWED BOOKS")
        print("="*80)
        
        if not self.borrowed_books:
            print("📚 No books are currently borrowed!")
            return
        
        print(f"{'Book ID':<8} {'Book Title':<30} {'User':<20} {'Due Date':<15} {'Status'}")
        print("-" * 80)
        
        for book_id, borrow_info in self.borrowed_books.items():
            if not borrow_info["returned"] and book_id in self.books:
                book = self.books[book_id]
                user = self.users.get(borrow_info["user_id"], {"name": "Unknown"})
                due_date = datetime.fromisoformat(borrow_info["due_date"])
                due_date_str = due_date.strftime("%Y-%m-%d")
                
                # Check if overdue
                current_date = datetime.now()
                status = "⚠️ Overdue" if current_date > due_date else "📅 On time"
                
                print(f"{book_id:<8} {book['title']:<30} {user['name']:<20} {due_date_str:<15} {status}")

    def generate_report(self) -> None:
        """Generate a mini report of library statistics."""
        print("\n" + "="*60)
        print("LIBRARY REPORT")
        print("="*60)
        
        total_books = len(self.books)
        available_books = sum(1 for book in self.books.values() if book["availability"])
        borrowed_books = total_books - available_books
        total_users = len(self.users)
        
        print(f"📊 Library Statistics:")
        print(f"   Total Books: {total_books}")
        print(f"   Available Books: {available_books}")
        print(f"   Borrowed Books: {borrowed_books}")
        print(f"   Total Users: {total_users}")
        
        # Top borrowed books
        if self.borrowed_books:
            print(f"\n📈 Borrowing Activity:")
            borrow_counts = {}
            for book_id, borrow_info in self.borrowed_books.items():
                if book_id in self.books:
                    book_title = self.books[book_id]["title"]
                    borrow_counts[book_title] = borrow_counts.get(book_title, 0) + 1
            
            if borrow_counts:
                sorted_books = sorted(borrow_counts.items(), key=lambda x: x[1], reverse=True)
                print("   Top Borrowed Books:")
                for i, (title, count) in enumerate(sorted_books[:5], 1):
                    print(f"   {i}. {title} ({count} times)")
        
        # Overdue books
        overdue_count = 0
        total_late_fees = 0
        current_date = datetime.now()
        
        for book_id, borrow_info in self.borrowed_books.items():
            if not borrow_info["returned"]:
                due_date = datetime.fromisoformat(borrow_info["due_date"])
                if current_date > due_date:
                    overdue_count += 1
                    late_fee = self.calculate_late_fee(book_id)
                    total_late_fees += late_fee
        
        if overdue_count > 0:
            print(f"\n⚠️ Overdue Books: {overdue_count}")
            print(f"💰 Total Late Fees: ₹{total_late_fees}")
        else:
            print(f"\n✅ No overdue books!")

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*60)
        print("📚 LIBRARY MANAGEMENT SYSTEM")
        print("="*60)
        print("1.  Add New Book")
        print("2.  View All Books")
        print("3.  Search Books")
        print("4.  Register User")
        print("5.  Borrow Book")
        print("6.  Return Book")
        print("7.  Delete Book")
        print("8.  Delete User")
        print("9.  View Borrowed Books")
        print("10. Generate Report")
        print("11. Exit Program")
        print("="*60)

    def run(self) -> None:
        """Run the main program loop."""
        print("🎉 Welcome to Library Management System!")
        print("📖 Managing books and users made easy!")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-11): ").strip()
                
                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.view_all_books()
                elif choice == "3":
                    self.search_books()
                elif choice == "4":
                    self.register_user()
                elif choice == "5":
                    self.borrow_book()
                elif choice == "6":
                    self.return_book()
                elif choice == "7":
                    self.delete_book()
                elif choice == "8":
                    self.delete_user()
                elif choice == "9":
                    self.view_borrowed_books()
                elif choice == "10":
                    self.generate_report()
                elif choice == "11":
                    print("\n👋 Thank you for using Library Management System!")
                    print("📚 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice! Please enter a number between 1-11.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Program interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Main function to start the program."""
    try:
        library = LibraryManagementSystem()
        library.run()
    except Exception as e:
        print(f"❌ Failed to start Library Management System: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
