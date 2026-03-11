from email import header
from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QHeaderView, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolBar, QLabel, QStatusBar
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt
from src.ui.book_form import BookForm
from src.ui.statistics_view import StatisticsView
from src.controllers.main_controller import MainController
class MainWindow(QMainWindow):
    def __init__(self, books):
        super().__init__()
        self.books = books
        self.setWindowTitle("Library Management System")
        self.setGeometry(200, 100, 800, 600)
        self.controller = MainController(self,books)
        self.book_form = BookForm(self)
        # Toolbar
        self.setup_actions()
        # Thiết lập giao diện
        self.setup_ui()
        


    def setup_ui(self):
        """Thiết lập bố cục tổng thể"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Thiết lập Style chung cho cả cửa sổ
        self.apply_global_styles()

        # Khởi tạo Layout chính (Hộp ngang)
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15) # Khoảng cách giữa bảng và panel
        central_widget.setLayout(self.main_layout)

        # --- TÁCH THÀNH 2 PHẦN ---
        self.init_left_column()  # Hàm xử lý bảng bên trái
        self.init_right_column() # Hàm xử lý panel bên phải

        # Thêm Status Bar
        self.setup_status_bar()
        
    def init_left_column(self):
        """Khởi tạo bảng dữ liệu bên trái"""
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category", "Year", "Status", "Borrows"
        ])
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #dcdde1; border-radius: 8px; background-color: white; }
            QTableWidget::item:selected { background-color: #d1e9ff; color: #2f3640; }
            QTableWidget::item:hover { background-color: #f0f7ff; }
        """)
        
        # Cấu hình hành vi của bảng
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Cấu hình độ giãn cột
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Title
            for i in [2, 3, 4, 5, 6]:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        # Thêm bảng vào layout chính với tỷ lệ stretch=3
        self.main_layout.addWidget(self.table, stretch=3)
           
    def init_right_column(self):
        """Khởi tạo panel chi tiết bên phải"""
        self.info_panel = QWidget()
        self.info_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 12px;
            }
        """)
        
        info_layout = QVBoxLayout() # Tạo layout cho panel chi tiết
        self.info_panel.setLayout(info_layout)

        # Tiêu đề nhỏ
        title_mini = QLabel("BOOK INFORMATION")
        title_mini.setStyleSheet("color: #7f8c8d; font-size: 10px; font-weight: bold; border: none;")
        
        # Nhãn hiển thị chi tiết
        self.info_label = QLabel("Please select a book\nfrom the list to view details.")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_label.setStyleSheet("font-size: 13px; color: #2f3640; border: none;")

        # Thêm các thành phần vào layout của panel
        info_layout.addWidget(title_mini)
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()

        # Thêm panel vào layout chính với tỷ lệ stretch=1
        self.main_layout.addWidget(self.info_panel, stretch=1)     
    
    def apply_global_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QTableWidget { background-color: white; border-radius: 8px; }
            QTableWidget::item:selected { background-color: #d1e9ff; color: #2f3640; }
            QHeaderView::section { background-color: #f1f2f6; font-weight: bold; }
        """)

    def setup_status_bar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background-color: white; border-top: 1px solid #dcdde1;")
        self.status_bar.showMessage("System Ready")
    
    def setup_actions(self):
        """Thiết lập Thanh công cụ và các nút bấm điều hướng"""
        # 1. Khởi tạo Toolbar (Chỉ gọi addToolBar một lần duy nhất)
        toolbar = self.addToolBar("Main Toolbar")
        if toolbar is not None:
            toolbar.setMovable(False) # Cố định thanh công cụ để giao diện ổn định
        
            # 2. Định nghĩa style CSS
            toolbar.setStyleSheet("""
            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #dee2e6;
                spacing: 0;       /* Khoảng cách ngang giữa các nút */
                min-height: 60px;    /* Chiều cao tối thiểu của thanh công cụ */
                padding-left: 15px;
            }
            QToolButton {
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 6px 14px;   /* Khoảng cách chữ bên trong nút */
                margin-top: 8px;     /* Đẩy nút cách viền trên Toolbar */
                margin-bottom: 8px;  /* Đẩy nút cách viền dưới Toolbar */
                margin-left: 15px;
                color: #495057;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #e9ecef;
                border-color: #3498db;
                color: #3498db;      /* Đổi màu chữ khi rê chuột cho sinh động */
            }
            QToolButton:pressed {
                background-color: #dee2e6;
            }
            """)

            # 3. Dữ liệu các nút: (Tên nút, Hàm xử lý)
            # actions_data = [
            #     ("➕ Add", self.controller.open_add_form),
            #     ("✏️ Edit", self.controller.open_update_form),
            #     ("🗑️ Delete", self.controller.delete_book),
            #     ("🔍 Search", self.controller.open_search_books_form),
            #     ("🔀 Sort", self.controller.open_sort_form),
            #     ("📊 Statistics", self.controller.open_statistics)
            # ]

            # # 4. Tạo và thêm các Action vào Toolbar
            # for text, slot in actions_data:
            #     action_item = QAction(text, self)
            #     action_item.triggered.connect(slot)
            #     toolbar.addAction(action_item)
            # --- 1. Nút ADD ---
            self.add_action = QAction("➕ Add", self)
            self.add_action.triggered.connect(self.controller.open_add_form)
            toolbar.addAction(self.add_action)

            # --- 2. Nút EDIT ---
            self.edit_action = QAction("✏️ Edit", self)
            self.edit_action.triggered.connect(self.controller.open_update_form)
            toolbar.addAction(self.edit_action)

            # --- 3. Nút DELETE ---
            self.delete_action = QAction("🗑️ Delete", self)
            self.delete_action.triggered.connect(self.controller.delete_book)
            toolbar.addAction(self.delete_action)

            # --- 4. Nút SEARCH ---
            self.search_action = QAction("🔍 Search", self)
            self.search_action.triggered.connect(self.controller.open_search_books_form)
            toolbar.addAction(self.search_action)

            # --- 5. Nút SORT ---
            self.sort_action = QAction("🔀 Sort", self)
            self.sort_action.triggered.connect(self.controller.open_sort_form)
            toolbar.addAction(self.sort_action)

            # --- 6. Nút STATISTICS ---
            self.stats_action = QAction("📊 Statistics", self)
            self.stats_action.triggered.connect(self.controller.open_statistics)
            toolbar.addAction(self.stats_action)