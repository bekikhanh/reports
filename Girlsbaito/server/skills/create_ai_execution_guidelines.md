# Skill: Tạo file `ai_execution_guidelines.md` cho Dự án

**Mục tiêu của Skill này:**
Hướng dẫn AI quét codebase, đọc file cấu hình thực tế, và phỏng vấn user để tạo ra một file `.antigravity/rules/ai_execution_guidelines.md` chính xác, phản ánh đúng công cụ và lệnh thực tế của từng dự án (không phụ thuộc vào ngôn ngữ hay framework).

---

## 1. Triết lý của file này

File `ai_execution_guidelines.md` **không phải là tài liệu chung chung** về best practice. Nó là **tập hợp các lệnh cụ thể, có địa chỉ thực tế** mà AI được phép hoặc bị cấm chạy trong dự án này. Một file tốt cần:

- **Lệnh phải copy-paste được ngay:** Không có placeholder trừu tượng như `<your-command>`. Phải là lệnh thật, chạy được.
- **Phân loại rõ ràng 3 nhóm lệnh:**
  - `TUYỆT ĐỐI KHÔNG`: AI không được tự động chạy, chỉ được in ra cho user.
  - `PHẢI HỎI user trước`: AI phải xin phép trước khi chạy.
  - `Tự chạy an toàn`: AI có thể chạy mà không cần hỏi.
- **Gắn với công cụ thực tế:** Docker Compose, Make, npm, Artisan, Gradle... tùy dự án.

---

## 2. Quy trình AI thực hiện (Step-by-step)

### Bước 1: Phỏng vấn User

Đặt **một lần duy nhất** tất cả các câu hỏi sau. Không hỏi lại từng câu rời rạc:

**Nhóm A - Môi trường chạy lệnh:**
- Dự án có dùng Docker Compose không? Nếu có, service chính (chứa app code) tên là gì? (vd: `app`, `web`, `backend`)
- Dự án có file `Makefile` không? Nếu có, đây là nơi wrap các lệnh chính?
- Ngoài Docker/Make, có công cụ nào khác để chạy lệnh không? (vd: `npm scripts`, `rake`, `gradle`, `just`...)

**Nhóm B - Quản lý Package:**
- Package manager dự án này dùng là gì? (vd: `composer`, `npm`/`yarn`/`pnpm`, `pip`/`poetry`/`uv`, `go get`, `cargo`, `bundler`...)
- Có lệnh cụ thể để thêm/xóa package không? (vd: `composer require`, `npm install`)

**Nhóm C - Database Migration:**
- Tool quản lý migration là gì? (vd: `Artisan migrate`, `Alembic`, `Flyway`, `Sequelize`, `Knex`, `Rails db:migrate`...)
- Lệnh tạo migration mới? Lệnh chạy migration? Lệnh rollback?

**Nhóm D - Linter & Formatter:**
- Tool linting/formatting là gì? (vd: `PHP-CS-Fixer`, `ESLint+Prettier`, `Ruff+Black`, `gofmt`, `rustfmt`...)
- Lệnh chạy cho toàn dự án? Có thể chạy cho 1 file cụ thể không?

**Nhóm E - Testing:**
- Framework test là gì? (vd: `PHPUnit`, `Jest`, `pytest`, `go test`, `RSpec`, `JUnit`...)
- Lệnh chạy toàn bộ test? Chạy 1 file test cụ thể?

**Nhóm F - Quy tắc đặc biệt của team:**
- Có lệnh nào AI tuyệt đối không được chạy không? (vd: lệnh ảnh hưởng production DB, lệnh deploy...)
- Có workflow đặc biệt nào sau khi hoàn thành task không? (vd: ghi changelog, chạy format bắt buộc...)

---

### Bước 2: Tự đọc Codebase (Song song với Bước 1)

AI tự động thực hiện để bổ sung thông tin thiếu:

**2a. Xác định môi trường chạy lệnh:**
```
list_dir(root_directory)             # Tìm Makefile, docker-compose.yml, package.json, etc.
view_file("docker-compose.yml")      # Đọc tên service
view_file("Makefile")                # Đọc tất cả các target có sẵn
```

**2b. Xác định package manager:**
```
# Kiểm tra file đặc trưng:
# PHP:    composer.json
# JS:     package.json (npm/yarn/pnpm scripts)
# Python: pyproject.toml, requirements.txt, Pipfile
# Go:     go.mod
# Ruby:   Gemfile
# Rust:   Cargo.toml
```

**2c. Tìm lệnh linter/formatter:**
```
grep_search("cs-fixer\|phpstan\|eslint\|prettier\|ruff\|black\|gofmt", Includes=["Makefile", "package.json", ".github/**/*.yml"])
```

**2d. Tìm lệnh test:**
```
grep_search("artisan test\|phpunit\|jest\|pytest\|go test\|rspec", Includes=["Makefile", "package.json", ".github/**/*.yml"])
```

**2e. Xem CI/CD pipeline (nếu có):**
```
list_dir(".github/workflows/")       # Xem các lệnh chạy trong CI
```
→ CI thường chứa lệnh chính xác nhất mà team đang dùng.

---

### Bước 3: Tổng hợp và Viết file

Viết file tại `.antigravity/rules/ai_execution_guidelines.md` theo cấu trúc bên dưới.

---

## 3. Cấu trúc chuẩn của file `ai_execution_guidelines.md` đầu ra

