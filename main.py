# ---------- Imports ----------
# Import necessary modules
# from src.models.BookManager import BookManager
from src.controllers.main_controller import MainController
# from src.services.book import sort_books
from src.ui.menu_handler import handle_menu_choice
from src.ui.menu import show_menu
from src.configs.config import DATA_BOOKS_FILE
from src.services.file_io import load_from_file

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    # 1. Load dữ liệu từ file trước
    books = load_from_file(DATA_BOOKS_FILE)
    if not books:
        print("No books found. Starting with an empty book list.")
        books = []

    # 2. Hỏi người dùng lựa chọn giao diện
    choice_ui = input("Ban muon su dung giao dien do hoa (UI) không? (y/n): ").strip().lower()

    if choice_ui == "y":
        # --- CHẠY GIAO DIỆN ĐỒ HỌA (UI) ---
        app = QApplication(sys.argv)
        
        # Khởi tạo Window trước
        window = MainWindow(books) 
        
        # Khởi tạo Controller và truyền 'window' thật vào thay vì 'None'
        # Như vậy self.main_window trong Controller mới có thể truy cập vào bảng (table)
        controller = MainController(window, books)
        # kết nối:
        window.table.cellClicked.connect(controller.handle_cell_click)

        # Gọi load_data để đổ dữ liệu lên bảng ngay khi mở
        controller.load_data()

        window.show()
        sys.exit(app.exec())     
    else:
        # --- CHẠY GIAO DIỆN CONSOLE ---
        print("\nWelcome to the Book Management System (Console Mode)!")
        while True:
            show_menu()
            choice = input("Enter your choice: ")
            # Giả sử hàm handle_menu_choice trả về False khi chọn 'Thoát'
            if not handle_menu_choice(choice=choice, books=books):
                print("Goodbye!")
                break
            
            
if __name__ == "__main__":
    main()
    
