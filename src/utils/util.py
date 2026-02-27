import os
import time

def generate_book_id(books):
    # Tạo danh sách chứa tất cả book_id đang được sử dụng
    used_ids = []

    for book in books:
        used_ids.append(int(book.book_id))

    # Bắt đầu kiểm tra từ ID = 1
    new_id = 1
    print(f"Used IDs: {used_ids}")
    # Nếu ID đã tồn tại thì tăng lên cho đến khi tìm được ID trống
    while new_id in used_ids:
        new_id = new_id + 1

    return new_id

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def pause():
    input("Press Enter to continue...")

def get_current_time():
    return time.time()

def short_text_smart(text, width):
    if len(text) <= width:
        return text
    cut = text[:width - 3]
    if ' ' in cut:
        cut = cut.rsplit(' ', 1)[0]
    return cut + "..."

def convert_borrowers_to_string(borrowers): # Chuyển đổi list borrower (list of dict) thành string để lưu vào file
    borrowers_str = ""
    print("Converting borrowers to string...")
    print("Borrowers list:", borrowers)
    if borrowers:   # nếu list không rỗng
    
        temp_list = []   # tạo list tạm
        
        for b in borrowers:   # duyệt từng dictionary
            name = b["name"]       # lấy name
            phone = b["phone"]     # lấy phone
            text = name + "-" + phone   # ghép thành chuỗi
            temp_list.append(text)      # thêm vào list tạm
        
        # Sau khi có list tạm, nối lại bằng |
        borrowers_str = ""
        
        for i in range(len(temp_list)):
            
            borrowers_str += temp_list[i]
            # thêm dấu | nếu chưa phải phần tử cuối
            if i != len(temp_list) - 1:
                borrowers_str += "|"
    return borrowers_str
                  
def convert_string_to_borrowers(borrowers_str): # Chuyển đổi string từ file thành list borrower (list of dict)
    borrowers = []
    # print("Converting string to borrowers...")
    # print("Borrowers string:", borrowers_str)
    if borrowers_str:   # nếu chuỗi không rỗng
        if "|" in borrowers_str:   # nếu có dấu |, nghĩa là có nhiều borrower
            borrower_list = borrowers_str.split("|")   # tách thành list các borrower
        else:   # nếu không có dấu |, nghĩa là chỉ có 1 borrower
            borrower_list = [borrowers_str]   # tạo list chứa 1 phần tử là chuỗi đó
            # print("Single borrower detected, borrower_list:", borrower_list)
        for element in borrower_list:    # duyệt từng phần tử
            # print("Processing element:", element)
            if "-" in element:
                name, phone = element.split("-", 1)   # tách name và phone chỉ tách 1 lần 
                borrower_dict = {"name": name, "phone": phone}   # tạo dict
                # print("Created borrower dict:", borrower_dict)
                borrowers.append(borrower_dict)    # thêm vào list borrowers
    return borrowers