# Rule: AI Training Material Generator
Role: Learning Experience (LX) Designer & UI/UX Architect

---

## 0. Non-Negotiable Output Constraints

> Các ràng buộc dưới đây LUÔN LUÔN được áp dụng cho mọi file tài liệu training HTML được tạo ra bởi workflow này.

### 0.1 — Single File & Self-Contained
- Toàn bộ CSS và JavaScript phải được nhúng trực tiếp trong file HTML.
- Không sử dụng thư viện ngoài trừ Google Fonts.

### 0.2 — Interactive Sidebar & Navigation
- Sidebar phải chứa danh mục các chương và mục con.
- Sử dụng hàm JavaScript `show(sectionId)` để chuyển đổi giữa các `div.section`.
- Sidebar item phải có class `active` khi section tương ứng đang hiển thị.

### 0.3 — Mobile Responsiveness
- Trên màn hình nhỏ (< 900px), sidebar phải có cơ chế đóng/mở (mặc định đóng).
- Content padding phải được điều chỉnh cho phù hợp với di động.

---

## 1. CSS Design System (Bắt buộc)

Sử dụng các biến CSS và reset sau:

```css
:root {
  --green:       #16a34a;
  --green-light: #22c55e;
  --green-dim:   #14532d;
  --green-bg:    #f0fdf4;
  --green-border:#bbf7d0;
  --blue:        #2563eb;
  --blue-bg:     #eff6ff;
  --amber:       #d97706;
  --amber-bg:    #fffbeb;
  --red:         #dc2626;
  --red-bg:      #fef2f2;
  --purple:      #7c3aed;
  --sidebar-w:   280px;
  --header-h:    56px;
  --text:        #1e293b;
  --text-muted:  #64748b;
  --border:      #e2e8f0;
  --bg:          #ffffff;
  --sidebar-bg:  #f8fafc;
  --code-bg:     #f1f5f9;
  --radius:      8px;
  --shadow:      0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06);
}

body {
  font-family: 'Outfit', sans-serif;
  color: var(--text);
  background: var(--bg);
  font-size: 15px;
  line-height: 1.7;
}
```

---

## 2. Mandatory UI Components

### 2.1 — Callouts
Dùng cho các ghi chú, mục tiêu hoặc cảnh báo.
```html
<div class="callout success">
  <span class="callout-icon">💡</span>
  <div class="callout-body">
    <div class="callout-title">Tiêu đề</div>
    Nội dung...
  </div>
</div>
```
Các class: `info`, `success`, `warning`, `danger`.

### 2.2 — Card Grid
Dùng để tóm tắt các ý chính.
```html
<div class="card-grid cols-2">
  <div class="card green">
    <div class="card-icon">🎯</div>
    <div class="card-title">Tiêu đề</div>
    <div class="card-body">Mô tả ngắn...</div>
  </div>
</div>
```

### 2.3 — Prompt Box (QUAN TRỌNG)
Dùng để hiển thị ví dụ prompt AI.
```html
<div class="prompt-box">
  <div class="prompt-label">Prompt hoàn chỉnh</div>
  <span class="prompt-role">Bạn là [Vai trò].</span><br><br>
  <span class="prompt-task">Thực hiện [Nhiệm vụ].</span><br><br>
  <span class="prompt-context">Bối cảnh: [Bối cảnh].</span><br><br>
  <span class="prompt-format">Định dạng: [Định dạng].</span>
</div>
```

### 2.4 — Steps Flow
Dùng mô tả quy trình.
```html
<div class="steps">
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-label">Bước 1</div>
  </div>
  <!-- ... -->
</div>
```

---

## 3. JavaScript Logic (Bắt buộc)

```javascript
function show(id) {
  // Ẩn tất cả các section
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  // Hiện section được chọn
  const target = document.getElementById(id);
  if (target) target.classList.add('active');
  
  // Cập nhật trạng thái active cho Sidebar
  document.querySelectorAll('.sidebar-item').forEach(item => {
    item.classList.remove('active');
    if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(`'${id}'`)) {
      item.classList.add('active');
    }
  });

  // Cuộn lên đầu trang nội dung
  window.scrollTo(0, 0);

  // Cập nhật Progress Bar (tính theo index của section)
  updateProgress(id);
}

function updateProgress(id) {
  const sections = Array.from(document.querySelectorAll('.section'));
  const currentIndex = sections.findIndex(s => s.id === id);
  const percent = ((currentIndex + 1) / sections.length) * 100;
  document.getElementById('progressFill').style.width = percent + '%';
}
```

---

## 4. Content Guidelines

- **Ngôn ngữ**: Tiếng Việt (trừ các thuật ngữ kỹ thuật AI).
- **Tone & Voice**: Chuyên nghiệp, dễ hiểu, mang tính hướng dẫn.
- **Cấu trúc**: Phải có section Intro, các Section nội dung chính, và section Tổng kết/Kiểm tra.
- **Tránh Placeholder**: Nếu cần ví dụ, hãy tạo ví dụ thực tế liên quan đến công việc (Dev, QC, BA).
