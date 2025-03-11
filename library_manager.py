import os

# File to save/load library data
LIBRARY_FILE = "library.txt"

# Initialize the library
library = []

def add_book():
    """Add a book to the library."""
    print("\n📖 Add a Book")
    title = input("Enter the book title: ")
    author = input("Enter the author's name: ")
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ")
    read_status = input("Have you read this book? (Yes/No): ").strip().lower() == "yes"
    
    if title and author and genre:
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read_status": read_status
        }
        library.append(book)
        print("✅ Book added successfully!")
    else:
        print("❌ Please fill in all fields.")

def remove_book():
    """Remove a book from the library by title."""
    print("\n❌ Remove a Book")
    title = input("Enter the title of the book to remove: ")
    
    if title:
        for book in library:
            if book["title"].lower() == title.lower():
                library.remove(book)
                print(f"✅ '{title}' removed successfully!")
                return
        print(f"❌ '{title}' not found in the library.")
    else:
        print("❌ Please enter a title.")

def search_book():
    """Search for a book by title or author."""
    print("\n🔍 Search for a Book")
    search_by = input("Search by (Title/Author): ").strip().lower()
    search_term = input(f"Enter the {search_by}: ").strip().lower()
    
    if search_term:
        matching_books = []
        for book in library:
            if search_by == "title" and search_term in book["title"].lower():
                matching_books.append(book)
            elif search_by == "author" and search_term in book["author"].lower():
                matching_books.append(book)
        
        if matching_books:
            print("📚 Matching Books:")
            for i, book in enumerate(matching_books, start=1):
                status = "✅ Read" if book["read_status"] else "❌ Unread"
                print(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            print("❌ No matching books found.")
    else:
        print("❌ Please enter a search term.")

def display_all_books():
    """Display all books in the library."""
    print("\n📚 Your Library")
    if not library:
        print("No books in the library.")
        return
    
    for i, book in enumerate(library, start=1):
        status = "✅ Read" if book["read_status"] else "❌ Unread"
        print(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics():
    """Display library statistics."""
    print("\n📊 Library Statistics")
    total_books = len(library)
    if total_books == 0:
        print("No books in the library.")
        return
    
    read_books = sum(book["read_status"] for book in library)
    percentage_read = (read_books / total_books) * 100
    
    print(f"📖 **Total books:** {total_books}")
    print(f"📈 **Percentage read:** {percentage_read:.1f}%")

def save_library():
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        for book in library:
            file.write(f"{book['title']},{book['author']},{book['year']},{book['genre']},{book['read_status']}\n")
    print("✅ Library saved to file.")

def load_library():
    """Load the library from a file."""
    if not os.path.exists(LIBRARY_FILE):
        print("No library file found. Starting with an empty library.")
        return
    
    try:
        with open(LIBRARY_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        # Split the line into exactly 5 parts
                        parts = line.split(",")
                        if len(parts) == 5:
                            title, author, year, genre, read_status = parts
                            book = {
                                "title": title,
                                "author": author,
                                "year": int(year),
                                "genre": genre,
                                "read_status": read_status == "True"
                            }
                            library.append(book)
                        else:
                            print(f"⚠️ Skipping invalid line in library file: {line}")
                    except ValueError:
                        print(f"⚠️ Skipping invalid line in library file: {line}")
        print("✅ Library loaded from file.")
    except Exception as e:
        print(f"❌ Error loading library: {e}")

def main():
    """Main function to run the console-based app."""
    print("📚 Personal Library Manager")
    print("Welcome to your personal library! Manage your book collection with ease.")
    
    # Load library at startup
    load_library()
    
    while True:
        print("\nMenu:")
        print("1. Add a Book")
        print("2. Remove a Book")
        print("3. Search for a Book")
        print("4. Display All Books")
        print("5. Display Statistics")
        print("6. Save and Exit")
        
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_all_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            save_library()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
