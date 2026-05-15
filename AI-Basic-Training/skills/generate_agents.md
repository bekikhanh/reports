# Skill: Tạo file AGENTS.md cho Dự án

**Mục tiêu của Skill này:**
Hướng dẫn AI thu thập đầy đủ thông tin từ codebase thực tế và phỏng vấn user để tạo ra một file `AGENTS.md` chất lượng cao, phản ánh đúng đặc thù dự án, áp dụng được cho mọi tech stack (frontend, backend, mobile, fullstack...).

---

## 1. Triết lý của một AGENTS.md tốt

Một file `AGENTS.md` không phải là tài liệu mô tả project cho con người đọc, mà là **tập hợp các ràng buộc và ngữ cảnh** giúp AI coding assistant hoạt động như một thành viên thực sự của team. Một AGENTS.md tốt cần đạt được:

- **Cụ thể hơn là chung chung:** Thay vì "Luôn xử lý lỗi đúng cách", cần viết "Luôn dùng `AppError` class tại `src/lib/errors.ts`, không throw Error gốc".
- **Gắn với codebase thực tế:** Mọi quy ước phải kèm đường dẫn file hoặc ví dụ cụ thể từ code thật.
- **Ngắn gọn và có thể hành động được (Actionable):** Mỗi mục phải trả lời được câu hỏi "AI cần làm gì cụ thể?".
- **Không thừa, không thiếu:** Chỉ ghi những điều mà nếu AI không biết sẽ gây ra lỗi hoặc vi phạm pattern của team. Bỏ qua những gì đã là best practice phổ quát.

---

## 2. Quy trình AI thực hiện (Step-by-step)

### Bước 1: Phỏng vấn User (Bắt buộc)

Trước khi đọc code, AI cần hỏi user một lượt để thu thập thông tin không thể tự suy ra từ code. Đặt tối đa **một lần** với tất cả câu hỏi sau (không hỏi nhiều lần riêng lẻ):

**Nhóm A - Ngữ cảnh Dự án:**
- Tên dự án và mô tả ngắn về sản phẩm là gì?
- Các bên liên quan là ai? (Ví dụ: Client cuối, đơn vị outsource, team nội bộ)
- Có bao nhiêu môi trường triển khai? Mỗi môi trường tương ứng với nhánh Git nào? (Ví dụ: dev → branch `develop`, staging → branch `stg`, prod → branch `main`)
- Ai là người review code cuối cùng? (Techlead, Senior, hay tự merge?)

**Nhóm B - Quy ước Nhóm:**
- Ngôn ngữ giao tiếp với AI là gì? (Tiếng Việt, Anh, Nhật...)
- Ngôn ngữ viết comment bên trong source code là gì?
- Quy ước commit message: Conventional Commits (`feat:`, `fix:`...) hay tự do?
- Có công cụ linter/formatter cụ thể nào không? (ESLint + Prettier, Ruff, Black, gofmt...) Lệnh chạy là gì?

**Nhóm C - Kiến trúc & Đặc thù:**
- Tech stack chính là gì? (Framework, ngôn ngữ, ORM/Database, State management...)
- Cấu trúc thư mục có quy ước đặc biệt gì không? (Ví dụ: feature-based, layer-based)
- Có các pattern bắt buộc nào không? (Ví dụ: bắt buộc dùng Repository pattern, Factory, Context API...)
- Có external service nào thường xuyên tích hợp không? (AWS S3, Stripe, Firebase, Sendgrid...)
- Có quy tắc đặc biệt về migration DB hay schema không?

**Nhóm D - Điều cần tránh (Quan trọng):**
- Có những lệnh Terminal nào AI tuyệt đối không được tự chạy? (Ví dụ: migration, deploy, seed production data)
- Có file hoặc thư mục nào tuyệt đối không được sửa trực tiếp?

---

### Bước 2: Tự đọc Codebase

Sau khi có câu trả lời từ user, AI tự động thực hiện các bước sau để bổ sung thông tin còn thiếu:

**2a. Khám phá cấu trúc dự án:**
```
list_dir(root_directory)          # Xem cấu trúc thư mục gốc
list_dir(src_directory)           # Xem cấu trúc thư mục source chính
```

**2b. Đọc file cấu hình nhanh:**
- `package.json` / `pyproject.toml` / `go.mod` / `pubspec.yaml` → Xác định dependencies, scripts
- `.eslintrc` / `ruff.toml` / `.prettierrc` → Xác định linter config
- `Dockerfile` / `docker-compose.yml` → Xác định các service liên quan
- `README.md` → Đọc tổng quan nếu có

**2c. Tìm các pattern bắt buộc:**
```
grep_search("throw new")          # Pattern xử lý lỗi (JS/TS)
grep_search("raise ")             # Pattern xử lý lỗi (Python)
grep_search("useQuery\|useMutation") # Pattern data fetching (React)
grep_search("@Injectable\|@Component") # Pattern DI (Angular/NestJS)
grep_search("router\.\|app\.")    # Pattern routing (Express/FastAPI)
```

