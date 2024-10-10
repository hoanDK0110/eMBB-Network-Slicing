# eMBB-Network-Slicing
# Hướng dẫn Pull Code và Chạy Dự Án

## 1. Clone Repository

Trước tiên, hãy clone repository này về máy của bạn bằng lệnh sau:

git clone https://github.com/hoanDK0110/eMBB-Network-Slicing.git

## 2. Cấu trúc Thư mục

Thư mục code được chia thành các file, mỗi file sẽ đảm nhiệm một chức năng cụ thể:

- `main.py`: Là nơi chương trình được chạy. Nó sẽ import code từ các file khác.
- `gen_RU_UE.py`: Tạo mô hình không gian của các RU (Radio Units) và UE (User Equipment).
- `wireless.py`: Xử lý các vấn đề liên quan tới phần wireless.
- `RAN_topo.py`: Tạo mô hình mạng.
- `solving.py`: Chạy thuật toán và giải quyết vấn đề.
- `benchmark.py`: Đo đạc thông số sau khi tính toán.
- `result/`: Thư mục này chứa các kết quả sau khi chạy chương trình.

## 3. Cách Chạy Code

- Đảm bảo bạn đã cài đặt tất cả các thư viện cần thiết.
- Mở terminal và điều hướng đến thư mục chứa `main.py`.
- Chạy chương trình bằng lệnh:

   ```bash
   python main.py
