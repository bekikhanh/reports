# BÁO CÁO TỔNG HỢP & PHÂN TÍCH SỰ CỐ BẢO MẬT HỆ THỐNG
## Dự án: Girlsbaito | Ngày lập báo cáo tổng hợp: 22/05/2026
**Mức độ nghiêm trọng toàn cục: 🔴 CRITICAL (Tối khẩn cấp)**  
**Tình trạng hiện tại: Đang trong quá trình xử lý & khắc phục**

---

### I. TỔNG QUAN SỰ CỐ (EXECUTIVE SUMMARY)
- Thời điểm phát hiện: 13:49 ngày 21/05/2026, qua phân tích access‑log.
- Mô tả sự cố: Rò rỉ các tệp cấu hình nhạy cảm (.env, .git) và log hệ thống (laravel.log); đồng thời phát hiện malware persistence trên server Production.
- Trạng thái hiện tại: Mã độc tạm thời không hoạt động; các chỉ số CPU, RAM, mạng bình thường. Các file nhạy cảm đã được chặn truy cập công khai từ 20/05/2026.
- Mối nguy cấp bách: Thông tin cá nhân và khóa bí mật đã bị rò rỉ, cần khắc phục nhanh để bảo vệ dữ liệu khách hàng và khôi phục niềm tin của client. 



---

### II. PHÂN TÍCH NGUYÊN NHÂN DẪN ĐẾN SỰ CỐ (ROOT CAUSE ANALYSIS)

Dựa trên điều tra chi tiết ngày 25/05/2026, nguyên nhân gây ra chuỗi sự cố được tổng hợp vào ba nhóm chính:

1. **Rò rỉ dữ liệu khi di chuyển hệ thống**
   - *Quy trình Migration không dọn dẹp*: Sao chép toàn bộ thư mục dự án, bao gồm `storage/logs/` chứa log lịch sử (từ 10/2022), sang máy chủ mới.
   - *Thiếu bước Cleanup*: Không rà soát, xóa các file log, backup, zip nhạy cảm trước khi đưa mã nguồn lên Production.

2. **Lỗ hổng kỹ thuật khi triển khai môi trường mới**
   - *Chuyển đổi Apache → Nginx chưa chuẩn*: `.htaccess` trên Apache không được chuyển sang cấu hình Nginx, dẫn tới việc bỏ qua các rule chặn file ẩn và log.
   - *Cấu trúc dự án không chuẩn*: `index.php` đặt ở thư mục gốc thay vì `/public`, khiến `.env`, `.git`, `storage/logs/` trở thành tài nguyên tĩnh có thể truy cập công khai.

3. **Thiếu sót về quy trình và năng lực con người**
   - *Không có Checklist bảo mật*: Không có tài liệu kiểm tra an toàn khi deploy Laravel trên Nginx, và không có quy trình rà soát bảo mật trước Go‑live.
   - *Kỹ năng vận hành hạn chế*: Nhân sự thiếu kinh nghiệm cấu hình Laravel/Nginx và không thực hiện kiểm thử an toàn thực tế sau khi cấu hình.

---

### III. BÁO CÁO CHI TIẾT CÁC LỖ HỔNG & SỰ CỐ

#### 1. Rò rỉ tệp cấu hình nhạy cảm `.env` và thư mục quản lý `.git`
* **Mức độ nghiêm trọng**: 🔴 **CRITICAL**
* **Môi trường xảy ra**: Web Server Nginx (Production)
* **Phạm vi ảnh hưởng**: 
  * Rò rỉ mã khóa ứng dụng Laravel (`APP_KEY`).
  * Rò rỉ thông tin xác thực cơ sở dữ liệu (`DB_USERNAME`, `DB_PASSWORD`).
  * Rò rỉ khóa kết nối Google API (`GOOGLE_CLIENT_SECRET`, Google Refresh Token).
  * Lộ toàn bộ mã nguồn (Source Code) và lịch sử phát triển thông qua thư mục quản lý phiên bản `.git`.
