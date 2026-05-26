

**BÁO CÁO SỰ CỐ BẢO MẬT THÔNG TIN**

(Báo cáo tổng hợp xử lý sự cố bảo mật)

Ngày lập báo cáo: 21/05/2026  
**Mức độ nghiêm trọng: Critical (Cao nhất)**

# **1\. Tổng quan sự cố**

| Nội dung | Rò rỉ thông tin .env / .git và các thông tin mật ra bên ngoài |
| :---- | :---- |
| **Thời gian phát hiện** | 21/05/2026 khoảng 13:49 |
| **Phương pháp phát hiện** | Phân tích access log |
| **IP tấn công ①** | 94.26.88.32 (Bot quét tự động) |
| **IP tấn công ②** | 18.183.48.62 (AWS Tokyo \- đăng nhập SSH root trái phép) |
| **Phạm vi ảnh hưởng** | Rò rỉ .env và .git, rò rỉ thông tin cá nhân qua laravel.log (34 người), cài mã độc |

# **2\. Nguyên nhân xảy ra sự cố**

## **2-1. Nguyên nhân trực tiếp**

- Cấu hình nginx sai: thư mục .env và .git có thể truy cập từ bên ngoài

- Document root trỏ đến project root nên storage/logs/laravel.log cũng bị lộ ra ngoài

- SQL tải cao (query tìm kiếm girlsbaito) làm tăng nguy cơ lỗ hổng bảo mật

- Bot quét tự động (IP: 94.26.88.32) gửi hàng loạt request đến .git và .env

## **2-2. Nguyên nhân gốc rễ**

- Chưa cài đặt cấu hình chặn file ẩn (location \~ /\\.) trong nginx

- File .env chưa được thêm vào .gitignore, bị quản lý bởi Git

- Khi nâng cấp server, file laravel.log cũ (7.2GB) được chuyển sang server mới

- Chưa có quy trình kiểm tra bảo mật khi deploy và review bảo mật định kỳ

# **3\. Chi tiết sự cố**

## **3-1. Rò rỉ thông tin .env / .git**

| Thông tin bị rò rỉ | Nội dung | Mức độ nguy hiểm |
| :---- | :---- | ----- |
| APP\_KEY | Khóa mã hóa của Laravel | 🔴 Cao nhất |
| DB\_PASSWORD / DB\_USERNAME | Thông tin kết nối cơ sở dữ liệu | 🔴 Cao nhất |
| GOOGLE\_CLIENT\_SECRET | Google OAuth secret key | 🔴 Cao nhất |
| Google Refresh Token | Quyền truy cập Google API vĩnh viễn | 🔴 Cao nhất |
| Thông tin .git repository | Toàn bộ source code và lịch sử commit | 🟡 Cao |

## **3-2. Rò rỉ thông tin cá nhân qua laravel.log**

| File bị rò rỉ | /www/girls-baito-production/storage/logs/laravel.log (7.2GB) |
| :---- | :---- |
| **Thời gian ghi log** | Tháng 10/2022 đến 24/06/2025 (log từ server cũ XSERVER) |
| **Dung lượng bị tải xuống** | 474MB / 7.2GB (khoảng 6.6%) |
| **Đối tượng tải xuống** | 212.86.126.157 (tải 367MB ngày 05/04/2026, xác định là bot quét 1 lần) |
| **Ngày chặn truy cập** | 20/05/2026 (đã xử lý bằng cách thay đổi cấu hình nginx) |

**Thông tin bị rò rỉ**

- Họ tên và địa chỉ email của người dùng

- Mật khẩu dạng hash (bcrypt) \- khó bị lợi dụng ngay, nhưng mật khẩu yếu có nguy cơ bị tấn công từ điển

- Số điện thoại (một phần)

- Trạng thái tài khoản

**Đối tượng bị ảnh hưởng**

| Loại người dùng | Số lượng | Ghi chú |
| :---- | ----- | :---- |
| Hội viên thường (role=1) | 5 người |  |
| Quản trị viên cửa hàng (role=2) | 28 người | Nhiều nhất |
| Quản trị viên vận hành (role=4) | 1 người |  |
| Tài khoản thử nghiệm | 1 người | Không xử lý |
| **Tổng cộng** | **34 người / tổng 11.892 người (0,29%)** |  |

