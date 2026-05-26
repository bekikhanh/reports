# Rule: Technical Specification Visualizer
Role: Senior Tech Lead & UI/UX Architect

---

## 0. Non-Negotiable Output Constraints

> Các ràng buộc dưới đây LUÔN LUÔN được áp dụng cho mọi file spec HTML được tạo ra bởi workflow này.
> Không cần nhắc lại trong prompt. Không có ngoại lệ dù model có giới hạn token.

### 0.1 — Sticky Navigation Bar (BẮT BUỘC có ở mọi output)
- Luôn là thẻ `<nav>` đầu tiên trong `<body>`, trước mọi section nội dung.
- CSS: `position: sticky; top: 0; z-index: 1000; background: #1f2937; border-bottom: 3px solid #F98800;`
- Chứa: tên spec + ngày + anchor link đến tất cả section chính.
- **Bắt buộc thêm `scroll-margin-top: 70px` vào mọi `.screen-section`** để tiêu đề không bị nav che khi click anchor link.
- **Nếu thiếu Sticky Nav hoặc thiếu scroll-margin-top → output bị coi là không hợp lệ, phải làm lại.**

### 0.2 — Browser Mockup phải đầy đủ 100% UI gốc
- Trước khi viết HTML mockup, đếm số field/element trong file source được đọc.
- Mockup phải render đủ số lượng đó — **TUYỆT ĐỐI không được dùng `...`, text thay thế kiểu "以降〜が続きます", hay comment thay thế field**.
- Nếu form gốc có 12 field → mockup phải có đủ 12 field, theo đúng thứ tự.
- **Nếu thiếu bất kỳ field nào hoặc có "..." → output bị coi là không hợp lệ.**

### 0.3 — Highlight thay đổi (BẮT BUỘC)
- **Field/element MỚI thêm**: `border: 2.5px solid #dc2626; box-shadow: 0 0 0 3px rgba(220,38,38,0.12)` + badge `NEW` absolute màu đỏ (top: -12px; left: -2px).
- **Field/element BỊ SỬA**: `border: 2.5px solid #d97706` + badge `MODIFIED` absolute màu cam.
- Badge CSS: `position:absolute; background:[màu]; color:#fff; font-size:10px; font-weight:700; padding:2px 8px; border-radius:4px;`

### 0.4 — Code Diff Block (BẮT BUỘC có với mọi thay đổi code)
- Luôn hiển thị ít nhất **3 dòng context** (màu `#94a3b8`) trước và sau đoạn thay đổi.
- Dòng thêm vào: class `fix-line` (nền xanh lá nhạt).
- Dòng xóa đi: class `highlight-line` (nền đỏ nhạt).
- Ghi rõ file path + số dòng ước tính ở đầu block.

### 0.5 — QA Checklist (BẮT BUỘC ở cuối mọi spec)
- Section cuối cùng trước Summary.
- Dùng component `<ul class="checklist">` với `check-icon yes/warn/skip`.
- Mỗi item checklist phải cụ thể, có thể test được (không viết chung chung).

---

## 1. Presentation Standards

- **Format**: Single-file HTML, self-contained, không dùng framework ngoài (không React, không Vite).
- **Styling**: CSS thuần với CSS Variables (`:root`). Không dùng Tailwind — design system tự viết nhất quán hơn.
- **Fonts**: Google Fonts `Inter` + `Noto Sans JP` (để hiển thị chữ Nhật + Latin).
- **Cấu trúc file**: `<head>` → `<style>` toàn bộ CSS → `</head>` → `<body>` → content.

---

## 2. CSS Design System (Bắt buộc khai báo `:root` với các biến sau)

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Inter', 'Noto Sans JP', sans-serif;
  background: #e5e7eb; color: #000; min-height: 100vh; font-size: 16px; line-height: 1.6;
  overflow-x: hidden;
}
h1, h2, h3, h4, h5, h6, .screen-section { scroll-margin-top: 80px; }
:root {
  --primary: #F98800;         /* Juku orange */
  --primary-light: #FFF2D5;
  --text-1: #000000;
  --text-2: #555555;
  --text-3: #AAAAAA;
  --border: #e2e2e2;
  --bg: #ffffff;
  --red: #dc2626; --red-bg: #fef2f2; --red-border: #fecaca;
  --green: #16a34a; --green-bg: #f0fdf4; --green-border: #bbf7d0;
  --blue: #2563eb; --blue-bg: #eff6ff; --blue-border: #bfdbfe;
}
```

---

## 3. Mandatory UI Components (Các block HTML bắt buộc có)

### 3.1 — Sticky Navigation Bar
```html
<nav class="screen-nav">
  <span class="screen-nav-title">[Tên Spec] ([Ngày])</span>
  <div class="nav-links">
    <a href="#overview" class="nav-btn">概要</a>
    <a href="#change-1" class="nav-btn">変更1</a>
    <a href="#checklist" class="nav-btn">確認</a>
  </div>
