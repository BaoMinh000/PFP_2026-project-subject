from time import sleep, time
from src.services.file_io import load_from_file
from src.configs.config import DATA_BOOKS_FILE
from src.models import book
from src.utils.util import clear_screen
from src.services.book import add_book, return_book, sort_books, update_book, delete_book, display_books, search_books, update_book, borrow_book
from src.ui.menu import show_statistics_menu
from src.configs.config import DATA_BOOKS_FILE

def handle_menu_choice(choice, books):
    # luôn load dữ liệu mới nhất từ file
    try:
        books = load_from_file(DATA_BOOKS_FILE)
    except FileNotFoundError:
        books = []

    if choice == "1":
        add_book(books)

    elif choice == "2":
        update_book(books)

    elif choice == "3":
        delete_book(books)

    elif choice == "4":
        display_books(books)

    elif choice == "5":
        search_books(books)

    elif choice == "6":
        borrow_book(books)

    elif choice == "7":
        return_book(books)

    elif choice == "8":
        # list_borrowed_books(books)
        pass

    elif choice == "9":
        # Statistics & Reports
        show_statistics_menu()

        sub_choice = input("Choose an option: ")

        if sub_choice == "1":
            # list_most_borrowed_books(books)
            pass
        elif sub_choice == "0":
            return True
        else:
            print("Invalid choice in statistics menu.")

    elif choice == "0":
        print("Goodbye!")
        sleep(1)
        clear_screen()
        return False   # 👉 báo cho main() thoát vòng lặp

    else:
        print("Invalid choice! Try again.")

    return True        # 👉 quay lại menu chính
