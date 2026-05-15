# Workflow: Visual Technical Specification Slide Deck
# ID: visual-spec-slide-001
# Base: visual-spec-generation.md
# Trigger: User cung cấp mô tả thay đổi + (optional) các file liên quan
# Output: Một file HTML slide presentation (FullHD), dùng cho báo cáo/demo.

---

## 1. Core Logic Inheritance

Workflow này kế thừa toàn bộ logic phân tích tại:
- **Bước 1: Context Awareness** (từ `visual-spec-generation.md`)
- **Bước 2: Solution Architecture** (từ `visual-spec-generation.md`)

*Lưu ý: Chỉ thay đổi cách trình bày (Rendering) từ dạng tài liệu cuộn sang dạng Slide.*

---

## 2. Rendering Requirements (Slide Version)

Áp dụng style từ `n8n-workshop-fullhd.html` để tạo file HTML.

### A. UI/UX Style (Bắt buộc)
- **Framework**: Tailwind CSS (CDN).
- **Fonts**: `Inter`, `Fira Code` (cho code), `Noto Sans JP` (cho tiêu đề nếu cần).
- **Theme**: Dark Mode (Background: `radial-gradient(circle at top right, #1e293b 0%, #020617 100%)`).
- **Aesthetics**:
  - Glassmorphism cho card (`backdrop-filter: blur(12px)`).
  - Giao diện MacBook/Terminal cho các phần hiển thị code/mockup.
  - Hiệu ứng `animate-float` và `animate-slideIn`.
  - Progress bar ở dưới cùng để theo dõi tiến độ slide.

### B. Slide Structure
Mỗi mục nội dung từ Bước 2 sẽ được phân bổ vào các Slide sau:

1. **Slide 0: Cover**
   - Tiêu đề tính năng (lớn, gradient text).
   - Author (ChungNB) + Logo project.
   - Minh họa bằng `n8n-node` icons (nếu liên quan đến workflow).

2. **Slide 1: Overview (概要)**
   - Business Goals (2-3 gạch đầu dòng).
   - Flow Diagram (nằm trong một `glass-card` lớn).

3. **Slide 2: Current State (現状)**
   - Liệt kê file bị ảnh hưởng.
   - Một `mac-window` mockup hiển thị UI hiện tại (nếu có).

4. **Slide 3+: Implementation (変更内容)**
   - **Mỗi Layer/Feature = 1 slide riêng.**
   - **Trái**: Browser Mockup (Bắt buộc hiển thị 100% UI, highlight element NEW/MODIFIED bằng border đỏ/cam và badge).
   - **Phải**: Code Diff Block (Dùng giao diện Terminal tối màu).
   - Sử dụng `chibi-box` hoặc `mac-window` để bọc các phần này.

5. **Slide N-1: QA Checklist (確認項目)**
   - Danh sách các test case cần verify, trình bày dạng card sạch sẽ.

6. **Slide N: Summary (まとめ)**
   - Bảng tổng hợp thay đổi.
   - Nút "End Presentation" hoặc thông tin liên hệ.

---

## 3. Interactive Logic (JavaScript)

File HTML phải bao gồm script điều hướng:
- Phím mũi tên Sang trái/Sang phải để chuyển slide.
- Nút bấm Prev/Next nổi trên màn hình (độ mờ thấp, hiện rõ khi hover).
- Logic `slide.active` để điều khiển hiển thị (như trong `n8n-workshop-fullhd.html`).

---

## 4. Output Validation

- [ ] **Slide Layout**: Nội dung không được tràn khỏi màn hình (sử dụng `overflow-y: auto` cho slide nội dung dài).
- [ ] **Mockup Integrity**: Vẫn tuân thủ rule "hiển thị 100% UI gốc", không được rút gọn.
- [ ] **Animations**: Phải có hiệu ứng `slideIn` khi chuyển slide.
- [ ] **Responsive**: Phải hiển thị tốt trên màn hình 1920x1080 và MacBook 16".
- [ ] **Self-contained**: Một file HTML duy nhất, không phụ thuộc vào server (ngoại trừ CDN CSS/JS).

---

## 5. Completion Criteria

- Một file presentation chuyên nghiệp, có thể dùng để thuyết trình trực tiếp cho khách hàng hoặc PM.
- Hiệu ứng visual "WOW" ngay từ slide đầu tiên.
- Thông tin kỹ thuật vẫn đầy đủ và chính xác như bản spec dạng document.