</nav>
```
CSS:
```css
.screen-nav { position:sticky; top:0; z-index:1000; background:#1f2937; border-bottom:3px solid var(--primary); padding: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
@media (max-width: 640px) { .screen-nav { flex-direction: column; align-items: flex-start; } }
.screen-nav-title { color: white; font-weight: bold; font-size: 1.1rem; }
.nav-links { display: flex; gap: 10px; flex-wrap: wrap; }
.nav-btn { color: white; text-decoration: none; font-weight: bold; background: #374151; padding: 6px 14px; border-radius: 6px; transition: all 0.2s; border: 1px solid #4b5563; font-size: 0.9rem; }
.nav-btn:hover { background: var(--primary); color: #1f2937; border-color: var(--primary); }
```

### 3.2 — Section Container
```html
<div class="screen-section" id="overview">
  <span class="screen-label orange">概要</span>      <!-- orange | blue | green | red | gray | purple -->
  <h2 class="screen-title">セクションタイトル</h2>
  <p class="screen-desc">説明文...</p>
</div>
```

### 3.3 — White Card Box
```html
<div class="section-box">
  <div class="section-box-header">
    <div class="section-box-title">カードタイトル</div>
  </div>
  <!-- content inside -->
</div>
```

### 3.4 — Browser Mockup (QUAN TRỌNG — dùng để so sánh Before/After)
Luôn đặt trong `.comparison` (2 cột flex), một cột "Before" border đỏ, một cột "After" border xanh.
```html
<div class="comparison">
  <div class="comparison-panel">
    <span class="comparison-label bug">変更前</span>
    <div class="browser-mock">
      <div class="browser-bar">
        <div class="browser-dots"><span class="r"></span><span class="y"></span><span class="g"></span></div>
        <div class="browser-url">https://example.com/target-page/</div>
      </div>
      <div class="browser-body">
        <div style="font-size:48px">⚠️</div>
        <div style="font-size:18px; font-weight:700; color:var(--red)">問題の説明</div>
        <div style="font-size:13px; color:#6b7280">サブテキスト</div>
      </div>
    </div>
  </div>
  <div class="comparison-panel">
    <span class="comparison-label fix">変更後</span>
    <div class="browser-mock">
      <!-- tương tự, nhưng dùng icon 🔒 hoặc ✅ và màu green -->
    </div>
  </div>
</div>
```

### 3.5 — Flow Diagram (Luồng logic / Pipeline)
```html
<div class="flow-diagram">
  <div class="flow-box">
    <div class="flow-label">起点</div>
    <div class="flow-text">GET /page/</div>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-box warn">
    <div class="flow-label">判定</div>
    <div class="flow-text">条件チェック</div>
  </div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-box ok">   <!-- ok=green | blocked=red | warn=orange -->
    <div class="flow-text">通過</div>
  </div>
</div>
```

### 3.6 — Code Block / Diff Block (macOS style)
Mọi khối code (chứa code thường hoặc code diff) BẮT BUỘC phải sử dụng giao diện cửa sổ macOS. Background đồng màu, padding full.
```html
<div class="mac-window">
  <div class="mac-header">
    <div class="mac-buttons">
      <span class="mac-btn close"></span>
      <span class="mac-btn minimize"></span>
      <span class="mac-btn maximize"></span>
    </div>
    <span class="mac-title">src/path/to/file.ts</span>
  </div>
  <pre><code>
<span class="line">// context line</span>
<span class="line remove">// ← dòng bị xóa (đỏ)</span>
<span class="line add">// ← dòng mới (xanh)</span>
  </code></pre>
</div>
```
CSS quan trọng cần thêm vào thẻ `<style>`:
```css
.mac-window { background: #1e1e1e; border-radius: 8px; overflow: hidden; margin: 1.5rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.mac-header { background: #2d2d2d; padding: 10px 16px; display: flex; align-items: center; }
.mac-buttons { display: flex; gap: 8px; width: 60px; }
.mac-btn { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.mac-btn.close { background: #ff5f56; }
.mac-btn.minimize { background: #ffbd2e; }
.mac-btn.maximize { background: #27c93f; }
.mac-title { color: #9ca3af; font-size: 0.85rem; font-family: monospace; flex: 1; text-align: center; margin-right: 60px; }
.mac-window pre { margin: 0; padding: 0.5rem 0; font-family: 'Courier New', monospace; font-size: 0.9rem; color: #e5e7eb; overflow-x: auto; background: transparent; }
.mac-window code { background: transparent; padding: 0; display: block; }
.mac-window .line { display: block; padding: 0 1rem; min-height: 1.5rem; line-height: 1.5rem; }
.mac-window .line.remove { background: rgba(220, 38, 38, 0.2); }
.mac-window .line.add { background: rgba(34, 197, 94, 0.2); }
```

### 3.7 — Annotations (Chú thích màu sắc)
```html
<div class="bug-annotation"><strong>問題:</strong> ...</div>    <!-- đỏ -->
<div class="fixed-annotation"><strong>解決:</strong> ...</div>   <!-- xanh dương -->
<div class="resolved-annotation"><strong>効果:</strong> ...</div> <!-- xanh lá -->
<div class="info-banner"><span class="info-banner-icon">ℹ️</span><div>...</div></div> <!-- xanh nhạt -->
```

### 3.8 — Data Table
```css
.table-responsive { width: 100%; overflow-x: auto; margin-top: 1rem; border-radius: 8px; border: 1px solid var(--border); }
.data-table { width: 100%; border-collapse: separate; border-spacing: 0; min-width: 600px; }
.data-table th, .data-table td { border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); padding: 0.75rem; text-align: left; }
.data-table th:last-child, .data-table td:last-child { border-right: none; }
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table th { background: #1f2937; color: white; font-weight: bold; border-bottom-color: #374151; border-right-color: #374151; }
.data-table tbody tr:nth-child(even) { background: #f9fafb; }
.data-table tbody tr:nth-child(odd) { background: white; }
```
```html
<div class="table-responsive">
  <table class="data-table">
    <thead><tr><th>列1</th><th>列2</th><th>状態</th></tr></thead>
    <tbody>
      <tr>
        <td><span class="file-badge">path/to/file.ts</span></td>
        <td>説明</td>
        <td><span class="status-badge" style="background:#d1fae5; color:#065f46;">実装済み</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

### 3.9 — Step List (Deploy checklist có số tự động)
```html
<ol class="step-list">
  <li><strong>タスク名</strong> — 詳細説明。</li>
  <li>次のタスク。<code>コマンド</code> を実行。</li>
</ol>
```

### 3.10 — Checklist (QA check)
```html
<ul class="checklist">
  <li><span class="check-icon yes">✓</span><div><strong>確認項目</strong></div></li>
  <li><span class="check-icon warn">!</span><div>注意が必要な項目</div></li>
  <li><span class="check-icon skip">-</span><div style="color:#6b7280">対応不要な項目</div></li>
</ul>
```

### 3.11 — Key-Value Row (Thông tin biến môi trường, cấu hình)
```html
<div class="kv-row">
  <div class="kv-key">変数名</div>
  <div class="kv-val"><code>PUBLIC_ENABLE_FEATURE</code></div>
</div>
```

---

## 4. Inline Code Style
- File path ngắn: `<span class="file-badge">src/pages/xxx.astro</span>`
- Inline `<code>`: nền `#f3f3f3`, font mono, padding nhỏ, border-radius 4px.

---

## 5. Content Rules (Quy tắc nội dung)

- **Ngôn ngữ (BẮT BUỘC)**: 100% sử dụng Tiếng Nhật cho TẤT CẢ nội dung hiển thị (heading, label, paragraph, table, chú thích...). TUYỆT ĐỐI KHÔNG sử dụng Tiếng Việt. Hạn chế tối đa Tiếng Anh, chỉ dùng cho các thuật ngữ kỹ thuật (vd: User Panel, API, PR) hoặc tên code.
- **Section Overview**: Luôn có — tóm tắt mục tiêu nghiệp vụ 2-3 câu.
- **Cuối tài liệu**: Luôn có block **Summary Table** (bảng tổng hợp file thay đổi + số dòng thêm/sửa).
- **Không dùng placeholder**: Mọi file path, biến số, tên function phải lấy từ context thực tế.
- **Links/URLs**: KHÔNG ĐƯỢC hiển thị URL thô (raw url) ra màn hình. Mọi URL xuất hiện trong yêu cầu bắt buộc phải được bọc trong thẻ `<a>` với `target="_blank"` và class `external-link`. Text hiển thị phải là text mô tả (ví dụ: `PR #1306 を開く ↗`).
  CSS bắt buộc thêm: `.external-link { display: inline-flex; align-items: center; gap: 4px; background: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.85rem; border: 1px solid #bfdbfe; transition: all 0.2s; } .external-link:hover { background: #dbeafe; }`
