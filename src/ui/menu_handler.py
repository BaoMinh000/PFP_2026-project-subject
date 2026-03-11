from time import sleep, time
from src.services.file_io import load_from_file
from src.configs.config import DATA_BOOKS_FILE
from src.models import book
from src.utils.util import clear_screen
from src.services.book import add_book, list_most_borrowed_books, return_book, sort_books, update_book, delete_book, display_books, search_books, update_book, borrow_book
from src.ui.menu import show_statistics_menu
from src.configs.config import DATA_BOOKS_FILE

def handle_menu_choice(choice, books):
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
        condition = input("Enter the title to sort by: ")
        sort_books(books, condition, "asc")
    
    elif choice == "9":
        # Statistics & Reports
        show_statistics_menu()

        sub_choice = input("Choose an option: ")

        if sub_choice == "1":
            list_most_borrowed_books(books)
        elif sub_choice == "2": # thống kê tổng số lượng sách trong thư viện
            total_number_of_books = len(books)
            print(f"Total number of books: {total_number_of_books}")
        elif sub_choice == "3": # thống kê số lượng sách đang được mượn (borrowed) trong thư viện - không có sẵn để mượn
            total_borrowed_books = 0
            for book in books:
                if not book.is_available:
                    total_borrowed_books += 1
            print(f"Total borrowed books: {total_borrowed_books}")
        elif sub_choice == "4": # thống kê số lượng sách hiện có (available) trong thư viện - có thể mượn được
            total_available_books = 0
            for book in books:
                if book.is_available:
                    total_available_books += 1
            print(f"Total available books: {total_available_books}")
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
