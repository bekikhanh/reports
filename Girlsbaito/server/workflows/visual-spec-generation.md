# Workflow: Visual Technical Specification Generation
# ID: visual-spec-gen-001
# Trigger: User cung cấp mô tả thay đổi + (optional) các file liên quan
# Output: Một file HTML self-contained, chứa tài liệu Đặc tả Kỹ thuật trực quan

---

## 1. Input Requirements

| Input | Bắt buộc | Mô tả |
|---|---|---|
| Requirement | Có | Mô tả yêu cầu thay đổi (từ user/ticket) |
| File Context | Không | Đường dẫn file source code liên quan — nếu có, phải đọc trước khi viết |
| Output File Name | Không | Nếu không chỉ định, đặt tên theo pattern: `[feature]-spec.html` |

---

## 2. Execution Steps

### Bước 1: Context Awareness (Phân tích bối cảnh thực tế)

**CHỈ thực hiện nếu user đính kèm file hoặc chỉ đường dẫn cụ thể.**

- Đọc toàn bộ file liên quan (component, route, config, middleware).
- Xác định:
  - Luồng dữ liệu hiện tại (As-Is): dữ liệu đi qua đâu, render ở đâu.
  - Pain point: Vấn đề đang xảy ra là gì (UX, SEO, Security, Permission).
  - Existing patterns: Có cơ chế tương tự nào trong codebase không? Nếu có → tuân theo, đừng phát minh lại.

**Output nội bộ của bước này:** Danh sách file bị ảnh hưởng + mô tả ngắn vai trò từng file.

---

### Bước 2: Solution Architecture (Thiết kế giải pháp)

- Xây dựng giải pháp **tối thiểu, có thể revert được** — không over-engineer.
- Chia nhỏ thay đổi thành các **Layer**:
  - `UI Layer`: Component, Sidebar, Route Guard phía client.
  - `Server Layer`: Middleware, API, SSR guard (Astro frontmatter).
  - `SEO Layer`: robots.txt, sitemap filter, noindex.
  - `Config Layer`: Biến môi trường, feature flag.
- **Xác định rõ**: Cái gì thay đổi, cái gì KHÔNG thay đổi (để tránh scope creep).
- **Xác định Release Plan**: Thay đổi có cần deploy riêng không? Có thể rollback bằng cách nào?

**Output nội bộ của bước này:** Danh sách thay đổi theo từng file + số dòng ước tính.

---

### Bước 3: HTML Spec Rendering (Sinh file tài liệu)

Áp dụng rule `technical-spec-visualizer` để tạo file HTML.

**Cấu trúc bắt buộc (theo thứ tự sau):**

> **CRITICAL — KHÔNG được bỏ qua dù model có giới hạn token:**
> - Sticky Nav BẮT BUỘC xuất hiện ở mọi file output, không ngoại lệ.
> - Browser Mockup BẮT BUỘC hiển thị ĐẦY ĐỦ 100% phần tử UI gốc — KHÔNG được cắt bớt, rút gọn, hay thay bằng `...` hoặc comment. Nếu UI có 12 trường thì mockup phải có đủ 12 trường.
> - Phần tử thêm/sửa phải có border đỏ + badge `NEW` / `MODIFIED` rõ ràng.

1. **Sticky Nav** *(BẮT BUỘC, LUÔN CÓ)*
   - `position: sticky; top: 0; z-index: 1000`
   - Nền tối (`#1f2937`), border dưới màu `var(--primary)` (`#F98800`).
   - Anchor link đến tất cả section chính trong trang.

2. **Overview** (label: 概要)
   - Mục tiêu nghiệp vụ 2-3 câu.
   - Flow Diagram mô tả kết quả mong muốn (ai bị chặn, ai được phép).

3. **Current State** (label: 現状) — *Bỏ qua nếu không có file context*
   - Bảng liệt kê file liên quan + trạng thái hiện tại (đã làm / chưa làm).
   - info-banner giải thích điểm cần chú ý.

4. **Strategy / Flow** (label: 方針) — *Bỏ qua nếu thay đổi đơn giản, 1 bước*
   - Flow Diagram mô tả luồng kiểm duyệt/phân quyền theo từng nhánh.

5. **Implementation Sections** (label: 変更N) — 1 section riêng cho mỗi layer thay đổi
   - **Browser Mockup** *(BẮT BUỘC nếu thay đổi bất kỳ phần UI nào)*:
     - Render lại TOÀN BỘ form/trang — gồm TẤT CẢ các field/element hiện có.
     - Element mới thêm: `border: 2.5px solid #dc2626` + badge `NEW` absolute.
     - Element được sửa: `border: 2.5px solid #d97706` + badge `MODIFIED` absolute.
   - **Code Diff Block** — Luôn có, chỉ rõ file path + dòng nào thêm/xóa, ít nhất 3 dòng context trước/sau.
   - **Annotations** (bug/fixed/resolved/info) để giải thích lý do kỹ thuật.

6. **Environment Variables** (label: 環境変数) — *Chỉ có nếu tính năng dùng biến môi trường / feature flag*
   - kv-row cho từng biến: Tên, Giá trị mặc định, Phạm vi.
   - Bảng: Giá trị theo môi trường (local / dev / prod).

7. **Release Plan** (label: 公開手順) — *Bỏ qua nếu không có deploy steps phức tạp*
   - Step-list cho Phase 1 (merge + không public).
   - Step-list cho Phase 2 (public thật sự) — nếu áp dụng.

8. **QA Checklist** (label: 確認項目) — Bắt buộc
   - Checklist với `check-icon` yes/warn/skip cho từng kịch bản cần verify.

9. **Summary Table** (label: まとめ) — Bắt buộc
   - Bảng tổng hợp: File | Nội dung thay đổi | Phase/Action.
   - resolved-annotation tổng kết lợi ích của giải pháp.

---

### Bước 4: Output & Validation

- **Tên file**: Đặt tại root của project (`/Users/chungnb/workspace/coding/1-beki/3-juku/juku-user/`), tên dạng `[feature-slug]-spec.html`.
- **Kiểm tra trước khi xuất**:
  - [ ] `<meta charset="UTF-8">` có không? (Bắt buộc để hiển thị tiếng Nhật)
  - [ ] **Sticky Nav có xuất hiện không?** (Nếu không → output sai, phải làm lại)
  - [ ] Tất cả anchor trong Sticky Nav link đúng đến `id` trong body chưa?
  - [ ] **Browser Mockup có đủ 100% phần tử của UI gốc không?** Đếm số field trong file source và so sánh với mockup — phải bằng nhau.
  - [ ] Element mới/sửa có border đỏ và badge `NEW`/`MODIFIED` không?
  - [ ] Code diff có ít nhất 3 dòng context trước/sau không?
  - [ ] File path và biến môi trường có lấy từ code thực tế, không phải placeholder?
  - [ ] Mọi `<span class="highlight-line">` có wrap trong `<span>...<br>` không? (Nếu thiếu `display:block` sẽ không hiển thị đúng)
  - [ ] Section nào "Bỏ qua" phải bỏ hoàn toàn, không để lại comment placeholder.

---

## 3. Completion Criteria

- Một file HTML duy nhất, mở trực tiếp trên browser không cần server.
- Người không biết code (PM, BA, khách hàng Nhật) đọc được và hiểu rõ thay đổi nhờ Browser Mockup + Flow Diagram.
- Developer biết chính xác cần sửa file gì, dòng nào, không cần hỏi lại.
- Có thể in ra PDF (print-friendly layout) — không có fixed-height container gây cắt nội dung.
