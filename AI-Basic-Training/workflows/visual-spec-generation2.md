# Workflow: AI Training Material Generation
# ID: visual-training-gen-001
# Trigger: User cung cấp nội dung bài học hoặc đề cương khoá học
# Output: Một file HTML self-contained, chứa tài liệu đào tạo nội bộ chuyên nghiệp

---

## 1. Input Requirements

| Input | Bắt buộc | Mô tả |
|---|---|---|
| Lesson Outline | Có | Đề cương hoặc nội dung chi tiết của bài học/khoá học |
| Target Audience | Không | Đối tượng người học (Dev, QC, BA, HR, v.v.) |
| Output File Name | Không | Nếu không chỉ định, đặt tên theo pattern: `[topic]-training.html` |

---

## 2. Execution Steps

### Bước 1: Content Structuring (Cấu trúc nội dung)

- **Nguyên tắc cốt lõi**: Giữ nguyên nội dung từ input đầu vào, tuyệt đối KHÔNG tự ý thêm bớt hoặc "bịa" nội dung ngoài tài liệu gốc.
- Phân tích nội dung đầu vào để chia thành các **Chương (Chapters)** và **Mục nhỏ (Sections)** đúng theo cấu trúc của file nguồn.
- Xác định các phần nội dung có độ phức tạp cao (quy trình, so sánh, danh sách dài) để chuyển sang dạng hình ảnh trực quan.

**Output nội bộ:** Danh sách các ID section và danh sách các phần sẽ được chuyển thành Infographic.

---

### Bước 2: Visual Mapping (Ánh xạ thành phần trực quan)

Dựa trên nội dung, chọn các component từ `format_training.html` hoặc tạo Infographic:
- **Lý thuyết/Văn bản**: Dùng đoạn văn + `card-grid`.
- **Lưu ý/Tips**: Dùng `callout` (info/success/warning/danger).
- **Flow, Table, Ví dụ**: BẮT BUỘC sử dụng skill `canvas-design` để tạo **Infographics** (.png).
- **Tiến độ**: Sử dụng `level-seg` hoặc `steps` flow.

---

### Bước 3: Training HTML Rendering (Sinh file bài giảng)

Áp dụng rule `training-material-generator` để tạo file HTML.

**Cấu trúc bắt buộc (phải có đủ các thành phần sau):**

1.  **Top Nav**: Chứa Logo công ty, tên khoá học và phiên bản.
2.  **Navigation Buttons (Top)**: Các nút "Tiếp theo" và "Quay lại" BẮT BUỘC đặt ở đầu mỗi section (ngay dưới top nav hoặc trên page-header).
3.  **Sidebar Navigation**: Danh sách các chương và mục con với logic `show(sectionId)`.
4.  **Page Header**: Mỗi section bắt đầu bằng `page-header`.
5.  **Infographics (Trọng tâm)**: Chèn các hình ảnh đã generate cho các phần Flow, Table, và Ví dụ. Mỗi hình ảnh phải có `infographic-caption` mô tả ngắn gọn.
6.  **Prompt Boxes**: Sử dụng định dạng code/box chuyên dụng cho các ví dụ prompt AI nếu không dùng infographic.

---

### Bước 4: JavaScript & Logic Integration

- Tích hợp hàm `show(id)` để ẩn/hiện các section.
- Cập nhật thanh `progress-bar` khi người dùng chuyển section.
- Đảm bảo class `active` được gán đúng cho cả section nội dung và item trong sidebar.

---

### Bước 5: Output & Validation

- **Tên file**: Lưu tại đường dẫn user yêu cầu hoặc mặc định `[topic]-training.html`.
- **Checklist kiểm tra**:
  - [ ] File HTML có self-contained (CSS/JS nằm trong file hoặc link CDN ổn định)?
  - [ ] Sidebar có đầy đủ các chương và link đúng `id`?
  - [ ] Các `callout` và `card` có hiển thị đúng màu sắc/icon không?
  - [ ] Các ví dụ prompt có sử dụng class `prompt-box` không?
  - [ ] Mobile responsive: Menu có thu gọn hoặc hoạt động tốt trên màn hình nhỏ?
  - [ ] Font chữ: Đã link Google Fonts (Outfit, Lora, JetBrains Mono) chưa?

---

## 3. Completion Criteria

- Một file HTML duy nhất, giao diện Premium, hiện đại với tông màu và font chữ đúng yêu cầu.
- **Nội dung chính xác 100%** so với tài liệu gốc, không có hiện tượng "bịa" nội dung.
- Các quy trình phức tạp (Flow), bảng dữ liệu (Table), và ví dụ thực hành (Example) được trình bày dưới dạng **Infographics** sắc nét.
- Trải nghiệm người dùng mượt mà, điều hướng thuận tiện với các nút bấm ở đầu trang.
- Phù hợp cho việc tự học hoặc đào tạo nội bộ chuyên nghiệp.
