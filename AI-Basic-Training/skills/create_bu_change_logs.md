# Skill: Hướng dẫn Viết File Lịch sử Thay đổi Nghiệp vụ (bu_change_logs)

**Mục tiêu của Skill này:**
Giúp AI tạo ra các file ghi chép lịch sử thay đổi code liên quan đến nghiệp vụ một cách chuẩn chỉ, đủ chi tiết để AI đọc lại ở context khác có thể hiểu chính xác những gì đã làm, tại sao làm, và code cụ thể đã thay đổi thế nào — mà không cần phải đọc lại toàn bộ file source.

---

## 1. Vị trí lưu trữ & Quy tắc đặt tên
- **Thư mục gốc:** `.antigravity/bu_change_logs/`
- **Cấu trúc thư mục:** `.antigravity/bu_change_logs/<tên_chức_năng>/<tên_chức_năng_YYYYMMDD>.md`
  - Ví dụ: `.antigravity/bu_change_logs/import_jobs/import_jobs_20260428.md`
- **Quy tắc:** Mỗi lần thực hiện thay đổi lớn trong một ngày tạo một file mới với ngày tương ứng. Nếu cùng ngày có nhiều đợt thay đổi thì thêm hậu tố `_v2`, `_v3`.

---

## 2. Cấu trúc Tiêu chuẩn của một File Change Log

### Phần Header (Bắt buộc)
```
# Change Log: <Tên Chức năng> - YYYY/MM/DD

**Mục tiêu thay đổi:** (1-2 câu mô tả vấn đề cần giải quyết và giải pháp tổng thể)
**Ngày thực hiện:** YYYY-MM-DD HH:MM (Timezone: Asia/Tokyo)
**Người thực hiện:** AI (Antigravity) / <Tên Dev nếu có>
**Nhánh Git ảnh hưởng:** (dev / staging / production)

**Danh sách File đã thay đổi:**
- `/đường/dẫn/file1.py` — (mô tả ngắn gọn thay đổi ở file này)
- `/đường/dẫn/file2.py` — (mô tả ngắn gọn thay đổi ở file này)
```

---

### Mục 1: Bối cảnh & Vấn đề gốc (Root Cause)
- Mô tả chi tiết **vấn đề trước khi thay đổi**: Biểu hiện lỗi là gì (timeout, sai dữ liệu, crash...)? Vấn đề xảy ra ở đâu trong luồng code?
- Nêu rõ **nguyên nhân kỹ thuật**: N+1 query, blocking I/O, race condition, logic sai...
- Ghi cụ thể **hàm/dòng code** nào là nguyên nhân gốc.

### Mục 2: Các Thay đổi Cụ thể (Detailed Changes)
Đây là phần **quan trọng nhất**. Với mỗi thay đổi phải ghi đủ:

**a) Mô tả thay đổi:** Thay đổi gì, tại sao thay đổi.

**b) Code trước (Before):** Đoạn code gốc bị thay thế (dùng code block).
```python
# Code cũ
```

**c) Code sau (After):** Đoạn code mới thay thế (dùng code block).
```python
# Code mới
```

**d) Lý do kỹ thuật:** Giải thích tại sao code mới đúng hơn code cũ.

> Mỗi thay đổi độc lập (tối ưu cache, fix bug, refactor...) cần được liệt kê thành một block riêng biệt theo format trên.

### Mục 3: Kiểm tra sau thay đổi (Verification)
- Đã kiểm tra syntax chưa? (`ast.parse` hay tương đương)
- Đã kiểm tra logic thủ công chưa?
- Có test case nào cần chạy không?

### Mục 4: Tác động & Rủi ro (Impact & Risk)
- Thay đổi có ảnh hưởng đến luồng nào khác không?
- Có cần chạy migration DB không?
- Có cần thông báo Frontend về thay đổi format API không?
- Có điểm rủi ro tiềm ẩn nào cần theo dõi thêm không?

---

## 3. Quy tắc Ngôn ngữ & Văn phong
- **Ngôn ngữ:** Tiếng Việt. Thuật ngữ kỹ thuật giữ nguyên tiếng Anh.
- **Code snippet:** Luôn dùng code block có chú thích `# Code cũ` / `# Code mới`.
- **Không viết chung chung:** Không viết "Đã tối ưu hiệu năng". Phải viết "Thay thế `requests.head()` bằng `httpx.AsyncClient` + `asyncio.gather()` để fetch metadata ảnh song song thay vì tuần tự."

---

## 4. Cách AI thực hiện Task này (Step-by-step)
1. **Đọc lại context:** Tổng hợp tất cả thay đổi đã làm trong phiên làm việc hiện tại từ ký ức context hoặc đọc lại file source.
2. **Phân nhóm thay đổi:** Gom các thay đổi lại theo nhóm (Performance / Bug Fix / Refactor...).
3. **Viết Before/After:** Với mỗi thay đổi, trích dẫn đoạn code gốc và đoạn code mới. Nếu không nhớ chính xác, dùng `grep_search` + `view_file` để tìm lại trong source.
4. **Ghi tác động:** Nhận xét xem thay đổi có cần migration, có ảnh hưởng Frontend, có rủi ro không.
5. **Lưu file:** Ghi vào `.antigravity/bu_change_logs/<tên>/<tên_YYYYMMDD>.md`.
