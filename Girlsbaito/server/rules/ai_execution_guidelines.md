# Hướng dẫn Thực thi Lệnh Dành cho AI (AI Execution Guidelines)

File này định nghĩa các lệnh Bash/Makefile chuẩn mà AI BẮT BUỘC phải dùng để thao tác với dự án Juku Connect một cách an toàn và nhất quán.

## 1. Nguyên tắc cốt lõi
Hệ thống sử dụng Docker Compose. Mọi câu lệnh tương tác với code (chạy test, cài thư viện, format code) đều phải được thực thi qua `docker compose exec web` hoặc `docker compose exec poetry` để đảm bảo môi trường Python là chính xác nhất.

---

## 2. Quản lý Thư viện (Poetry via Makefile)
Dự án sử dụng Makefile để bọc các lệnh Poetry, giúp build lại container tự động sau khi cài thư viện.

**⚠️ QUY TẮC NGHIÊM NGẶT:** AI **TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ ĐỘNG CHẠY** các lệnh cài đặt thư viện này. AI chỉ được phép in ra lệnh (dưới dạng markdown block) và yêu cầu User tự chạy trên Terminal của họ.

Các lệnh tham khảo (để in ra cho User):

- **Thêm thư viện cho Production:**
  `make library-add PACKAGES="ten_thu_vien_1 ten_thu_vien_2"`
- **Thêm thư viện cho Development (như pytest, black):**
  `make library-add-dev PACKAGES="ten_thu_vien"`
- **Xóa thư viện:**
  `make library-remove PACKAGES="ten_thu_vien"`

*Giải thích: Các lệnh trên sẽ tự động add thư viện, sinh lại `requirements.txt`, và build/restart lại container `web` để áp dụng ngay.*

---

## 3. Format Code và Linter (Bắt buộc sau khi sửa code)
Mỗi khi AI sửa đổi bất kỳ file `.py` nào, phải chạy format trước khi kết thúc lượt để tránh lỗi Git Hook và giữ code sạch:

- **Chạy Linter/Formatter cho toàn dự án:**
  `docker compose --env-file ./src/.env.dev exec poetry ruff check --fix .`
  `docker compose --env-file ./src/.env.dev exec poetry black .`
- **Chạy Linter cho một file/thư mục cụ thể (Tiết kiệm thời gian):**
  `docker compose --env-file ./src/.env.dev exec poetry ruff check --fix src/app/services/admin/job.py`

---

## 4. Quản lý Cơ sở dữ liệu (Alembic Migrations)
Bất cứ khi nào AI chỉnh sửa các file trong `src/app/models/`, bắt buộc phải tạo file Migration.

**⚠️ QUY TẮC NGHIÊM NGẶT:** AI **TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ ĐỘNG CHẠY** các lệnh migration (gen/upgrade) làm thay đổi Database. AI chỉ được phép in lệnh ra màn hình và yêu cầu User tự thao tác.

Các lệnh tham khảo (để in ra cho User):
- **Bước 1: Sinh file migration tự động**
  `docker compose --env-file ./src/.env.dev exec web alembic revision --autogenerate -m "Mô tả ngắn gọn bằng tiếng Anh"`
- **Bước 2: Cập nhật Database thực tế (Chạy migration)**
  `docker compose --env-file ./src/.env.dev exec web alembic upgrade head`
- **Gotcha (Lưu ý quan trọng):** Sau khi auto-generate, AI PHẢI MỞ FILE MIGRATION ĐÓ RA xem lại. Đôi khi Alembic không nhận diện đúng việc đổi tên cột hoặc xóa bảng, cần chỉnh tay lại file `.py` trong `alembic/versions/` trước khi upgrade.

---

## 5. Chạy Unit Test (Pytest)
Mỗi khi viết logic mới, hoặc refactor code cũ ở thư mục `services/`, phải chạy file test tương ứng:

- **Chạy toàn bộ test:**
  `docker compose --env-file ./src/.env.dev exec web pytest`
- **Chạy test cho 1 thư mục cụ thể:**
  `docker compose --env-file ./src/.env.dev exec web pytest tests/api/admin/`
- **Chạy test cho 1 file cụ thể với cờ báo lỗi chi tiết (-v):**
  `docker compose --env-file ./src/.env.dev exec web pytest -v tests/api/admin/test_job.py`

---

## 6. Ghi Log Changelog (Quy trình chốt Task)
Sau khi User báo "Hoàn thành Task X", AI NÊN đề xuất chạy lệnh ghi lại nhật ký (Để AI sau này đọc lại):
`Tạo file: /.antigravity/bu_change_logs/YYYY-MM-DD_Ten_Task.md` và tóm tắt ngắn gọn các bảng DB đã sửa, các logic đã thay đổi.