* **Risk tiềm ẩn (Rủi ro)**: 
  * Kẻ tấn công có thể giải mã session/cookie của người dùng để giả mạo phiên đăng nhập của bất kỳ ai.
  * Sử dụng thông tin đăng nhập database để truy cập trực tiếp vào cơ sở dữ liệu nhằm đánh cắp, sửa đổi hoặc xóa sạch dữ liệu (tấn công Ransomware tống tiền).
  * Lạm dụng API Google của dự án (sử dụng refresh token vô hạn), gây phát sinh chi phí lớn hoặc bị Google khóa tài khoản vĩnh viễn do vi phạm chính sách.
  * Lộ bí mật công nghệ, sở hữu trí tuệ của dự án và tạo điều kiện cho kẻ tấn công tìm kiếm thêm các lỗ hổng logic sâu hơn trong mã nguồn.
* **Nguyên nhân dự kiến**:
  * Cấu hình Web Server Nginx bị thiếu quy tắc chặn các yêu cầu truy cập trực tiếp vào các tệp tin ẩn (các tệp tin hoặc thư mục bắt đầu bằng dấu chấm `.`).
  * Tệp cấu hình môi trường cục bộ `.env` chưa được đưa vào tệp `.gitignore` nên đã bị đẩy lên Git repository và kéo về máy chủ Production.
* **Đề xuất hướng xử lý ngắn hạn (Cho Dev)**:
  * Tạo lại khóa mã hóa ứng dụng `APP_KEY` bằng lệnh `php artisan key:generate`.
  * Vô hiệu hóa và cấp lại Google Client Secret & Refresh Token trên Google Cloud Console.
  * Thay đổi thông tin mật khẩu database (`DB_PASSWORD`) ngay lập tức (thực hiện vào khung giờ đêm).
  * Cấu hình Nginx chặn triệt để các tệp/thư mục ẩn: `location ~ /\. { deny all; return 404; }`.
  * Đưa `.env` vào `.gitignore` và loại bỏ tệp `.env` cũ khỏi lịch sử Git bằng lệnh `git rm --cached .env`.

#### 2. Lộ lọt thông tin cá nhân khách hàng qua tệp tin `laravel.log` công khai
* **Mức độ nghiêm trọng**: 🔴 **CRITICAL**
* **Môi trường xảy ra**: Web Server Nginx (Production) - Tệp tin `/www/girls-baito-production/storage/logs/laravel.log`
* **Phạm vi ảnh hưởng**: 
  * Tệp tin log có dung lượng tích lũy lớn (7.2GB), lưu trữ dữ liệu lịch sử từ tháng 10/2022 đến tháng 06/2025 (log cũ từ máy xuất XSERVER).
  * Xác định có **474 MB dữ liệu log (~6.6% dung lượng)** đã bị tải xuống thành công bởi một IP botnet lạ (`212.86.126.157`) vào ngày 05/04/2026.
  * **34 người dùng bị ảnh hưởng trực tiếp**, trong đó bao gồm: **28 Quản trị viên cửa hàng (role=2)**, **5 Hội viên thường (role=1)**, **1 Quản trị viên vận hành (role=4)**, **1 Tài khoản thử nghiệm (không xử lý)**.
  * Thông tin bị rò rỉ: Họ tên, địa chỉ email, mật khẩu đã được băm (bcrypt), một phần số điện thoại, và trạng thái tài khoản. *Nguyên nhân lưu thông tin:* Do thiết kế của Laravel tự động lưu các giá trị truy vấn (bind values) kèm theo khi xảy ra các ngoại lệ SQL (SQL Exceptions).