Tìm bất kỳ pattern nào xuất hiện >= 3 lần trong codebase → đó là convention của team, phải ghi vào AGENTS.md.

**2d. Tìm file auth/permission tiêu biểu:**
```
grep_search("middleware\|guard\|auth\|permission", Includes=["*.ts", "*.py", "*.go"])
```
Đọc 1-2 file để hiểu cách phân quyền hoạt động, ghi tên helper/decorator/HOC cụ thể.

**2e. Kiểm tra thư mục tests (nếu có):**
- Tìm hiểu framework test đang dùng (Jest, pytest, go test, Vitest...)
- Ghi nhận convention đặt tên file test (`*.spec.ts`, `*_test.go`, `test_*.py`...)

---

### Bước 3: Tổng hợp và Viết AGENTS.md

Viết file `AGENTS.md` tại **thư mục gốc của project** với cấu trúc sau:

---

## 3. Cấu trúc chuẩn của file AGENTS.md đầu ra

```markdown
# Hướng dẫn cho AI Coding Assistant (AGENTS.md)

## Nguyên tắc chung
[Các quy tắc áp dụng cho MỌI tác vụ AI thực hiện trong project này]
1. **Ngôn ngữ giao tiếp:** [Ngôn ngữ AI dùng khi trả lời user]
2. **Phong cách làm việc:** [Tông văn bản, cách trình bày, bắt đầu bằng Plan...]
3. **Tóm tắt công việc:** [Sau khi hoàn thành, phải chốt lại gì]
4. **Cấu hình hệ thống chung:** [Timezone, locale, i18n nếu có]
5. **Quy ước Commit Git:** [Conventional Commits hay tự do, ngôn ngữ commit]
6. **Quy ước Comment trong Code:** [Ngôn ngữ, style của comment]

## Thông tin Dự án & Quy trình Triển khai
- **Tên dự án:** [...]
- **Mô tả ngắn:** [...]
- **Các bên liên quan:**
  - [Tên]: [Vai trò]
- **Môi trường & Nhánh Git:**
  - **[Tên môi trường] ([tên nhánh]):** [Mục đích, ai dùng]

## Nhân sự & Vai trò
- **[Vai trò]:** [Mô tả ngắn, quyền hạn trong dự án]

## Kiến trúc dự án (Tech Stack)
- **Ngôn ngữ:** [...]
- **Framework chính:** [...]
- **Database / ORM:** [...]
- **State Management (nếu có):** [...]
- **Styling:** [...]
- **Cấu trúc thư mục chính:** [Mô tả từng thư mục quan trọng, vai trò và quy tắc]
- **Quy ước đặt tên:** [File, component, function, biến...]
- **Quy ước kiến trúc bắt buộc:** [Pattern nào phải tuân thủ]

## Best Practices tại dự án này
1. **Bảo mật & Phân quyền:** [Helper/decorator/HOC cụ thể phải dùng]
2. **Xử lý Lỗi:** [Class/function cụ thể, không hardcode message ra sao]
3. **Data Fetching / Database:** [Pattern truy vấn, connection pool, transaction]
4. **Async / Side Effects:** [Cách xử lý async, background job, queue]
5. **Linter & Formatter:** [Lệnh chạy cụ thể]
6. **Testing:** [Framework, convention đặt tên, cách chạy test]
7. **[Best practice đặc thù khác của dự án]**

## Quy tắc Thực thi Lệnh (AI Execution Guidelines)
[Danh sách lệnh ĐƯỢC và KHÔNG ĐƯỢC phép chạy]
- **TUYỆT ĐỐI KHÔNG chạy:** [migration, deploy, seed, drop database...]
- **PHẢI hỏi user trước khi chạy:** [install package, thay đổi env...]
- **Có thể tự chạy an toàn:** [lint, format, test đơn lẻ...]
- Tham khảo chi tiết tại: `/.antigravity/rules/ai_execution_guidelines.md` (nếu có)

## Chiến lược Tối ưu hóa (Token Saving & Hiệu quả)
1. **Chỉ đọc vùng cần thiết:** Dùng `StartLine`/`EndLine` khi đọc file lớn.
2. **Tận dụng Search:** Dùng `grep_search` thay vì đọc toàn bộ thư mục.
3. **Thay thế cục bộ:** Dùng `replace_file_content` thay vì viết lại cả file.
4. **Hỏi trước khi sửa lớn:** Nếu thay đổi ảnh hưởng > 3 file, xin ý kiến user trước.
5. **Dọn dẹp sau khi hoàn thành:** Xóa file tạm, script debug... Chỉ tạo scratch trong `.antigravity/scratch/`.
[Thêm các tip đặc thù cho tech stack của dự án nếu cần]

## Thông tin Hệ thống Quan trọng (System Context)
[Mô tả các tài liệu nội bộ quan trọng AI phải đọc trước khi làm tính năng]
- Tài liệu nghiệp vụ: `/.antigravity/bu_logics/init.md` (nếu có)
- Endpoints reference: `/.antigravity/bu_logics/endpoints.md` (nếu có)
- Execution guidelines: `/.antigravity/rules/ai_execution_guidelines.md` (nếu có)
```