## **3-3. Dấu vết mã độc (Malware) trên server**

**Phát hiện**

- Tìm thấy file thực thi ELF và shell script trong thư mục /var/tmp/ trên server production

- Mã độc đã thêm các entry vào crontab để tự động chạy mỗi phút, mỗi ngày, khi khởi động lại

**Dòng thời gian (Timeline)**

| Ngày | Sự kiện |
| :---: | :---- |
| 27/01/2026 | Mã độc xâm nhập lần đầu \+ Đăng nhập SSH root trái phép (10:22\~11:09) từ IP 18.183.48.62 |
| 10/03/2026 | Thêm thư mục mới (/var/tmp/8fbb119f/ được tạo) |
| 12/03/2026 | Thêm và cập nhật loader script |
| 14/03/2026 | Server khởi động lại (ước tính từ uptime) |
| 05/04/2026 | 367MB từ laravel.log bị tải xuống từ bên ngoài |
| 20/05/2026 | Chặn truy cập laravel.log bằng cách thay đổi cấu hình nginx |
| 21/05/2026 | Phát hiện sự cố, bắt đầu điều tra, lập báo cáo này |

**Tình trạng hiện tại**

- Mã độc hiện tại KHÔNG hoạt động (CPU, bộ nhớ, kết nối mạng đều bình thường)

- Các file đã được bảo toàn, có thể thực hiện điều tra forensic

- Không phát hiện tài khoản backdoor nào trong MySQL

- Hành động của kẻ tấn công trong \~6 tuần hoạt động (27/01 \~ 12/03) chưa xác định được (cần điều tra thêm)

## **3-4. Đăng nhập SSH root trái phép**

| Địa chỉ IP | 18.183.48.62 |
| :---- | :---- |
| **Nguồn kết nối** | AWS Tokyo Region (ap-northeast-1) |
| **Thời gian kết nối** | 27/01/2026 từ 10:22 đến 11:09 (khoảng 47 phút) |
| **Phương thức xác thực** | Xác thực khóa công khai (ED25519) |
| **Lưu ý quan trọng** | Trùng ngày mã độc xâm nhập lần đầu \=\> Kết nối SSH này rất có thể là nguồn gốc của toàn bộ sự cố |

# **4\. Danh sách công việc cần xử lý (Ưu tiên & Trạng thái)**

## **① Cấp lại thông tin xác thực**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Tạo lại APP\_KEY | php artisan key:generate | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Cấp lại GOOGLE\_CLIENT\_SECRET | Vô hiệu hóa và cấp lại trên Google Cloud Console | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Vô hiệu hóa Google Refresh Token | Vô hiệu hóa token trên tài khoản Google | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Đổi DB\_PASSWORD | Quản trị viên DB thay đổi bằng ALTER USER | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |

## **② Sửa cấu hình Web Server (nginx)**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Thêm cấu hình chặn file ẩn vào nginx | location \~ /\\. { deny all; return 404; } | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Xóa dòng cấu hình hệ thống wvp không rõ nguồn gốc | Xóa dòng include trong nginx.conf | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Reload nginx sau khi sửa | nginx \-t \=\> systemctl reload nginx | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |

## **③ Tăng cường bảo mật MySQL nhiều lớp**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Đổi gbaito@% thành gbaito@localhost | Tạo user mới, cấp quyền, xóa user cũ (khung giờ đêm) | 🟡 Cao | 🟡 Cao | \[ \] Chưa xử lý |
| Xác nhận hoàn thành và báo cáo kết quả | SELECT User, Host FROM mysql.user | 🟡 Cao | 🟡 Cao | \[ \] Chưa xử lý |

## **④ Xử lý rò rỉ thông tin cá nhân (laravel.log)**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Bắt buộc 34 người dùng bị ảnh hưởng đổi mật khẩu | Reset mật khẩu qua trang quản trị hoặc DB trực tiếp | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Thông báo rò rỉ thông tin cá nhân đến 34 người | Gửi email thông báo, yêu cầu đổi mật khẩu | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Di chuyển / xóa file laravel.log | Bảo toàn file trước, sau đó di chuyển ra ngoài vùng public | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Thêm storage/logs/ vào .gitignore | git rm \--cached để xóa khỏi lịch sử Git | 🟡 Cao | 🟡 Cao | \[ \] Chưa xử lý |