```markdown
# Hướng dẫn Thực thi Lệnh Dành cho AI (AI Execution Guidelines)

File này định nghĩa các lệnh chuẩn mà AI BẮT BUỘC phải dùng để thao tác với dự án [TÊN DỰ ÁN] một cách an toàn và nhất quán.

## 1. Nguyên tắc cốt lõi
[Mô tả ngắn: Dự án chạy lệnh bằng công cụ gì? Docker Compose? Makefile? npm scripts? Hay chạy trực tiếp?]
[Quy tắc chung: Ví dụ "Mọi lệnh phải chạy qua `docker compose exec app` để đúng môi trường".]

---

## 2. Quản lý Package / Thư viện
[Package manager là gì, lệnh thêm/xóa/cập nhật package]

**QUY TẮC:** AI [TUYỆT ĐỐI KHÔNG / CÓ THỂ] tự chạy các lệnh này.

- **Cài toàn bộ dependencies:**
  `[lệnh thực tế, vd: make composer-install / npm install / poetry install]`
- **Thêm package mới:**
  `[lệnh thực tế, vd: docker compose exec app composer require vendor/package]`
- **Xóa package:**
  `[lệnh thực tế]`

---

## 3. Linter & Formatter (Bắt buộc sau khi sửa code)
Mỗi khi AI sửa đổi bất kỳ file [.php / .ts / .py / .go]... nào, phải chạy format trước khi kết thúc lượt:

**QUY TẮC:** AI CÓ THỂ tự chạy các lệnh format này (đây là lệnh an toàn, không thay đổi data).

- **Chạy Linter/Formatter cho toàn dự án:**
  `[lệnh thực tế, vd: make format]`
- **Chạy cho một file/thư mục cụ thể:**
  `[lệnh thực tế, vd: docker compose exec app vendor/bin/php-cs-fixer fix app/Services/MyService.php]`

---

## 4. Quản lý Cơ sở dữ liệu (Migration)
Bất cứ khi nào AI chỉnh sửa các file Model/Schema, bắt buộc phải nhắc user tạo/chạy migration.

**QUY TẮC NGHIÊM NGẶT:** AI TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ ĐỘNG CHẠY các lệnh migration. Chỉ được in lệnh ra màn hình và yêu cầu User tự thao tác.

Các lệnh tham khảo (để in ra cho User):
- **Tạo migration mới:**
  `[lệnh thực tế]`
- **Chạy migration:**
  `[lệnh thực tế]`
- **Rollback:**
  `[lệnh thực tế]`
- **Gotcha:** [Ghi chú đặc thù nếu cần kiểm tra file migration thủ công]

---

## 5. Chạy Tests
Mỗi khi viết logic mới hoặc refactor code, phải chạy test tương ứng:

**QUY TẮC:** AI CÓ THỂ tự chạy test (đây là lệnh chỉ đọc, không thay đổi data production).

- **Chạy toàn bộ test:**
  `[lệnh thực tế, vd: make test / npm test / docker compose exec app php artisan test]`
- **Chạy test cho 1 file cụ thể:**
  `[lệnh thực tế, vd: docker compose exec app php artisan test --filter=MyServiceTest]`

---

## 6. [Mục đặc thù của dự án nếu cần]
[Ví dụ: Lệnh Generate Swagger docs, lệnh clear cache, lệnh chạy queue worker...]

---

## 7. Ghi Log Changelog (Quy trình chốt Task)
Sau khi User báo "Hoàn thành Task X", AI NÊN đề xuất tạo file ghi lại nhật ký:
`Tạo file: /.antigravity/bu_change_logs/YYYY-MM-DD_Ten_Task.md` và tóm tắt ngắn gọn các file đã sửa, logic đã thay đổi.
```

---

## 4. Quy tắc phân loại lệnh (Quan trọng)

| Loại lệnh | Ví dụ | AI làm gì? |
|---|---|---|
| **Hủy hoại dữ liệu** | migrate fresh, db:seed, drop table | IN LỆNH RA, không tự chạy |
| **Cài đặt thư viện** | composer require, npm install | HỎI user trước |
| **Deploy / Release** | git push production, ecs deploy | TUYỆT ĐỐI không tự chạy |
| **Format / Lint** | php-cs-fixer, eslint --fix | TỰ CHẠY được |
| **Test (không production)** | phpunit, jest, pytest | TỰ CHẠY được |
| **Đọc trạng thái** | migrate status, npm list | TỰ CHẠY được |
| **Clear cache** | artisan cache:clear, redis flush | TỰ CHẠY được (nếu môi trường dev) |

---

## 5. Kiểm tra chất lượng trước khi lưu

- [ ] Mọi lệnh đều là lệnh thực tế, copy-paste chạy được ngay (không có `<placeholder>`)
- [ ] Đã phân loại rõ 3 nhóm: KHÔNG chạy / HỎI trước / Tự chạy an toàn
- [ ] Có lệnh chạy linter/formatter cụ thể (tên tool + lệnh thực tế)
- [ ] Có lệnh test cụ thể (chạy toàn bộ + chạy 1 file)
- [ ] Lệnh migration nằm ở nhóm "KHÔNG TỰ CHẠY"
- [ ] Lệnh cài package nằm ở nhóm "PHẢI HỎI trước"
- [ ] Không có nội dung copy từ dự án khác (tên dự án, đường dẫn... phải đúng với dự án hiện tại)

---

## 6. Lưu file và thông báo

Sau khi tạo xong:
1. Lưu file tại `.antigravity/rules/ai_execution_guidelines.md`.
2. Cập nhật phần `Quy tắc Thực thi Lệnh` trong `AGENTS.md` ở thư mục gốc để tham chiếu sang file này.
3. Thông báo cho user các mục đã điền đầy đủ và mục nào cần user xác nhận thêm.
