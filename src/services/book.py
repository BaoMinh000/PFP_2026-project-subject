from src.services.file_io import save_to_file
from src.models.book import Book 
from src.configs.config import DATA_BOOKS_FILE
from src.utils.util import generate_book_id, short_text_smart

def add_book(books):
    # self.books.append(book)
    print("Adding a new book...")
    print(f"{books}")
    book_id = generate_book_id(books)

    print(f"Empty fields will cancel the adding process.")
    while True:
        title = input("Enter book title: ").strip()
        author = input("Enter book author: ").strip()
        category = input("Enter book category: ").strip()
        publication_year = input("Enter publication year: ").strip()

        if title and author and category and publication_year:
            break
        else:
            cancel = input("Do you want cancel adding book? (y/n): ").strip().lower()
            if cancel == 'y':
                return
            print("All fields are required. Please try again.")

    
    # Create and add the new book
    new_book = Book(book_id, title, author, category, publication_year, True, 0, None)
    books.append(new_book) # add to list in memory, not file yet
    
    # Save to file
    if save_to_file(books, DATA_BOOKS_FILE):
        print("Data saved successfully.")
        print(f"Book '{title}' added successfully with ID {book_id}.")
    else:
        print("Failed to save data.")

def delete_book(books):
    print("Deleting a book...")
    book_id = input("Enter the Book ID to delete: ")
    if book_id.strip() == "":
        print("Book ID cannot be empty.")
        return
    book = get_book_by_id(books, book_id)
    if book:
        
        # Check if the book is currently borrowed
        if book.is_available == False:
            print(f"Cannot delete '{book.title}' as it is currently borrowed.")
            return
        books.remove(book)
        save_to_file(books, DATA_BOOKS_FILE)
        print(f"Book ID {book_id} deleted successfully.")
    else:    
        print(f"Book ID {book_id} not found.")
           
def display_books(books):
    if not books:
        print("No books in the system.")
        return
    
    if books is None:
        return
    
    print("=" * 132)
    print("📚 BOOK LIST".center(125))
    print("=" * 132)


    header = (
        f"| {'ID':<12}"
        f"| {'Title':<24}"
        f"| {'Author':<24}"
        f"| {'Category':<24}"
        f"| {'Year':<10}"
        f"| {'Status':<13}"
        f"| {'Borrowed':<10} |"
        f"| {'Borrower':<20} |"
    )

    line = "+" + "-" * (len(header) - 2) + "+"

    print(line)
    print(header)
    print(line)

    

    for book in books:
        
        # Lấy tên người mượn để hiển thị
        infob =""
        for b in book.get_borrowers():
            infob += f"{b['name']}, "
        
        print(
            f"| {book.book_id:<12}"
            f"| {short_text_smart(book.title, 24):<24}"
            f"| {book.author:<24}"
            f"| {short_text_smart(book.category, 24):<24}"
            f"| {book._publication_year:<10}"
            f"| {'Available' if book.is_available else 'Borrowed':<13}"
            f"| {book.borrow_count:<10} |"
            f"| {infob:<20} |"
        )

    print(line)

def update_book(books):
    print("Updating a book...")
    book_id = input("Enter the Book ID to update: ")
    book = get_book_by_id(books, book_id)
    
    if book:
        # Nhap thong tin can cap nhat
        new_title = input(f"Enter new title (current: {book.title}): ") or book.title
        new_author = input(f"Enter new author (current: {book.author})): ") or book.author
        new_category = input(f"Enter new category (current: {book.category}): ") or book.category
        new_publication_year = input(f"Enter new publication year (current: {book._publication_year}): ") or book._publication_year
        
        book.title = new_title
        book.author = new_author
        book.category = new_category
        book._publication_year = new_publication_year
        save_to_file(books, DATA_BOOKS_FILE)
        print(f"Book ID {book_id} updated successfully.")
    else:
        print(f"Book ID {book_id} not found.")
    
def search_books(books):
    print("Searching for books...")
    print("Enter search criteria (leave blank to skip):")
    print("1. Title/Author/Category keyword")
    title = input("Enter a keyword to search (title): ").strip().lower()
    author = input("Enter a keyword to search (Author): ").strip().lower()
    category = input("Enter a keyword to search (Category): ").strip().lower()
    
    # check if all inputs are empty -> return
    if not title and not author and not category:
        print("No search criteria provided.")
        return

    results = books

    if title:
        print(f"Searching by title containing: {title}")
        new_list = []
        for book in results:
            if title in book.title.lower():
                new_list.append(book)
        results = new_list
    if author:
        print(f"Searching by author containing: {author}")
        new_list = []
        for book in results:
            if author in book.author.lower():
                new_list.append(book)
        results = new_list
    if category:
        print(f"Searching by category containing: {category}")
        new_list = []
        for book in results:
            if category in book.category.lower():
                new_list.append(book)
        results = new_list
    
    if results:
        print(f"Found {len(results)} matching books:")
        display_books(results)
    else:
        print("No matching books found.")
        
