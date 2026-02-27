class Book:
    def __init__(self, book_id, title, author, category, publication_year,
                 is_available=True, borrow_count=0, borrowers=None):

        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self._publication_year = publication_year
        self._is_available = is_available
        self.borrow_count = borrow_count
        self.borrowers  = borrowers if borrowers is not None else []   # None nếu chưa ai mượn
        
    @property
    def is_available(self):
        return self._is_available
    
    def borrow(self, borrower_info):
        if self._is_available:
            self._is_available = False
            self.borrow_count += 1
            if self.borrowers is None:
                self.borrowers = []
            self.borrowers.append(borrower_info)
            return True
        return False
    
    def get_borrow_count(self):
        return self.borrow_count
    
    def return_book(self, borrower_info):
        if self.borrowers and borrower_info in self.borrowers:
            self.borrowers.remove(borrower_info)
            self._is_available = True
            
            return True
        return False
    
    def get_borrowers(self):
        if self.borrowers:
            return self.borrowers
        return [] 
    
    def __str__(self):
        status = "Available" if self._is_available else "Borrowed"

        # if len(borrower) > 

        return (
            f"Book ID: {self.book_id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Category: {self.category}, "
            f"Year: {self._publication_year}, "
            f"Status: {status}, "
            f"Borrow count: {self.borrow_count}, "
            f"Borrower: {self.get_borrowers()}"
        )
