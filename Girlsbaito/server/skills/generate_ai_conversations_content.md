# Skill: Tạo Nhật ký Phiên Làm Việc AI (AI Conversations Content)

**Mục tiêu của Skill này:** 
Chuẩn hóa quy trình AI tự động tóm tắt và ghi lại nhật ký (log) của các phiên làm việc (Conversation Histories). Việc này giúp hệ thống lưu giữ "ký ức" về các quyết định kiến trúc, các file đã sửa, và bối cảnh (context) phát triển để các phiên bản AI sau hoặc Developer khác có thể đọc lại mà không bị mất dấu.

---

## 1. Vị trí lưu trữ
- Tất cả nhật ký phiên làm việc phải được tạo tại thư mục: `.antigravity/ai_conversations/YYYYMMDD/` (trong đó YYYYMMDD là ngày thực hiện, ví dụ `20240428`).
- Tên file phải viết bằng tiếng Anh, nối nhau bằng dấu gạch dưới `_`, thể hiện rõ chủ đề chính của cuộc trò chuyện. Ví dụ: `update_ai_structures.md`, `optimize_job_import_performance.md`.

## 2. Quy tắc Ngôn ngữ & Văn phong
- **Ngôn ngữ:** Tuân thủ `AGENTS.md`, chỉ sử dụng **tiếng Việt**.
- **Văn phong:** Chuyên nghiệp, súc tích, đi thẳng vào vấn đề. Tường thuật lại những gì "chúng ta" (User và AI) đã quyết định và thực thi. 
- Không liệt kê lan man các câu chat, chỉ tập trung vào **KẾT QUẢ KỸ THUẬT**.

## 3. Cấu trúc Tiêu chuẩn của một file Conversation Log
Một file nhật ký chuẩn bắt buộc phải tuân theo cấu trúc sau:

### 3.1. Header (Thông tin chung)
- **Tiêu đề chính:** Tóm tắt Phiên làm việc: [Tên chủ đề]
- **Ngày thực hiện:** DD/MM/YYYY
- **Chủ đề (Topic):** 1 câu tóm tắt ngắn gọn.

### 3.2. Mục tiêu phiên làm việc (Objective)
- Giải thích tại sao cuộc trò chuyện này diễn ra? Vấn đề User đang gặp phải là gì? (Ví dụ: Tối ưu hóa API Import bị timeout, Xây dựng tài liệu nghiệp vụ, Sửa lỗi UI).

### 3.3. Các công việc đã hoàn thành (Tasks Completed)
Liệt kê chi tiết (Bullet points) các hành động AI đã làm:
- Đã đọc/phân tích những file nào?
- Đã tạo ra/sửa đổi những file nào? (Ghi rõ đường dẫn tương đối).
- Các logic/code cụ thể nào đã được viết hoặc Refactor? (Ví dụ: Đã đổi vòng lặp đồng bộ sang `asyncio.gather()`, đã phân quyền lại role Admin).

### 3.4. Các quyết định kỹ thuật / Phát hiện quan trọng (Key Discoveries & Decisions)
Đây là phần **GIÁ TRỊ NHẤT**. Hãy ghi lại:
- Những quy tắc hoặc ràng buộc hệ thống mới được phát hiện (Gotchas).
- Quyết định thay đổi kiến trúc (Ví dụ: Quyết định cấm AI chạy Alembic tự động, Quyết định tách luồng Gửi Email ra khỏi Transaction).
- Lý do tại sao lại chọn giải pháp A thay vì giải pháp B.

### 3.5. Việc cần làm tiếp theo (Next Steps - Nếu có)
- Các công việc đang làm dang dở hoặc User bảo "để sau làm".
- Các technical debt sinh ra trong phiên làm việc cần giải quyết trong tương lai.

---

## 4. Cách AI thực hiện Task này (Step-by-step)

Khi User yêu cầu *"Tóm tắt cuộc trò chuyện"* hoặc *"Lưu lại lịch sử"*:
1. **Quét bộ nhớ (Context Retrieval):** AI tự động xem lại (recall) toàn bộ chuỗi hội thoại từ đầu phiên đến hiện tại.
2. **Trích xuất thông tin:** Lọc ra các File Paths đã tương tác, các Tool đã gọi (ví dụ: `replace_file_content`, `run_command`), và kết quả của chúng.
3. **Format nội dung:** Sử dụng chính xác cấu trúc 5 phần ở mục 3 để soạn thảo nội dung Markdown.
4. **Tạo thư mục & Lưu file:** Sử dụng tool `write_to_file` để lưu vào đúng đường dẫn `.antigravity/ai_conversations/YYYYMMDD/<topic>.md`. Nếu thư mục ngày chưa tồn tại, tool sẽ tự động tạo.
5. **Thông báo hoàn tất:** Báo cáo lại cho User bằng tiếng Việt rằng nhật ký đã được lưu thành công kèm đường dẫn để User tiện kiểm tra.
