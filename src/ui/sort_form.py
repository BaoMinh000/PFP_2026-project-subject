from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QPushButton, QVBoxLayout, QLabel

class SortForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sắp xếp sách")
        self.setFixedWidth(300)
        
        layout = QFormLayout()

        # 1. Chọn tiêu chí sắp xếp
        self.criteria_combo = QComboBox()
        self.criteria_combo.addItems([
            "Tiêu đề (Title)", 
            "Tác giả (Author)", 
            "Năm xuất bản (Year)", 
            "Số lần mượn (Borrow Count)"
        ])

        # 2. Chọn thứ tự
        self.order_combo = QComboBox()
        self.order_combo.addItems(["Tăng dần (A-Z, 0-9)", "Giảm dần (Z-A, 9-0)"])

        layout.addRow("Sắp xếp theo:", self.criteria_combo)
        layout.addRow("Thứ tự:", self.order_combo)

        self.sort_btn = QPushButton("Áp dụng")
        self.sort_btn.setStyleSheet("background-color: #f1c40f; color: black; font-weight: bold; padding: 8px;")
        self.sort_btn.clicked.connect(self.accept)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.sort_btn)
        self.setLayout(main_layout)

    def get_sort_data(self):
        # Trả về index của lựa chọn để dễ xử lý trong Controller
        return {
            "criteria_index": self.criteria_combo.currentIndex(),
            "is_reverse": self.order_combo.currentIndex() == 1
        }