# 📚 Hệ thống Quản lý Thư viện (Library Management System)

Dự án xây dựng bằng **Django** (Python) nhằm quản lý sách, độc giả, mượn/trả sách trong thư viện.  
Giao diện thân thiện với **Bootstrap 5**, hỗ trợ đầy đủ các nghiệp vụ cơ bản của một thư viện thực tế.

![Django](https://img.shields.io/badge/Django-4.2-green)  ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)

---

## ✨ Tính năng chính

### 🧑‍🎓 Dành cho Độc giả
- Đăng ký / Đăng nhập tài khoản.
- Xem danh sách sách, tìm kiếm theo tên, tác giả, thể loại.
- Xem chi tiết từng cuốn sách (vị trí kệ, số lượng còn).
- **Mượn sách**: Hệ thống tự kiểm tra thẻ thư viện (hạn, trạng thái), loại sách đặc biệt, tài liệu số.
- Xem **lịch sử mượn / trả** cá nhân.
- **Trả sách** (kèm tính phí trễ hạn tự động).
- Tự động gia hạn thẻ khi đăng ký (mặc định 1 năm).

### 👩‍💼 Dành cho Nhân viên / Quản trị viên
- Quản lý toàn bộ dữ liệu qua **Django Admin**:
  - Thể loại, Kệ sách, Sách, Độc giả, Thẻ thư viện, Nhân viên, Phiếu mượn/trả, Phiếu nhập sách.
- (Đang phát triển) Giao diện nhân viên để xử lý mượn/trả tại quầy.

### ⚙️ Nghiệp vụ được xử lý tự động
- Kiểm tra thẻ hợp lệ (hạn, trạng thái).
- Phân quyền mượn sách đặc biệt (chỉ VIP hoặc Giảng viên).
- Tài liệu số chỉ cho mượn Online.
- Tính ngày trả dự kiến theo loại độc giả:
  - Giảng viên: **30 ngày**
  - Sinh viên: **14 ngày**
  - Khách bên ngoài: **7 ngày**
- Phí trễ hạn: **5.000 VND / ngày** (có thể tùy chỉnh trong code).

---

## 🛠 Công nghệ sử dụng

- **Backend**: Django 4.2, Python 3.8+
- **Database**: SQLite (mặc định) – có thể chuyển sang PostgreSQL/MySQL dễ dàng.
- **Frontend**: Bootstrap 5, Font Awesome, HTML/CSS
- **Authentication**: Django built-in User + Model `DocGia` mở rộng (OneToOne).

---

## 📂 Cấu trúc thư mục chính
QuanLyThuVien/
├── library_system/ # Thư mục project Django
│ ├── settings.py
│ ├── urls.py
│ └── ...
├── library/ # App chính
│ ├── migrations/ # Các file migration
│ ├── templates/ # Template HTML
│ │ ├── base.html
│ │ ├── registration/ # Đăng nhập, đăng ký
│ │ └── library/ # Các trang chức năng
│ ├── models.py # Định nghĩa 11 bảng dữ liệu
│ ├── views.py # Xử lý logic
│ ├── urls.py # URL của app
│ ├── forms.py # Form đăng ký
│ └── admin.py # Cấu hình Admin
├── manage.py
├── requirements.txt # Danh sách thư viện Python
└── README.md # Hướng dẫn này


---

## 🚀 Hướng dẫn cài đặt và chạy local

> **Yêu cầu**: Máy tính đã cài **Python 3.8 trở lên** và **pip**.  
> (Nếu chưa có, tải Python tại [python.org](https://www.python.org/downloads/))

### 1️⃣ Tải mã nguồn về máy

Mở **Terminal** (trên Linux/macOS) hoặc **Command Prompt / PowerShell** (Windows) và thực hiện:

```bash
git clone https://github.com/your-username/QuanLyThuVien.git
cd QuanLyThuVien

### 2️⃣ Thiết lập môi trường ảo (Virtual Environment)

Việc dùng môi trường ảo giúp dự án của bạn chạy ổn định, không bị xung đột với các thư viện khác trên máy tính.


# ============================================================
# 2️⃣ THIẾT LẬP MÔI TRƯỜNG ẢO (VIRTUAL ENVIRONMENT)
# ============================================================

# --- DÀNH CHO WINDOWS ---
# Bước 1: Tạo môi trường ảo
python -m venv venv
# Bước 2: Kích hoạt môi trường
venv\Scripts\activate


# --- DÀNH CHO MAC OS / LINUX ---
# Bước 1: Tạo môi trường ảo
python3 -m venv venv
# Bước 2: Kích hoạt môi trường
source venv/bin/activate


# ============================================================
# 3️⃣ CÀI ĐẶT THƯ VIỆN & KHỞI TẠO DATABASE
# ============================================================

# Cài đặt các thư viện cần thiết (Django, Pillow,...)
pip install -r requirements.txt

# Tạo cấu trúc bảng dữ liệu
python manage.py makemigrations
python manage.py migrate

# Tạo tài khoản Admin (Thủ thư)
python manage.py createsuperuser

# Khởi động Server
python manage.py runserver



![alt text](image.png)