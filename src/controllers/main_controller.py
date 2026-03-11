from PyQt6.QtWidgets import QAbstractItemView, QMessageBox, QTableWidgetItem
from src.models.book import Book
from src.services.file_io import save_to_file
from src.services.book import get_book_by_id
from src.ui.book_form import BookForm
from src.ui.statistics_view import StatisticsView
from src.utils.util import get_html_template
# from src.utils.util import convert_borrowers_to_string
from src.configs.config import DATA_BOOKS_FILE
from src.ui.search_form import SearchForm
from src.ui.sort_form import SortForm
class MainController:
    def __init__(self, main_window, books):
        self.main_window = main_window
        self.books = books

    def open_add_form(self):
        # Tạo form
        book_form = BookForm(self.main_window)
        # Kết nối nút Save của form với hàm lưu dữ liệu trong Controller
        book_form.save_btn.clicked.connect(lambda: self.save_book(book_form))

        # Hiển thị form dưới dạng cửa sổ chờ (Modal)
        book_form.exec()
    
    def open_statistics(self):
        # 1. Tính toán số liệu thực tế từ danh sách books
        total = len(self.books)
        borrowed = sum(1 for b in self.books if not b.is_available)
        available = total - borrowed

        # 2. Đóng gói thành dictionary
        stats_data = {
            "total": total,
            "borrowed": borrowed,
            "available": available
        }

        # 3. Khởi tạo form và truyền dữ liệu vào
        stats_dialog = StatisticsView(stats_data, self.main_window)
        
        # 4. Hiển thị
        stats_dialog.exec()
        
    def open_update_form(self):
        if self.main_window.table.currentRow() < 0:
            QMessageBox.warning(self.main_window, "Thông báo", "Vui lòng chọn một sách để cập nhật!")
            return
        form = BookForm(self.main_window, book_data=self.get_book_from_row(self.main_window.table.currentRow()))
        form.exec()
        
    def delete_book(self):
        #1. Kiểm tra xem người dùng đã chọn hàng nào chưa
        row = self.main_window.table.currentRow()
        
        if row < 0:
            QMessageBox.warning(self.main_window, "Thông báo", "Vui lòng chọn một sách để xóa!")
            return
        #2. Lấy đối tượng Book từ hàng đã chọn
        book = self.get_book_from_row(row)
        
        if not book:
            QMessageBox.warning(self.main_window, "Thông báo", "Không tìm thấy sách đã chọn!")
            return
        # 3. Kiểm tra logic nghiệp vụ (Không cho xóa nếu sách đang được mượn)
        if not book.is_available:
            QMessageBox.warning(self.main_window, "Thông báo", "Không thể xóa sách đang được mượn!")
            return
        
        # 4. Xác nhận với người dùng trước khi xóa
        reply = QMessageBox.question(self.main_window, "Xác nhận", f"Bạn có chắc muốn xóa sách '{book.title}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 5. Thực hiện xóa sách khỏi danh sách
                self.books.remove(book)
                
                # 6. Lưu lại dữ liệu sau khi xóa
                if save_to_file(self.books, DATA_BOOKS_FILE):
                    QMessageBox.information(self.main_window, "Thành công", f"Đã xóa sách '{book.title}' thành công!")
                    self.load_data() # Cập nhật lại bảng sau khi xóa
                else:
                    QMessageBox.critical(self.main_window, "Lỗi", "Không thể lưu dữ liệu sau khi xóa!")
            except Exception as e:
                QMessageBox.critical(self.main_window, "Lỗi hệ thống", f"Có lỗi xảy ra: {str(e)}")
        else:
            QMessageBox.information(self.main_window, "Hủy bỏ", "Đã hủy bỏ thao tác xóa.")

    
    def open_search_books_form(self):
        # 1. Mở Search Form
        form = SearchForm(self.main_window)
        if form.exec(): # Nếu người dùng bấm nút "Tìm kiếm"
            criteria = form.get_criteria() # Lấy tiêu chí tìm kiếm từ form
            
            # 2. Thực hiện tìm kiếm dựa trên tiêu chí
            # Nếu tất cả để trống thì hiện lại toàn bộ sách
            if not any(criteria.values()):
                self.load_data()
                return
            # Lọc sách dựa trên tiêu chí (có thể có nhiều tiêu chí cùng lúc, nên lọc dần dần)
            results = self.books   
            if criteria["title"]:
                results = [b for b in results if criteria["title"] in b.title.lower()]
            if criteria["author"]:
                results = [b for b in results if criteria["author"] in b.author.lower()]
            if criteria["category"]:
                results = [b for b in results if criteria["category"] in b.category.lower()]   
            
            # 3. Hiển thị kết quả lên bảng (có thể tái sử dụng hàm load_data nhưng với danh sách đã lọc)
            self.main_window.table.setRowCount(0)
            self.main_window.table.setRowCount(len(results))
            # Duyệt qua danh sách kết quả và hiển thị lên bảng
            for row, book in enumerate(results): 
                id_item = QTableWidgetItem(str(book.book_id))
                self.main_window.table.setItem(row, 0, id_item)
                self.main_window.table.setItem(row, 1, QTableWidgetItem(book.title))
                self.main_window.table.setItem(row, 2, QTableWidgetItem(book.author))
                self.main_window.table.setItem(row, 3, QTableWidgetItem(book.category))
                self.main_window.table.setItem(row, 4, QTableWidgetItem(str(book._publication_year)))
                self.main_window.table.setItem(row, 5, QTableWidgetItem("Yes" if book.is_available else "No"))
                self.main_window.table.setItem(row, 6, QTableWidgetItem(str(book.borrow_count)))
            # Lệnh ẩn cột ID
            self.main_window.table.setColumnHidden(0, True)
    
    def open_sort_form(self):
        form = SortForm(self.main_window)
        
        if form.exec():
            data = form.get_sort_data()
            idx = data["criteria_index"] # 0: Title, 1: Author, 2: Year, 3: Borrow Count
            reverse = data["is_reverse"] # True nếu chọn giảm dần, False nếu chọn tăng dần

            # Ánh xạ từ lựa chọn giao diện sang thuộc tính của đối tượng Book
            # 0: Title, 1: Author, 2: Year, 3: Borrow Count
            sort_keys = [
                lambda b: b.title.lower(),
                lambda b: b.author.lower(),
                lambda b: b._publication_year,
                lambda b: b.borrow_count
            ]

            # Thực hiện sắp xếp danh sách gốc trong bộ nhớ
            self.books.sort(key=sort_keys[idx], reverse=reverse)
            for book in self.books:
                print(f"ID: {book.book_id} | Title: {book.title} | Available: {book.is_available}")
            # Cập nhật lại bảng và thông báo
            self.load_data()
            self.main_window.status_bar.showMessage("Đã sắp xếp danh sách sách.")
    
    def save_book(self, form):
        data = form.get_inputs() # Lấy dữ liệu từ form dưới dạng dict với keys: title, author, category, year

        # 1. Kiểm tra dữ liệu trống (giống logic 'if title and author...' của bạn)
        if not all([data["title"], data["author"], data["category"], data["year"]]):
            QMessageBox.warning(form, "Thông báo", "Tất cả các trường đều bắt buộc!")
            return

        # 2. Tạo ID tự động (giống logic console)
        from src.services.book import generate_book_id
        book_id = generate_book_id(self.books)

        # 3. Tạo đối tượng Book mới 
        # (ID, Title, Author, Category, Year, is_available=True, borrow_count=0, borrowers=None)
        try:
            new_book = Book(
                book_id=book_id,
                title=data["title"],
                author=data["author"],
                category=data["category"],
                publication_year=int(data["year"]),
                is_available=True,
                borrow_count=0,
                borrowers=None
            )

            # 4. Thêm vào danh sách bộ nhớ
            self.books.append(new_book)

            # 5. Lưu vào file (DATA_BOOKS_FILE)
            if save_to_file(self.books, DATA_BOOKS_FILE):
                QMessageBox.information(form, "Thành công", f"Đã thêm sách '{data['title']}' thành công!")
                self.load_data() # Cập nhật bảng trên màn hình chính
                form.accept()    # Đóng form
            else:
                QMessageBox.critical(form, "Lỗi", "Không thể lưu dữ liệu vào file!")
        
        except Exception as e:
            QMessageBox.critical(form, "Lỗi hệ thống", f"Có lỗi xảy ra: {str(e)}")
    
    def load_data(self, books = None):
        if books is None:
            books = self.books
        self.main_window.table.setRowCount(0)
        self.main_window.table.setRowCount(len(books))
        
        for row, book in enumerate(books):
            # Cột 0: ID (Sẽ ẩn)
            self.main_window.table.setItem(row, 0, QTableWidgetItem(str(book.book_id)))
            # Cột 1: Title
            self.main_window.table.setItem(row, 1, QTableWidgetItem(book.title))
            # Cột 2: Author
            self.main_window.table.setItem(row, 2, QTableWidgetItem(book.author))
            # Cột 3: Category
            self.main_window.table.setItem(row, 3, QTableWidgetItem(book.category))
            # Cột 4: Year
            self.main_window.table.setItem(row, 4, QTableWidgetItem(str(book._publication_year)))
            # Cột 5: Status
            self.main_window.table.setItem(row, 5, QTableWidgetItem("Yes" if book.is_available else "No"))
            # Cột 6: Borrows
            self.main_window.table.setItem(row, 6, QTableWidgetItem(str(book.borrow_count)))

        # Sau khi đổ xong 7 cột, ẩn cột 0 đi
        self.main_window.table.setColumnHidden(0, True)
            
    def get_book_from_row(self, row):
        """Bước 1: Lấy đối tượng Book từ vị trí hàng trên bảng"""
        try:
            # Lấy ID từ cột 0 của bảng
            book_id = self.main_window.table.item(row, 0).text()
            
            # Tìm đối tượng book trong danh sách dựa vào ID
            # (Sử dụng hàm get_book_by_id đã có để tìm kiếm nhanh hơn thay vì duyệt vòng for)
            return get_book_by_id(self.books, book_id)
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu hàng: {e}")
            return None  
        
    def render_book_details(self, book):
        """Bước 2: Hiển thị dữ liệu của đối tượng Book lên nhãn chi tiết"""
        if not book:
            return

        # Chuẩn bị dữ liệu hiển thị
        status_color = "#27ae60" if book.is_available else "#e74c3c"
        status_text = "Sẵn sàng" if book.is_available else "Đã mượn"

        # Lấy template và điền dữ liệu
        details = get_html_template("book_detail.html")
        
        formatted_html = details.format(
            title=book.title,
            author=book.author,
            category=book.category,
            year=book._publication_year,
            status_text=status_text,
            status_color=status_color,
            borrow_count=book.borrow_count
        )

        # Cập nhật giao diện
        self.main_window.info_label.setText(formatted_html)      
        
    def handle_cell_click(self, row, col):
        """Bước 3: Hàm tổng hợp xử lý sự kiện click"""
        # 1. Gọi hàm lấy dữ liệu
        book = self.get_book_from_row(row)
        
        # 2. Nếu tìm thấy sách, gọi hàm hiển thị
        if book:
            self.render_book_details(book)