* **Risk tiềm ẩn (Rủi ro)**:
  * Kẻ tấn công có thể sử dụng các máy tính hiệu năng cao hoặc các công cụ bẻ khóa mật khẩu (hashcat) để giải mã mật khẩu bcrypt đối với các tài khoản đặt mật khẩu yếu (tấn công từ điển).
  * Do phần lớn người dùng bị ảnh hưởng chưa thay đổi mật khẩu sau thời điểm rò rỉ, nguy cơ cao các mật khẩu bcrypt bị lộ trùng khớp với mật khẩu đang sử dụng hiện tại.
  * Nguy cơ cao xảy ra các cuộc tấn công lừa đảo (phishing) nhắm vào 34 người dùng bị lộ email/số điện thoại, đặc biệt là các tài khoản Quản trị viên cửa hàng có quyền hạn cao trên hệ thống.
  * Ảnh nghiêm trọng đến uy tín thương hiệu đối với Client và người dùng, đối mặt với các rủi ro pháp lý về Luật bảo vệ dữ liệu cá nhân.
* **Nguyên nhân dự kiến**:
  * Đường dẫn gốc của ứng dụng (Document Root) trong cấu hình Nginx bị thiết lập trỏ thẳng tới thư mục gốc của dự án (`project root`) thay vì trỏ tới thư mục `/public`, dẫn đến việc các thư mục con nhạy cảm như `storage/logs/` nằm trong phân vùng public và có thể truy cập được qua Internet.
  * File log cũ với kích thước lớn không được xóa bỏ hoặc lưu trữ bảo mật bên ngoài vùng Web Server khi tiến hành nâng cấp hệ thống máy chủ.
* **Đề xuất hướng xử lý ngắn hạn (Cho Dev)**:
  * Thực hiện di chuyển ngay tệp `laravel.log` ra ngoài khu vực công khai (hoặc xóa bỏ hoàn toàn sau khi sao lưu an toàn).
  * Thực hiện cấu hình bắt buộc đổi mật khẩu ngay lập tức đối với **34 tài khoản** bị ảnh hưởng khi họ đăng nhập lại vào hệ thống.
  * Soạn thảo email thông báo sự cố bảo mật một cách văn minh, minh bạch và chuyên nghiệp gửi tới 34 người dùng này để cảnh báo và hướng dẫn họ đổi mật khẩu.
  * Đưa thư mục `storage/logs/` vào `.gitignore` để tránh bị đẩy lên Git.

#### 3. Xâm nhập mã độc và thiết lập duy trì sự hiện diện (Malware Persistence)
* **Mức độ nghiêm trọng**: 🔴 **CRITICAL**
* **Môi trường xảy ra**: Hệ điều hành Linux (Production Server) - Thư mục `/var/tmp/`
* **Phạm vi ảnh hưởng**: 
  * Phát hiện các thư mục chứa tệp thực thi ELF độc hại và shell script trong phân vùng `/var/tmp/` trên server Production:
    * Thư mục `/var/tmp/5a118aba/`: Chứa file `51dc50c6` (826KB, ELF 64-bit), file `f5307ebe` (2.7MB, ELF 64-bit), file ẩn `.b4nd1d0` (170B, shell script), file ẩn `.c` (241B, shell script).
    * Thư mục `/var/tmp/.ladyg0g0/`: Chứa file ẩn `.pr1nc35` (17B).
    * Thư mục `/var/tmp/8fbb119f/`: (Đã được tạo nhưng hiện tại trống).
  * **Các tiến trình độc hại đã tự động đăng ký ngầm vào crontab của user `www`**:
    * `@daily   /var/tmp/6f2148e5/./51dc50c6 > /dev/null 2>&1 & disown`
    * `@reboot  /var/tmp/6f2148e5/./51dc50c6 > /dev/null 2>&1 & disown`
    * `* * * * * /var/tmp/6f2148e5/./51dc50c6 > /dev/null 2>&1 & disown`
    * `@monthly /var/tmp/6f2148e5/./51dc50c6 > /dev/null 2>&1 & disown`
    * `*/30 * * * * /var/tmp/6f2148e5/./.c > /dev/null 2>&1 & disown`
  * **Dòng thời gian sự kiện (Malware Timeline):**
    * *27/01/2026:* Mã độc xâm nhập lần đầu (thư mục `/var/tmp/5a118aba/` được tạo).
    * *10/03/2026:* Tạo thêm thư mục mới `/var/tmp/8fbb119f/`.
    * *12/03/2026:* Thêm mới và cập nhật các loader script.
    * *14/03/2026:* Server khởi động lại (ước tính từ uptime). Sau khi reboot, cron liên tục kích hoạt chạy mã độc mỗi phút nhưng bị thất bại do chỉ định sai đường dẫn (đường dẫn `/var/tmp/6f2148e5/` không tồn tại thực tế trên server), dẫn đến vòng lặp lỗi liên tục và mã độc hiện tại KHÔNG chạy active.
