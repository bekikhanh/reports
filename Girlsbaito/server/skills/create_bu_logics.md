# Skill: Hướng dẫn Viết Tài liệu Nghiệp vụ (Business Logics - bu_logics)

**Mục tiêu của Skill này:** 
Giúp AI tạo ra các tài liệu mô tả logic nghiệp vụ (Business Logics) một cách chuẩn chỉ, sâu sát với mã nguồn thực tế và hữu ích cho quá trình bảo trì dự án sau này.

---

## 1. Vị trí lưu trữ
- Tất cả tài liệu nghiệp vụ phải được tạo tại thư mục: `.antigravity/bu_logics/`
- Tên file phải mang ý nghĩa đại diện cho chức năng, ví dụ: `import_jobs.md`, `calculate_billing.md`.

## 2. Quy tắc Ngôn ngữ & Văn phong
- **Ngôn ngữ:** Tuân thủ AGENTS.md, chỉ sử dụng **tiếng Việt**.
- **Văn phong:** Viết theo dạng tài liệu kỹ thuật chuyên sâu (Deep-dive Tech Doc). Tránh sử dụng từ ngữ chung chung như "Hệ thống xử lý dữ liệu rồi lưu lại". Phải viết cụ thể: "Hệ thống dùng `begin_nested()` để tạo savepoint, nếu lỗi thì raise `SkipRowError` để rollback riêng dòng đó".
- **Không dùng Icon:** Tránh sử dụng các biểu tượng cảm xúc (🚀, 💡...) làm mất tính chuyên nghiệp.

## 3. Cấu trúc Tiêu chuẩn của một file bu_logics
Một file tài liệu nghiệp vụ chuẩn phải bao gồm các phần sau:

### 3.1. Thông tin cơ sở
- **Đường dẫn file xử lý chính:** (Ví dụ: `/src/app/services/.../file.py`)
- **Hàm/Class thực thi chính:** (Ví dụ: `import_job_from_csv_v2`)

### 3.2. Tổng quan Luồng (Workflow)
- Tóm tắt nhanh các bước từ khi nhận Request đầu vào đến khi trả Response đầu ra.
- Nếu có phân nhánh logic lớn (Ví dụ: Create vs Update), hãy liệt kê rõ ràng.

### 3.3. Các quy tắc Validate Dữ liệu (Validation Rules)
- Liệt kê cụ thể **các con số và điều kiện cứng** trong code:
  - Độ dài tối đa (max_length), kiểu dữ liệu.
  - Ràng buộc logic (Ví dụ: `end_date > start_date`, `max_salary > min_salary`).
  - Phân quyền (Ví dụ: Role nào được làm gì, trạng thái (status) nào thì được update).

### 3.4. Logic Cốt lõi (Core Logic)
- Giải thích cách hệ thống thao tác với cơ sở dữ liệu:
  - Cách tạo mới dữ liệu.
  - Cách cập nhật dữ liệu (Ví dụ: Xóa toàn bộ dữ liệu ở bảng trung gian (Many-to-Many) rồi Insert lại thay vì Update từng dòng).
  - Các kỹ thuật tối ưu: Caching dữ liệu tĩnh vào Dictionary/RAM để giảm thiểu N+1 queries.

### 3.5. Xử lý Dữ liệu bên thứ ba / Side Effects
- Bắt buộc phải mô tả nếu nghiệp vụ có gọi ra ngoài hệ thống:
  - Gọi AWS S3: Upload ảnh, kiểm tra dung lượng ảnh (Concurrent/Async I/O).
  - Gọi OpenSearch: Khi nào thì Reindex, dùng cơ chế Bulk hay update lẻ tẻ.
  - Gửi Email (SES) / Gửi SMS (SNS): Gửi khi nào, template nào.

### 3.6. Tính toàn vẹn Dữ liệu & Xử lý Lỗi (Transactions & Error Handling)
- Giải thích rõ cơ chế Transaction: Dùng `commit()`, `rollback()`, hay `begin_nested()` (Savepoint). Lỗi ở 1 dòng thì fail cả batch hay chỉ fail dòng đó.
- Cấu trúc Response trả lỗi về Frontend (để Frontend parse và hiển thị được màu đỏ đúng vị trí dòng/cột).

---

## 4. Yêu cầu bổ sung về nội dung
Ngoài cấu trúc trên, tùy vào từng nghiệp vụ, phải bổ sung thêm:
- **Bảng Mapping Field (nếu có import/export CSV hoặc form submit):** Liệt kê tên cột gốc (tiếng Nhật/Anh) sang tên field trong DB Model, ví dụ:
  | Tên cột CSV | Tên field trong Model | Ghi chú |
  |---|---|---|
  | `求人タイトル` | `Job.title` | Tối đa 50 ký tự |
- **Enum / Trạng thái:** Liệt kê các giá trị Enum quan trọng được dùng trong luồng (ví dụ: `PublishStatusEnum.DRAFT = 1`, `PublishStatusEnum.PUBLISHED = 2`).
- **Các Hàm Helper quan trọng:** Ghi chú tên và mục đích của các hàm phụ trợ thường xuyên được gọi trong luồng chính.

---

## 5. Cách AI thực hiện Task này (Step-by-step)
1. **Xác định điểm vào (Entry Point):** Dùng `grep_search` tìm tên hàm hoặc endpoint liên quan đến chức năng cần viết tài liệu.
2. **Đọc hàm chính:** Dùng `view_file` với `StartLine`/`EndLine` để đọc hàm chính từ đầu đến cuối. Chú ý đặc biệt đến các câu `if/else`, `raise`, `try/except`, `select`/`insert`/`update`/`delete`.
3. **Đọc các hàm Helper liên quan:** Grep để tìm và đọc các hàm helper được gọi bên trong hàm chính.
4. **Tra cứu Enum và Model:** Nếu cần, đọc file `enums/` và `models/` để lấy giá trị Enum chính xác và tên cột trong bảng DB.
5. **Tổng hợp và Viết:** Gom nhóm các logic rải rác thành các mục theo đúng cấu trúc ở mục 3. Mọi kết luận phải dựa trên code thực tế, tuyệt đối không tự sáng tác thêm logic nếu chưa đọc code xác nhận.
6. **Lưu file:** Ghi vào `.antigravity/bu_logics/<tên_chức_năng>.md`.
7. **Cập nhật Mapper:** Cập nhật file `.antigravity/bu_logics/init.md` bằng cách thêm một dòng mapping giữa file tài liệu vừa tạo và đường dẫn các file code thật sự, có thể là một hoặc nhiều tuỳ thuộc nghiệp vụ.
