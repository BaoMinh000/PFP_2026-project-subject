# ---------- Imports ----------
from src.services.book import sort_books
from src.ui.menu_handler import handle_menu_choice
from src.ui.menu import show_menu
from src.configs.config import DATA_BOOKS_FILE
from src.services.file_io import load_from_file, save_to_file
# Import necessary modules


# ---------- Data Structure ----------
data_books = DATA_BOOKS_FILE
# ---------- GPA Calculation ----------
# logger.info("Program started")
def main():
    try:
        books = load_from_file(data_books)
        books = sort_books(books,"id","asc")

        # save_to_file(books, DATA_BOOKS_FILE)
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        books = []
    for book in books:
        print(book)
    print("Welcome to the Book Management System!")
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if not handle_menu_choice(choice=choice, books = books):
            break
# ---------- Program Entry Point ----------
if __name__ == "__main__":
    main()
    