* **Tình trạng an toàn cơ sở dữ liệu hiện tại:**
  * Không phát hiện tài khoản backdoor đáng ngờ nào trong cơ sở dữ liệu (chỉ có root, gbaito và các tài khoản hệ thống chuẩn).
  * Tài khoản `root` của MySQL sử dụng xác thực `auth_socket` (không sử dụng mật khẩu truy cập ngoài), loại bỏ rủi ro bị rò rỉ mật khẩu root DB.
* **Risk tiềm ẩn (Rủi ro)**:
  * Kẻ tấn công sở hữu quyền kiểm soát sâu hệ thống ở mức hệ điều hành cao nhất dưới quyền user web `www`.
  * **Các hoạt động chưa xác định:** Trong khoảng **6 tuần hoạt động active (27/01 đến 12/03/2026)** của mã độc, chưa thể xác định hành vi của kẻ tấn công. Rủi ro cao bao gồm:
    * Có thể đã thực hiện đọc và dump toàn bộ dữ liệu database thông qua cấu hình DB kết nối của user `gbaito`.
    * Đã cài đặt thêm các file backdoor tĩnh ẩn giấu sâu ở các thư mục khác của dự án.
    * Đã thu thập thêm các thông tin xác thực nhạy cảm khác từ server.
* **Nguyên nhân dự kiến**: 
  * Kẻ tấn công có thể đã khai thác thông tin rò rỉ từ tệp cấu hình nhạy cảm `.env` (hoặc rò rỉ mã nguồn từ thư mục `.git`) để thực thi tải lên mã độc, cấu hình crontab và leo thang đặc quyền hệ thống dưới quyền `www`.
* **Đề xuất hướng xử lý ngắn hạn (Cho Dev)**:
  * Sao lưu an toàn các tệp mã độc sang một vùng lưu trữ độc lập để phục vụ công tác điều tra số (Forensics), sau đó tiến hành xóa bỏ triệt để.
  * Làm sạch toàn bộ các tác vụ crontab không rõ nguồn gốc của user `www`.
  * Thực hiện điều tra chuyên sâu nhật ký hệ thống (Forensics), rà soát toàn bộ source code xem có file backdoor nào mới được tải lên trong 6 tuần hoạt động active của hacker hay không.

---

### IV. KẾ HOẠCH KHẮC PHỤC & TRIỂN KHAI CHI TIẾT (ACTION PLAN & TIMELINE)

Dựa trên báo cáo đánh giá tính khả thi và sự cố thực tế, ban dự án thống nhất kế hoạch triển khai nâng cao bảo mật hệ thống toàn diện, chia theo các hạng mục lớn và lộ trình thời gian cụ thể như sau:

#### 1. Bảng chi tiết các Task cần triển khai

