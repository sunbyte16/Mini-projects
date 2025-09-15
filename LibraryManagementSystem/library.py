from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity
        self.available = quantity
        self.borrowers = {}

class Library:
    def __init__(self):
        self.books = {}
        self.book_counter = 1
    
    def add_book(self, title, author, quantity):
        book_id = f"B{self.book_counter:03d}"
        self.books[book_id] = Book(book_id, title, author, quantity)
        self.book_counter += 1
        return book_id
    
    def display_books(self):
        if not self.books:
            print("\nNo books in the library!")
            return
            
        print("\n{:<8} {:<30} {:<25} {:<10} {:<10}".format(
            "ID", "Title", "Author", "Available", "Total"))
        print("-" * 83)
        
        for book_id, book in self.books.items():
            print("{:<8} {:<30} {:<25} {:<10} {:<10}".format(
                book_id, book.title[:28] + '...' if len(book.title) > 28 else book.title,
                book.author[:22] + '...' if len(book.author) > 22 else book.author,
                book.available, book.quantity))
    
    def issue_book(self, book_id, borrower_name):
        if book_id not in self.books:
            return "Book not found!"
            
        book = self.books[book_id]
        
        if book.available <= 0:
            return "No copies available for issue!"
            
        if borrower_name in book.borrowers:
            return "You have already borrowed this book!"
            
        due_date = datetime.now() + timedelta(days=14)  # 2 weeks from now
        book.borrowers[borrower_name] = due_date
        book.available -= 1
        
        return f"Book issued successfully! Due date: {due_date.strftime('%Y-%m-%d')}"
    
    def return_book(self, book_id, borrower_name):
        if book_id not in self.books:
            return "Book not found!"
            
        book = self.books[book_id]
        
        if borrower_name not in book.borrowers:
            return "You haven't borrowed this book!"
            
        del book.borrowers[borrower_name]
        book.available += 1
        
        return "Book returned successfully!"
    
    def search_book(self, query):
        results = []
        query = query.lower()
        
        for book_id, book in self.books.items():
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query == book_id.lower()):
                results.append(book)
        
        if not results:
            print("\nNo books found matching your search!")
            return
            
        print("\nSearch Results:")
        print("{:<8} {:<30} {:<25} {:<10}".format(
            "ID", "Title", "Author", "Available"))
        print("-" * 73)
        
        for book in results:
            print("{:<8} {:<30} {:<25} {:<10}".format(
                book.book_id, 
                book.title[:28] + '...' if len(book.title) > 28 else book.title,
                book.author[:22] + '...' if len(book.author) > 22 else book.author,
                book.available))

def main():
    library = Library()
    
    # Add some sample books
    library.add_book("Python Programming", "John Smith", 5)
    library.add_book("Introduction to Algorithms", "Thomas Cormen", 3)
    library.add_book("Clean Code", "Robert Martin", 4)
    
    while True:
        print("\n=== Library Management System ===")
        print("1. Add New Book")
        print("2. Display All Books")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            title = input("\nEnter book title: ")
            author = input("Enter author name: ")
            try:
                quantity = int(input("Enter quantity: "))
                if quantity > 0:
                    book_id = library.add_book(title, author, quantity)
                    print(f"\nBook added successfully! Book ID: {book_id}")
                else:
                    print("\nQuantity must be greater than 0!")
            except ValueError:
                print("\nPlease enter a valid number!")
                
        elif choice == '2':
            library.display_books()
            
        elif choice == '3':
            query = input("\nEnter book title, author, or ID to search: ")
            library.search_book(query)
            
        elif choice == '4':
            library.display_books()
            book_id = input("\nEnter book ID to issue: ")
            borrower = input("Enter your name: ")
            result = library.issue_book(book_id, borrower)
            print(f"\n{result}")
            
        elif choice == '5':
            book_id = input("\nEnter book ID to return: ")
            borrower = input("Enter your name: ")
            result = library.return_book(book_id, borrower)
            print(f"\n{result}")
            
        elif choice == '6':
            print("\nThank you for using Library Management System!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()
