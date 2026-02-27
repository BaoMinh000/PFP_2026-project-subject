# from src.models.student_model import Student
from src.models.book import Book
from src.utils.util import convert_borrowers_to_string, convert_string_to_borrowers

def save_to_file(books, filename):
    print("Saving book data...")
    print("Please wait...")
    
    # try:
    #     with open(filename, 'r') as f:
    #         content = f.read()
    # except FileNotFoundError:
    #     print(f"File {filename} does not exist. Creating new file.")
    # except Exception as e:
    #     print(f"Error saving to file: {e}")
    #     return False
    
    try:
        with open(filename, 'w') as f:
            for book in books:
                if book.borrowers:   # nếu list không rỗng
                    borrowers_str = convert_borrowers_to_string(book.get_borrowers()) # chuyển list borrower (list of dict) thành string để lưu vào file
                else:
                    borrowers_str = "None"  # nếu list rỗng, gán chuỗi rỗng
                    
                # print("Writing book:", book)
                line = (
                    f"{book.book_id},"
                    f"{book.title},"
                    f"{book.author},"
                    f"{book.category},"
                    f"{book._publication_year},"
                    f"{book.is_available},"
                    f"{book.borrow_count},"
                    f"{borrowers_str}\n"
                )                # print("Line to write:", line)
                f.write(line) # write the line to the file
        return True
    except FileNotFoundError:
        print("File not found. Unable to save data.")
        return False
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def load_from_file(filename):
    books = []
    print("Loading book data...")
    print("Please wait...")
    try:
        with open(filename, 'r') as f:
            for line in f:
                data_in_line = line.strip().split(',')
                book_id = data_in_line[0]
                title = data_in_line[1]
                author = data_in_line[2]
                category = data_in_line[3]
                year = data_in_line[4]
                is_available = data_in_line[5].lower() == 'true'
                borrow_count = int(data_in_line[6])
                borrowers = data_in_line[7] if len(data_in_line) > 7 else "None"
                borrowers = convert_string_to_borrowers(borrowers) # chuyển string từ file thành list borrower (list of dict)       
                book = Book(
                    book_id,
                    title,
                    author,
                    category,
                    year,
                    is_available,
                    borrow_count,
                    borrowers  
                )
                books.append(book)
    except FileNotFoundError:
        print("File not found. Starting with an empty book list.")
        books = []
    except Exception as e:
        print(f"Error loading from file: {e}")
    
    return books
 