## **⑤ Xử lý mã độc (Malware)**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Bảo toàn và xóa file mã độc trong /var/tmp/ | Bảo toàn bằng chứng, sau đó rm \-rf để xóa | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Xóa các entry đáng ngờ trong crontab | Chỉnh sửa bằng crontab \-e | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Điều tra Forensic | Xác định hành động trong 6 tuần mã độc hoạt động | 🟡 Cao | 🟡 Cao | \[ \] Chưa xử lý |
| Vô hiệu hóa đăng nhập SSH bằng root | Thiết lập PermitRootLogin no, khởi động lại sshd | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |

## **⑥ Xử lý truy cập SSH trái phép**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Chặn IP 18.183.48.62 bằng tường lửa | Cấu hình iptables hoặc Security Group | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Chặn IP 94.26.88.32 bằng tường lửa | Cấu hình iptables hoặc Security Group | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Kiểm tra SSH log và bash\_history | Xem auth.log và /root/.bash\_history | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Xóa khóa công khai lạ trong authorized\_keys | Kiểm tra và xóa khóa công khai không rõ nguồn gốc | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |

## **⑦ Xử lý Git / Source code**

| Nội dung công việc | Cách thực hiện | Ưu tiên | Khẩn cấp | Trạng thái |
| ----- | ----- | :---: | :---: | :---: |
| Thêm .env vào .gitignore | echo ".env" \>\> .gitignore | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |
| Xóa .env khỏi lịch sử Git | git rm \--cached .env \=\> commit | 🔴 Cao nhất | 🔴 Cao nhất | \[ \] Chưa xử lý |

# **5\. Lịch trình xử lý khuyến nghị**

| Thời gian | Nội dung công việc |
| :---: | :---- |
| **Trong ngày hôm nay** | Xóa khóa công khai lạ, vô hiệu SSH root, bảo toàn & xóa mã độc, xóa crontab, chặn 2 IP, sửa cấu hình nginx, tạo lại APP\_KEY, vô hiệu hóa Google OAuth token |
| **Khung giờ ít truy cập (đêm)** | Tăng cường bảo mật MySQL (gbaito@% \=\> localhost), đổi DB\_PASSWORD |
| **Trong vài ngày tới** | Bắt buộc 34 người đổi mật khẩu, thông báo rò rỉ thông tin cá nhân, điều tra forensic, nộp bản báo cáo chính thức |
| **Trong vòng 1 tháng** | Quét lỗ hổng bảo mật, pen test, đào tạo bảo mật cho team, áp dụng công cụ quản lý secret (AWS Secrets Manager, HashiCorp Vault...) |

# **6\. Biện pháp phòng ngừa tái phát**

## **6-1. Thực hiện ngay**

- Chuẩn hóa cấu hình chặn file ẩn trong nginx (location \~ /\\.)

- Bắt buộc thêm .env vào .gitignore, không để Git quản lý

- Vô hiệu hóa đăng nhập SSH bằng root (PermitRootLogin no)

- Chỉ cho phép xác thực bằng khóa công khai, định kỳ review authorized\_keys

## **6-2. Trung hạn**

- Áp dụng công cụ quản lý secret (AWS Secrets Manager, HashiCorp Vault...)

- Thêm kiểm tra bảo mật vào CI/CD pipeline (Pre-commit hook...)

- Định kỳ quét lỗ hổng bảo mật (hàng tháng)

- Triển khai WAF (Web Application Firewall)

## **6-3. Xây dựng quy trình**

- Soạn thảo tài liệu hướng dẫn xử lý sự cố bảo mật

- Đào tạo bảo mật cho đội ngũ phát triển

- Xây dựng checklist kiểm tra bảo mật khi deploy

Báo cáo này được lập dựa trên các sự kiện đã được xác minh. Nội dung có thể được cập nhật thêm khi có kết quả điều tra bổ sung.  
Ngày lập: 21/05/2026     Mức độ: Critical (Cao nhất)     Trạng thái: Đang xử lý