---

## 4. Quy tắc chất lượng khi viết AGENTS.md

### Quy tắc PHẢI:
- Mọi tool/helper/function được đề cập phải kèm **tên cụ thể** (ví dụ: `useAuthGuard()`, không phải "hàm kiểm tra auth").
- Mọi thư mục/file được đề cập phải kèm **đường dẫn tương đối** từ root (ví dụ: `src/hooks/`, không phải "thư mục hooks").
- Mỗi best practice phải trả lời được "AI cần làm GÌ cụ thể khi gặp tình huống đó".
- Phần "Quy tắc Thực thi Lệnh" **bắt buộc phải có** và liệt kê rõ ràng dù project nhỏ.

### Quy tắc KHÔNG ĐƯỢC:
- Không viết những điều hiển nhiên đã là best practice chung (ví dụ: "Hãy viết code sạch").
- Không dùng các icon emoji kiểu 🚀, 💡... làm mất tính chuyên nghiệp.
- Không tự sáng tác quy ước nếu codebase không có bằng chứng.
- Không viết quá dài — mỗi mục nên đủ để AI hiểu và hành động, không cần giải thích dài dòng.

---

## 5. Điều chỉnh theo Tech Stack

Tùy vào tech stack, bổ sung thêm các phần đặc thù sau vào mục **Kiến trúc** và **Best Practices**:

### Frontend (React / Next.js / Vue / Nuxt)
- Quy ước quản lý state: Context API / Zustand / Pinia / Redux — file nào là store chính
- Quy ước component: Atomic Design? Feature-based? File `index.ts` barrel export?
- Quy ước routing: App Router / Pages Router / file-based routing
- Quy ước CSS/Styling: CSS Modules, Tailwind, Styled-components — class naming convention
- Quy ước data fetching: SWR, React Query, `fetch` trong Server Component, tRPC...
- Quy tắc SSR/SSG: Trang nào render server-side, trang nào static?

### Backend (Node.js Express/Fastify, Python FastAPI/Django, Go, Java Spring)
- Cấu trúc layer: Controller → Service → Repository hay MVC?
- Quy ước dependency injection (nếu có framework hỗ trợ)
- Quy ước transaction: Khi nào dùng transaction, rollback thế nào
- Quy ước migration: Tool nào, lệnh nào bị cấm tự chạy
- Quy ước naming: Route pattern, model naming, enum naming

### Mobile (React Native / Flutter)
- Quy ước navigation: Stack, Tab, Drawer — file config ở đâu
- Quy ước state: Provider, Bloc, Riverpod, Redux...
- Platform-specific code: Tổ chức `.android`/`.ios` folders thế nào
- Quy ước asset: Font, image, icon — import qua barrel hay trực tiếp

### Fullstack Monorepo (Turborepo, Nx, pnpm workspaces)
- Cấu trúc packages: `apps/`, `packages/`, `libs/` — vai trò từng nhóm
- Quy ước shared code: Type, util, UI component nào được shared
- Quy ước build: Chạy lệnh từ root hay từng package
- Dependency graph: Package nào phụ thuộc package nào

---

## 6. Kiểm tra chất lượng trước khi lưu

Trước khi lưu file AGENTS.md, AI tự kiểm tra checklist sau:

- [ ] Có phần "Nguyên tắc chung" với ngôn ngữ giao tiếp và phong cách làm việc rõ ràng
- [ ] Có phần "Thông tin Dự án" với môi trường và nhánh Git
- [ ] Có phần "Kiến trúc" với cấu trúc thư mục cụ thể, mỗi thư mục có giải thích vai trò
- [ ] Có ít nhất 3 Best Practice gắn với code thực tế (tên function/class cụ thể, không chung chung)
- [ ] Có phần "Quy tắc Thực thi Lệnh" với danh sách lệnh bị cấm rõ ràng
- [ ] Có phần "Token Saving" với ít nhất 4-5 quy tắc thực tế
- [ ] Không có icon emoji không cần thiết
- [ ] Không có nội dung tự sáng tác không có cơ sở từ codebase

---

## 7. Lưu file và thông báo

Sau khi tạo xong:
1. Lưu file tại **thư mục gốc** của dự án với tên `AGENTS.md`.
2. Thông báo cho user danh sách các phần đã điền đầy đủ và các phần nào cần user bổ sung thêm thông tin.
3. Nếu project có file `.antigravity/rules/ai_execution_guidelines.md`, kiểm tra xem các lệnh trong đó có khớp với phần "Quy tắc Thực thi Lệnh" không. Nếu không, hỏi user để điều chỉnh.
