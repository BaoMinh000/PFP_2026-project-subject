from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIntValidator # Để chỉ cho phép nhập số vào năm

class BookForm(QDialog):
    def __init__(self, parent=None, book_data=None):
        super().__init__(parent)
        if book_data:
            self.setWindowTitle("Cập nhật thông tin sách")
            self.fill_data(book_data)
        else:
            self.setWindowTitle("Thêm sách mới")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()

        # Tạo các ô nhập liệu
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.category_input = QLineEdit()
        
        # Ô nhập năm chỉ cho phép nhập số
        self.year_input = QLineEdit()
        self.year_input.setValidator(QIntValidator(1000, 2026)) 
        self.year_input.setPlaceholderText("Ví dụ: 2024")

        # Thêm vào hàng
        layout.addRow("Tiêu đề sách:", self.title_input)
        layout.addRow("Tác giả:", self.author_input)
        layout.addRow("Thể loại:", self.category_input)
        layout.addRow("Năm xuất bản:", self.year_input)

        self.save_btn = QPushButton("Lưu Sách")
        self.save_btn.setStyleSheet("background-color: #2ecc71; color: white; height: 30px; font-weight: bold;")
        
        # Layout tổng
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.save_btn)
        self.setLayout(main_layout)

    def get_inputs(self):
        """Lấy dữ liệu từ các ô nhập"""
        return {
            "title": self.title_input.text().strip(),
            "author": self.author_input.text().strip(),
            "category": self.category_input.text().strip(),
            "year": self.year_input.text().strip()
        }
    def fill_data(self, book):
        """Đổ dữ liệu cũ vào form khi cần sửa"""
        self.title_input.setText(book.title)
        self.author_input.setText(book.author)
        self.category_input.setText(book.category)
        self.year_input.setText(str(book._publication_year))