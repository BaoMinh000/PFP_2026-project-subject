from src.services.file_io import load_from_file
from src.configs.config import DATA_BOOKS_FILE

class BookManager:

    def __init__(self):
        self.books = load_from_file(DATA_BOOKS_FILE)
        
    def get_books(self):
        return self.books
    
    def add_book(self, book):
        self.books.append(book)
    
    def update_book(self, book_id, updated_book):
        for i, book in enumerate(self.books):
            if book.book_id == book_id:
                self.books[i] = updated_book
                return True
        return False
    
    def delete_book(self, book_id):
        for i, book in enumerate(self.books):
            if book.book_id == book_id:
                del self.books[i]
                return True
        return False
    
    def search_books(self, keyword):
        return [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
    
    # def sort_books(self, condition, order="asc"):
    #     reverse = (order == "desc")
    #     if condition == "title":
    #         self.books.sort(key=lambda x: x.title, reverse=reverse)
    #     elif condition == "author":
    #         self.books.sort(key=lambda x: x.author, reverse=reverse)
    #     elif condition == "publication_year":
    #         self.books.sort(key=lambda x: x._publication_year, reverse=reverse)
    #     elif condition == "borrow_count":
    #         self.books.sort(key=lambda x: x.borrow_count, reverse=reverse)
    #     elif condition == "id":
    #         self.books.sort(key=lambda x: x.id, reverse=reverse)
    #     return self.books