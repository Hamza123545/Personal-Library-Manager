import streamlit as st
import os

# File to save/load library data
LIBRARY_FILE = "library.txt"

# Initialize session state for the library
if "library" not in st.session_state:
    st.session_state.library = []
    st.session_state.library_loaded = False  # Track if library is loaded

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stRadio div {
        flex-direction: row;
        gap: 10px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

def add_book():
    """Add a book to the library."""
    st.subheader("📖 Add a Book")
    with st.form("add_book_form"):
        title = st.text_input("Title", placeholder="Enter the book title")
        author = st.text_input("Author", placeholder="Enter the author's name")
        year = st.number_input("Publication Year", min_value=0, max_value=9999, step=1, value=2023)
        genre = st.text_input("Genre", placeholder="Enter the genre")
        read_status = st.radio("Have you read this book?", ("Yes", "No"), index=1)
        
        if st.form_submit_button("Add Book"):
            if title and author and genre:
                book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read_status": read_status == "Yes"
                }
                st.session_state.library.append(book)
                st.success("✅ Book added successfully!")
            else:
                st.error("❌ Please fill in all fields.")

def remove_book():
    """Remove a book from the library by title."""
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter the title of the book to remove", placeholder="Enter the book title")
    
    if st.button("Remove Book"):
        if title:
            for book in st.session_state.library:
                if book["title"].lower() == title.lower():
                    st.session_state.library.remove(book)
                    st.success(f"✅ '{title}' removed successfully!")
                    return
            st.error(f"❌ '{title}' not found in the library.")
        else:
            st.error("❌ Please enter a title.")

def search_book():
    """Search for a book by title or author."""
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by:", ("Title", "Author"))
    search_term = st.text_input(f"Enter the {search_by.lower()}", placeholder=f"Enter the {search_by.lower()}")
    
    if st.button("Search"):
        if search_term:
            matching_books = []
            for book in st.session_state.library:
                if search_by == "Title" and search_term.lower() in book["title"].lower():
                    matching_books.append(book)
                elif search_by == "Author" and search_term.lower() in book["author"].lower():
                    matching_books.append(book)
            
            if matching_books:
                st.write("📚 Matching Books:")
                for i, book in enumerate(matching_books, start=1):
                    status = "✅ Read" if book["read_status"] else "❌ Unread"
                    st.write(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
            else:
                st.write("❌ No matching books found.")
        else:
            st.error("❌ Please enter a search term.")

def display_all_books():
    """Display all books in the library."""
    st.subheader("📚 Your Library")
    if not st.session_state.library:
        st.write("No books in the library.")
        return
    
    for i, book in enumerate(st.session_state.library, start=1):
        status = "✅ Read" if book["read_status"] else "❌ Unread"
        st.write(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics():
    """Display library statistics."""
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    if total_books == 0:
        st.write("No books in the library.")
        return
    
    read_books = sum(book["read_status"] for book in st.session_state.library)
    percentage_read = (read_books / total_books) * 100
    
    st.write(f"📖 **Total books:** {total_books}")
    st.write(f"📈 **Percentage read:** {percentage_read:.1f}%")

def save_library():
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        for book in st.session_state.library:
            file.write(f"{book['title']},{book['author']},{book['year']},{book['genre']},{book['read_status']}\n")
    st.success("✅ Library saved to file.")

def load_library():
    """Load the library from a file."""
    if not os.path.exists(LIBRARY_FILE):
        st.info("No library file found. Starting with an empty library.")
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
                            st.session_state.library.append(book)
                        else:
                            st.warning(f"Skipping invalid line in library file: {line}")
                    except ValueError:
                        st.warning(f"Skipping invalid line in library file: {line}")
        st.success("✅ Library loaded from file.")
    except Exception as e:
        st.error(f"❌ Error loading library: {e}")

def main():
    """Main function to run the Streamlit app."""
    st.title("📚 Personal Library Manager")
    st.markdown("Welcome to your personal library! Manage your book collection with ease.")
    
    # Load library only once at startup
    if not st.session_state.library_loaded:
        load_library()
        st.session_state.library_loaded = True  # Mark library as loaded
    
    # Sidebar menu
    st.sidebar.title("Menu")
    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Save and Exit"]
    choice = st.sidebar.radio("Choose an option", menu)
    
    if choice == "Add a Book":
        add_book()
    elif choice == "Remove a Book":
        remove_book()
    elif choice == "Search for a Book":
        search_book()
    elif choice == "Display All Books":
        display_all_books()
    elif choice == "Display Statistics":
        display_statistics()
    elif choice == "Save and Exit":
        save_library()
        st.write("👋 Goodbye!")
        st.stop()

if __name__ == "__main__":
    main()