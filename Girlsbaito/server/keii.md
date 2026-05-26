# 📋 WORKFLOW GUIDE: HOW TO GENERATE THIS REPORT
*Đây là tài liệu hướng dẫn quy trình (Workflow) để chuyển đổi báo cáo kỹ thuật thành báo cáo sự cố (経緯報告書) chuẩn doanh nghiệp Nhật Bản.*

Khi phát sinh sự cố hệ thống (System Failure / Security Incident), để tạo ra một tài liệu **経緯報告書 (Báo cáo diễn biến sự cố)** có độ tin cậy cao và chuyên nghiệp như trên, hãy tuân theo quy trình 5 bước sau:

### 1. Phân loại cấu trúc thông tin (Information Architecture)
Một báo cáo 経緯報告書 chuẩn Nhật luôn gồm 4 phần cốt lõi được sắp xếp theo trình tự:
* **Mở đầu (Intro):** Đặt tiêu đề trang trọng, ghi rõ ngày nộp, đơn vị nộp. Viết lời xin lỗi sâu sắc (お詫び) vì đã gây ảnh hưởng đến vận hành và khách hàng cuối.
* **Mục 1 (発生した問題と現在の対応状況):** Bảng tổng hợp các sự kiện. Chia cột gồm: *Nội dung lỗi* | *Mức ảnh hưởng khách hàng/doanh nghiệp* | *Tình trạng xử lý hiện tại* | *Ngày xác nhận*.
* **Mục 2 (各問題の原因):** Giải thích nguyên nhân một cách bình dân, dễ hiểu (わかりやすく), tránh thuật ngữ kỹ thuật quá sâu nếu đối tác là Client kinh doanh. Chia cột: *Nội dung lỗi* | *Nguyên nhân trực tiếp + gốc rễ*.
* **Mục 3 (今後の対応スケジュール):** Lộ trình khắc phục chia theo deadline cụ thể (Ngay lập tức, ngắn hạn, trung hạn).
* **Mục 4 (再発防止策):** Các giải pháp phòng ngừa tái phát từ quy trình vận hành và kỹ thuật.

### 2. Sử dụng ngôn từ chuẩn công sở Nhật Bản (Keigo & Business Japanese)
* Tiêu đề chính phải dùng khoảng trắng phân tách: `経　緯　報　告　書` hoặc `以　上` ở cuối trang.
* Lời mở đầu bắt buộc phải dùng các mẫu câu tạ lỗi chuẩn mực:
  * *深くお詫び申し上げます (Xin chân thành tạ lỗi sâu sắc)*
  * *多大なご迷惑とご不便をおかけしましたこと (Đã gây ra những phiền toái và bất tiện to lớn)*
* Khi viết trạng thái, sử dụng các từ khóa đơn giản: `対応中` (Đang xử lý), `対応済` (Đã xử lý xong), `調査・修正中` (Đang điều tra/sửa lỗi).

### 3. Tóm tắt vấn đề dưới dạng bảng (Tabular Summarization)
Markdown hóa các bảng biểu từ file gốc Word. Đảm bảo độ rộng của cột hợp lý và căn lề đúng cách:
* Cột tiêu đề/ID/Ngày: Căn giữa (`:---:`).
* Cột nội dung chi tiết: Căn trái (`:---`) và sử dụng xuống dòng (`<br>`) để phân tách các ý nhỏ cho bảng gọn gàng.

### 4. Quy trình xử lý dữ liệu nhạy cảm
* Trước khi đưa thông tin vào báo cáo, bắt buộc phải rà soát và loại bỏ các IP nội bộ, tài khoản test hoặc dữ liệu không liên quan đến cuộc tấn công thực tế (như đã loại bỏ IP `18.183.48.62` sau khi xác nhận là IP nội bộ).

### 5. Duy trì tính nhất quán trên các nền tảng
* Bất cứ khi nào cập nhật thông tin trong báo cáo diễn biến sự cố (`keii.md`), hãy kiểm tra và đồng bộ hóa các tệp tin báo cáo kỹ thuật liên quan (`bao-cao.md` và `bao-cao.xlsx`) để đảm bảo không bị lệch dữ liệu giữa Dev và Client.
