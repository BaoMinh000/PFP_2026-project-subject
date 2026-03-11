from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class StatisticsView(QDialog):
    def __init__(self, stats, parent=None):
        """
        stats: Một dictionary chứa dữ liệu. 
        Ví dụ: {"total": 100, "borrowed": 20, "available": 80}
        """
        super().__init__(parent)
        self.setWindowTitle("Thống kê Thư viện")
        self.setFixedWidth(350)
        
        layout = QVBoxLayout()
        layout.setSpacing(15) # Khoảng cách giữa các dòng cho thoáng

        # Sử dụng f-string để đưa giá trị từ biến stats vào chữ
        self.total_label = QLabel(f"📊 <b>Tổng số sách:</b> {stats['total']}")
        self.borrowed_label = QLabel(f"📕 <b>Đang cho mượn:</b> {stats['borrowed']}")
        self.available_label = QLabel(f"📗 <b>Sách có sẵn:</b> {stats['available']}")

        # Làm cho chữ to và đẹp hơn một chút bằng CSS
        label_style = "font-size: 14px; color: #2c3e50;"
        for lbl in [self.total_label, self.borrowed_label, self.available_label]:
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)

        self.setLayout(layout)