| ID | Hạng mục & Tên công việc | Phương án triển khai chi tiết (Dev) | Mục tiêu & Lợi ích mang lại | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **1.1** | **Giám sát**: Phát hiện truy cập bất thường | Cài đặt `fail2ban` quét log Nginx tự động chặn các IP dò quét khả nghi và cảnh báo qua Slack/Telegram. | Ngăn chặn bots, dò quét tự động và brute force. | Chưa thực hiện |
| **1.2** | **Giám sát**: Kiểm tra định kỳ tải server & logs | Tạo cronjob chạy script phân tích logs hàng ngày kết hợp Zabbix/Grafana theo dõi tài nguyên. | Phát hiện sớm DDoS nhỏ, botnet hoặc sự cố treo hệ thống. | Chưa thực hiện |
| **2.1** | **Máy chủ**: Quét file đáng ngờ định kỳ | Cấu hình `Maldet` + `ClamAV` quét tự động các thư mục `/var/tmp/`, `/tmp/`, `storage/` hàng đêm. | Phát hiện và cách ly sớm webshell, backdoor độc hại. | Chưa thực hiện |
| **2.2** | **Máy chủ**: Vô hiệu hóa password SSH | Cấu hình `PasswordAuthentication no` trong sshd daemon. Sử dụng SSH Key cá nhân để đăng nhập. | Chặn 100% tấn công Brute Force mật khẩu cổng 22. | 🟢 Đã thực hiện |
| **2.3** | **Máy chủ**: Tối ưu cấu hình Nginx | Cấu hình rule chặn các file nhạy cảm (`.env`, `.git`, `.log`) và cấu hình Rate Limiting. | Ngăn rò rỉ dữ liệu tĩnh và giảm thiểu spam request. | 🟢 Đã thực hiện |
| **3.1** | **Quyền hạn**: Đặc quyền tối thiểu Database | Thu hồi quyền dư thừa (SUPER, FILE) của user `gbaito`. Chỉ GRANT quyền cơ bản (SELECT, INSERT, UPDATE, DELETE, INDEX). | Giảm thiểu thiệt hại tối đa nếu lộ thông tin kết nối DB. | Chưa thực hiện |
| **3.2** | **Quyền hạn**: Chính sách xác thực SSH | Tách biệt SSH Key từng nhân sự. Tiến hành kiểm tra và dọn dẹp `authorized_keys` định kỳ hàng tháng. | Loại bỏ rủi ro kiểm soát nội bộ, đảm bảo thu hồi quyền khi off-boarding. | 🟢 Đã thực hiện |
| **4.1** | **Ứng dụng**: Chuyển Document Root sang `/public` | Di chuyển file `index.php` vào thư mục `/public` và cấu hình Nginx trỏ Document Root trực tiếp vào đó. | Cô lập hoàn toàn mã nguồn gốc Laravel khỏi Internet. | Chưa thực hiện |
| **4.2** | **Ứng dụng**: Sanitize log Exception Handler | Can thiệp Exception Handler (`Handler.php`) bổ sung logic che giấu dữ liệu nhạy cảm trước khi ghi log. | Bảo vệ thông tin khách hàng khỏi rò rỉ khi gặp SQL Exception. | Chưa thực hiện |
| **4.3** | **Ứng dụng**: Duy trì log rotation | Duy trì cấu hình `LOG_CHANNEL=daily` (giữ 14 ngày) và cấu hình `logrotate` hệ thống cho log Nginx. | Tiết kiệm dung lượng đĩa, giảm thiểu lượng log rò rỉ tối đa. | 🟢 Đã thực hiện |
| **4.4** | **Ứng dụng**: Chuẩn hóa cấu hình môi trường | Tắt chế độ `APP_DEBUG` trên Production, dọn dẹp key thừa và phân quyền an toàn `chmod 600` cho file `.env`. | Tăng tính ổn định và bảo mật tối đa cho dữ liệu môi trường. | 🟡 Đang thực hiện |

---

#### 2. Kế hoạch & Tiến độ triển khai chi tiết (Gantt Schedule)

Dưới đây là lịch trình phân bổ công việc chi tiết từ ngày 26/05 đến ngày 04/06:

