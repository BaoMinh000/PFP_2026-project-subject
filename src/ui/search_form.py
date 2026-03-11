from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class SearchForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tìm kiếm sách")
        self.setFixedWidth(320) # Tăng nhẹ độ rộng để note hiển thị đẹp hơn
        
        layout = QFormLayout()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.category_input = QLineEdit()

        layout.addRow("Tiêu đề:", self.title_input)
        layout.addRow("Tác giả:", self.author_input)
        layout.addRow("Thể loại:", self.category_input)

        # --- Dòng ghi chú (Note) ---
        self.note_label = QLabel("💡 <i>Để trống các ô để hiển thị lại toàn bộ sách</i>")
        self.note_label.setStyleSheet("color: #7f8c8d; font-size: 11px; margin-top: 5px;")
        self.note_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Căn giữa dòng note
        self.note_label.setWordWrap(True) # Cho phép xuống dòng nếu text dài hơn chiều rộng form

        self.search_btn = QPushButton("Tìm kiếm")
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                font-weight: bold; 
                padding: 8px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        self.search_btn.clicked.connect(self.accept) 

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        
        # Thêm note vào đây
        main_layout.addWidget(self.note_label) 
        
        main_layout.addWidget(self.search_btn)
        self.setLayout(main_layout)
        
    def get_criteria(self):
        return {
            "title": self.title_input.text().strip().lower(),
            "author": self.author_input.text().strip().lower(),
            "category": self.category_input.text().strip().lower()
        }