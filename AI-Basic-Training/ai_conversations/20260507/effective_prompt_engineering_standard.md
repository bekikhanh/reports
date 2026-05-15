# Tóm tắt Phiên làm việc Chi tiết: Hệ thống Hóa Quy trình Spec & Tiêu chuẩn Prompting
**Ngày thực hiện:** 07/05/2026  
**Dự án:** AI Basic Training Documentation System  
**Chủ đề:** Tối ưu hóa quy trình tạo tài liệu kỹ thuật tự động và thiết lập "Gold Standard" cho Prompt Engineering.

## 1. Mục tiêu phiên làm việc (Detailed Objective)
- **Chuẩn hóa Workflow:** Xây dựng một quy trình lặp lại được để chuyển đổi dữ liệu thô (PDF) thành các sản phẩm trình chiếu (Slides) và báo cáo kỹ thuật (Reports) có tính tương tác cao.
- **Tối ưu hóa UX/UI cho Tài liệu:** Đảm bảo tài liệu kỹ thuật không bị khô khan bằng cách áp dụng các ngôn ngữ thiết kế hiện đại (Glassmorphism, Dark Mode) và các hiệu ứng động (Micro-animations).
- **Thiết lập Tiêu chuẩn Prompting:** Tìm ra công thức hoàn hảo để AI tạo ra kết quả chính xác, đầy đủ và không bị "ảo giác" ngay từ lần yêu cầu đầu tiên.

## 2. Các công việc đã hoàn thành (Tasks Completed)

### 2.1. Xây dựng Công cụ & Workflow
- **`visual-spec-generation-slide.md`**: Một workflow mới kế thừa từ bản gốc nhưng chuyên biệt cho việc render Slide HTML FullHD. Workflow này quy định chặt chẽ về việc sử dụng Tailwind CSS, CDN cho FontAwesome và cấu trúc navigation bằng phím mũi tên.
- **Hệ thống hóa nội dung:** Phân tích file `AI Basic Training.pdf` để bóc tách các module: Bản chất AI, Prompt Engineering, Use Cases, Security và Tooling.

### 2.2. Phát triển Sản phẩm Đầu ra
- **Slide Presentation (`ai-basic-training-slide.html`)**:
    - Sử dụng `clamp()` để font-size tự động điều chỉnh cực lớn (đảm bảo hiển thị tốt trên sân khấu).
    - Tích hợp thanh progress bar và hệ thống chuyển cảnh `cubic-bezier` mượt mà.
- **Technical Report (`quyen-sample-2.html`)**:
    - Bố cục Scrolling Report với thanh Navigation dính (Sticky Nav).
    - Tích hợp Logo Bekisoft (`QR.png`) và thanh tiến trình đọc (Scroll Progress indicator).
    - Mở rộng nội dung từ tóm tắt đơn giản thành tài liệu chi tiết (Full Content) với các bảng so sánh và Code Diff.
- **Pinky Versions**: Tạo các biến thể màu hồng cho cả Slide và Report để phục vụ sở thích cá nhân hóa thương hiệu.

### 2.3. Tối ưu hóa Visual & Interaction
- Triển khai hệ thống icon động sử dụng FontAwesome kết hợp CSS Animations:
    - `animate-float`: Cho các icon trang trí.
    - `animate-pulse-glow`: Cho logo và các cảnh báo quan trọng.
    - `animate-spin-slow`: Cho các icon liên quan đến tư duy/máy móc (Brain/Atom).
    - `animate-bounce-subtle`: Cho các tiêu đề mục.

## 3. Tiêu chuẩn Prompt Engineering "Gold Standard"
Phát hiện quan trọng nhất là làm thế nào để Prompt đạt hiệu quả tối đa ngay từ lần đầu (First-time Success).

### 3.1. Cấu trúc 6 Yếu tố (Bắt buộc)
1.  **Role (Vai trò):** Phải gán cho AI một "Personality" cụ thể. 
    *   *Bad:* "Hãy viết JD..."
    *   *Good:* "Bạn là một Tech Recruiter chuyên nghiệp tại Bekisoft với 10 năm kinh nghiệm tuyển dụng React Native..."
2.  **Task (Nhiệm vụ):** Phải là một hành động cụ thể và có mục đích.
    *   *Bad:* "Tóm tắt file này."
    *   *Good:* "Hãy tóm tắt 5 bài học quan trọng nhất từ file PDF này dưới dạng danh sách gạch đầu dòng để đào tạo cho nhân viên mới."
3.  **Context (Ngữ cảnh):** Cung cấp dữ liệu thô và bối cảnh sử dụng. (Ví dụ: "Đây là nội dung đào tạo AI, dùng để trình bày trên màn hình lớn cho 100 người xem").
4.  **Format (Định dạng):** Quy định rõ cấu trúc dữ liệu. (Ví dụ: "Trả về mã HTML sử dụng Tailwind CSS, màu chủ đạo là Cam").
5.  **Tone (Phong thái):** Quyết định cách AI "nói chuyện". (Ví dụ: "Ngôn ngữ kỹ thuật chính xác, chuyên nghiệp nhưng vẫn tạo được cảm hứng").
6.  **Constraint (Ràng buộc):** Đặt ra các "Red Lines". (Ví dụ: "Không được tự ý thêm các công cụ không có trong file PDF", "Giữ nguyên các ví dụ về code JS").

### 3.2. Kỹ thuật "Few-Shot" & "Chain-of-Thought"
- Cung cấp ít nhất 1-2 ví dụ mẫu (Few-shot) giúp AI hiểu được "gu" thẩm mỹ và độ chi tiết mong muốn.
- Yêu cầu AI "suy nghĩ từng bước" (Think step-by-step) trước khi đưa ra kết quả cuối cùng để tránh bỏ sót nội dung.

## 4. Các quyết định kỹ thuật Quan trọng
- **Tối ưu hóa Tài liệu:** Quyết định sử dụng kiến trúc "Self-contained HTML" (nhúng mọi thứ vào 1 file) để User có thể mở báo cáo ở bất cứ đâu mà không cần cài đặt môi trường.
- **Bảo mật:** Thiết lập quy tắc "Sanitize before Send" - Mọi dữ liệu code nhạy cảm phải được thay thế bằng placeholder trước khi đưa vào Prompt.
- **Branding:** Logo Bekisoft phải được đặt ở vị trí trang trọng (Nav bar) để khẳng định tính chính thống của tài liệu.

## 5. Việc cần làm tiếp theo (Next Steps)
- Lưu trữ bộ Template này làm chuẩn cho mọi dự án Spec sau này của Bekisoft.
- Tiếp tục mở rộng các bộ icon động và hiệu ứng tương tác để làm phong phú thêm trải nghiệm người đọc.
- Cập nhật định kỳ nội dung AI Basic Training khi các mô hình mới (GPT-5, Claude 4) ra đời.