def borrow_book(books):
    print("Borrowing a book...")
    
    while True:
        book_id = input("Enter the Book ID to borrow: ").strip()
        book = get_book_by_id(books, book_id)

        if book is not None:
            break   # thoát khi hợp lệ
    
    # Enter borrower info
    borrower_name = input("Enter borrower name: ")
    phone = input("Enter phone number: ")
    borrower_info = {"name": borrower_name, "phone": phone}
    
    # Kiểm tra thông tin hợp lệ và trạng thái sách trước khi mượn
    if book and borrower_name and phone:   
        if borrower_name.strip() == "" or phone.strip() == "":
            print("Borrower name and phone number cannot be empty.")
            return 
        if book.is_available: # nếu sách có thể mượn, thực hiện mượn
            if book.borrow(borrower_info):
                print(f"Borrowed book: {book.title}")
                print("Updating data...")
                print(f"Data {book}")
                save_to_file(books, DATA_BOOKS_FILE)
            else:
                print(f"Failed to borrow book: {book.title}")
                
        else:
            print(f"Sorry, '{book.title}' is currently not available.")
    else:
        print(f"Book ID {book_id} not found, cannot borrow.")
 
def return_book(books):
    print("Returning a book...")
    while True:
        book_id = input("Enter the Book ID to return: ").strip()
        book = get_book_by_id(books, book_id)

        if book is not None:
            break   # thoát khi hợp lệ

    if book: # nếu tìm thấy sách, tiếp tục kiểm tra trạng thái và thực hiện trả
        if not book.is_available: # nếu sách đang được mượn, thực hiện trả
            print(f"Enter borrower information to return the book '{book.title}':")
            
            # Nhập thông tin người trả để xác nhận
            borrower_name = input("Enter borrower name: ").strip()
            phone = input("Enter phone number: ").strip()
            # Kiểm tra thông tin hợp lệ trước khi trả
            if borrower_name == "" or phone == "":
                print("Borrower name and phone number cannot be empty.")
                return
            borrower_info = {"name": borrower_name, "phone": phone}
            
            if book.return_book(borrower_info):
                save_to_file(books, DATA_BOOKS_FILE)
                print(f"You have successfully returned '{book.title}'.")
            else:
                print(f"Failed to return book: {book.title}")
        else:
            print(f"'{book.title}' was not borrowed.")
        return
    else:
        print(f"Book ID {book_id} not found.")
    
def list_borrowed_books(books):
    print("Listing borrowed books...")
    borrowed_books = [book for book in books if not book.is_available]
    if borrowed_books:
        display_books(borrowed_books)
    else:
        print("No books are currently borrowed.")
        
def list_most_borrowed_books(books):
    if not books:
        print("No books in the system.")
        return

    temp_books = books[:]   # copy list

    # sort descending by borrow_count
    for i in range(len(temp_books)):
        for j in range(i + 1, len(temp_books)):
            if temp_books[j].borrow_count > temp_books[i].borrow_count:
                temp_books[i], temp_books[j] = temp_books[j], temp_books[i]

    display_books(temp_books[:5])

def sort_books(books, condition, order):
    sorted_books = books[:]   # copy list
    reverse = (order == "desc")

    if condition == "id":
        sorted_books.sort(key=book_sort_key_id, reverse=reverse)
    elif condition == "author":
        sorted_books.sort(key=book_sort_key_author, reverse=reverse)
    elif condition == "title":
        sorted_books.sort(key=book_sort_key_title, reverse=reverse)
    elif condition == "year":
        sorted_books.sort(key=book_sort_key_year, reverse=reverse)
    else:
        print(f"Invalid sort condition: {condition}. No sorting applied.")
        return None

    return sorted_books


     
def get_book_by_id(books, book_id):
    for book in books:
        if str(book.book_id) == str(book_id):
            return book
    return None
    
def book_sort_key_title(book):
    return book.title.lower()
def book_sort_key_author(book):
    return book.author.lower()
def book_sort_key_year(book):
    return book._publication_year
def book_sort_key_borrow_count(book):
    return book.borrow_count
def book_sort_key_id(book):
    return book.book_id