| Task ID | Hạng mục công việc | 26/05 | 27/05 | 28/05 | 29/05 | 01/06 | 02/06 | 03/06 | 04/06 | Trạng thái hiện tại |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.1** | Triển khai phát hiện truy cập bất thường | **X** | **X** | | | | | | | Chưa thực hiện |
| **1.2** | Kiểm tra định kỳ tải server & log | | | **X** | **X** | | | | | Chưa thực hiện |
| **2.1** | Quét file đáng ngờ định kỳ (`Maldet`) | | | **X** | **X** | | | | | Chưa thực hiện |
| **2.2** | Vô hiệu hóa xác thực mật khẩu SSH | **-** | | | | | | | | 🟢 **Đã thực hiện** |
| **2.3** | Tối ưu hóa cấu hình máy chủ Nginx | **-** | | | | | | | | 🟢 **Đã thực hiện** |
| **3.1** | Áp dụng đặc quyền tối thiểu DB | **X** | **X** | | | | | | | Chưa thực hiện |
| **3.2** | Thiết lập chính sách xác thực SSH | **-** | | | | | | | | 🟢 **Đã thực hiện** |
| **4.1** | Chuyển Document Root sang `/public` | | | | | **X** | **X** | **X** | | Chưa thực hiện |
| **4.2** | Sanitize log Exception Handler | | | | | **X** | **X** | | | Chưa thực hiện |
| **4.3** | Duy trì log rotation | **-** | | | | | | | | 🟢 **Đã thực hiện** |
| **4.4** | Chuẩn hóa cấu hình môi trường `.env` | **X** | | | | | | | | 🟡 **Đang thực hiện** |

*Ghi chú: Ký hiệu **X** biểu thị ngày làm việc, **-** biểu thị công việc đã hoàn thành trước đó.*

---

### V. BIỆN PHÁP PHÒNG NGỪA TÁI PHÁT (PREVENTATIVE MEASURES)

Để đảm bảo các sự cố tương tự không bao giờ lặp lại, toàn bộ đội ngũ dự án cần tuân thủ nghiêm ngặt các nguyên lý an toàn thông tin sau:

1. **Nguyên lý Đặc quyền tối thiểu (Least Privilege)**:
   * **Quản trị Máy chủ:** Tuyệt đối không cho phép đăng nhập SSH trực tiếp bằng tài khoản `root`. Lập trình viên chỉ được đăng nhập qua tài khoản cá nhân được cấp quyền hạn chế và dùng lệnh `sudo` khi cần thiết. Vô hiệu hóa xác thực bằng mật khẩu SSH, bắt buộc sử dụng xác thực khóa công khai (SSH Keys).
   * **Quản trị Cơ sở dữ liệu:** Tài khoản kết nối DB của ứng dụng (`gbaito`) chỉ được cấp các quyền cần thiết trên database cụ thể, tuyệt đối không dùng tài khoản root DB hoặc cấp quyền dư thừa.
2. **Quy chuẩn Cấu hình an toàn**:
   * **Cấu trúc dự án:** Thư mục gốc chứa tệp chạy công khai (Document Root) của Web Server **bắt buộc** phải trỏ vào thư mục `/public` (Laravel) để cô lập mã nguồn gốc.
   * **Quản lý Secrets:** Các tệp tin cấu hình môi trường chứa thông tin mật (`.env`) tuyệt đối không được đưa lên Git quản lý. Thiết lập phân quyền đọc/ghi khắt khe trên server Production.
3. **Giám sát & Cảnh báo thời gian thực**:
   * Thiết lập hệ thống giám sát tài nguyên máy chủ liên tục để phát hiện kịp thời các hành vi tăng vọt CPU/RAM bất thường (dấu hiệu của mã độc).
   * Thiết lập thông báo tự động (Slack/Telegram) mỗi khi có đăng nhập SSH thành công hoặc có IP bị chặn bởi cơ chế phát hiện truy cập bất thường (`fail2ban`).

---
*Báo cáo này được tổng hợp bởi Ban Quản lý Dự án (PM) dựa trên các dữ liệu kỹ thuật đã được xác minh tính đến ngày 22/05/2026. Mọi thắc mắc và đóng góp ý kiến về phương án xử lý xin vui lòng gửi về Ban dự án.*
