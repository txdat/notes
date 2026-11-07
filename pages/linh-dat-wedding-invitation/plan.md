---
title: Khánh Linh & Xuân Đạt - Thiệp cưới online (hướng B · Thiệp giấy)
draft: true
---

Kế hoạch thiết kế cho thiệp mời online một trang, 6 màn, theo hướng **B · Thiệp giấy (stationery)**. Tài liệu này mô tả *thiệp trông và hoạt động thế nào*, chưa phải kế hoạch code. Prompt tạo ảnh AI nằm ở [[gemini-prompts]].

## 1. Ý tưởng

**"Bộ thiệp đặt trên bàn."** Khách mở một phong bì thật, rồi lần lượt thấy từng món của một bộ thiệp cưới in trên giấy cotton, đặt trên nền vải lanh:

| Món trong bộ thiệp | Trang |
|---|---|
| Phong bì gắn con dấu sáp | 1 |
| Thiệp chính: ảnh in và tấm giấy can ghi tên | 2 |
| Thiệp mời in nổi (letterpress) | 3 |
| Thiệp thông tin: giờ, ngày, nơi | 4 |
| Xấp ảnh in | 5 |
| Thiệp hồi âm (RSVP) | 6 |

Mỗi trang là một món, nên khách hiểu ngay đang xem gì mà không cần nhiều chữ. Ảnh cưới xuất hiện như **ảnh in thật** có viền giấy, không phải ảnh web.

**Nguyên tắc:**
- Ít chữ. Mỗi trang chỉ có một ý chính.
- **Không thêm thông tin nào mà thiệp cũ không có.** Câu chữ lấy từ thiệp cũ (`pages/linh-dat-wedding`), xưng "chúng mình" vì thiệp do cô dâu và chú rể gửi.
- Chất liệu thật: vải, giấy cotton, sáp, giấy can, ruy băng. Không vẽ phẳng.
- Toàn bộ chữ là chữ HTML, **không có chữ nào nằm trong ảnh AI**.
- Một hướng sáng duy nhất: ánh sáng ban ngày mềm từ **góc trên bên trái**. Bóng đổ do CSS tạo, nên mọi món đổ bóng giống nhau.

## 2. Hệ thống thiết kế

### Màu

| Vai trò | Màu | Ghi chú |
|---|---|---|
| Nền vải lanh | `#D8CCB8` | Màu be xám ấm, lấy từ ảnh vải AI |
| Giấy thiệp | `#FBF8F1` | Ngà, giấy cotton |
| Phong bì | `#EDE3D1` | Kem đậm hơn giấy thiệp một chút |
| Chữ chính | `#2F241C` | Nâu espresso, không dùng đen |
| Chữ phụ | `#6E5A4A` | |
| **Màu nhấn: đỏ rượu vang** | `#6E1A26` | Monogram DL, con dấu sáp, lót phong bì |
| Nhũ vàng | `#A8844F` | Chỉ điểm xuyết: viền mảnh, nhãn nhỏ |
| Ruy băng | `#E8DCC6` | Champagne |

### Chữ

- **Cormorant Garamond** (serif, có tiếng Việt) cho tên, lời mời, ngày giờ. Chữ có hiệu ứng **in nổi**: mực hơi lún vào giấy, nhờ bóng sáng một pixel phía dưới.
- **Be Vietnam Pro** cho nhãn nhỏ (NHÀ TRAI, LỄ THÀNH HÔN…), viết hoa giãn rộng.
- **Không dùng font viết tay** cho tiếng Việt. Nét mềm duy nhất trên thiệp là monogram DL.

### Monogram

- Dùng file **DL** (`assets/monogram.webp`, nền trong suốt, đổi màu bằng CSS).
- Trên con dấu sáp: chữ nhũ vàng nổi trên sáp đỏ.
- Trên thiệp: màu đỏ rượu vang, in nổi.
- Làm favicon và ảnh xem trước khi chia sẻ link.

### Chất liệu

| Chất liệu | Nguồn |
|---|---|
| Vải lanh nền | AI (prompt 01) |
| Vân giấy cotton | AI (prompt 02) |
| Mép giấy xé (deckle) | AI (prompt 06), dùng làm khuôn cho thiệp và ảnh in |
| Phong bì đóng và mở | AI (prompt 03, 04) |
| Con dấu sáp trơn | AI (prompt 05), monogram đặt lên bằng CSS |
| Ruy băng lụa | AI (prompt 07) |
| Cành hoa khô | AI (prompt 08) |
| Giấy can mờ | CSS (lớp trắng trong mờ, làm nhòe nhẹ phía sau) |
| Bóng đổ | CSS, chung một hướng sáng |

### Ảnh cưới thành ảnh in

- Viền trắng ngà 10–14px. Phía dưới chừa rộng hơn một chút như ảnh in thật.
- Hạ nhẹ độ tương phản và nâng màu đen lên cho giống giấy ảnh mờ, thêm hạt nhiễu nhẹ. Áp dụng cùng một kiểu cho mọi ảnh để đồng bộ.
- Đặt nghiêng ngẫu nhiên −4° đến +6°. Không nghiêng quá, vì quá thì thành kiểu "vui nhộn".

### Chuyển động

- **Đặt xuống:** khi một trang hiện ra, từng món như được đặt lên bàn. Hơi to hơn và bóng xa ở đầu, rồi về đúng vị trí với bóng sát. Các món lệch nhau khoảng 120ms. Không nảy.
- **Mở phong bì:** chỉ có ở trang 1, giải thích ở dưới.
- Tắt toàn bộ chuyển động nếu máy bật giảm chuyển động.
- Không có nhạc, không có hoa rơi, không có đếm ngược.

### Bố cục và cuộn

- 6 màn, mỗi màn cao bằng màn hình điện thoại. Vuốt thì dừng đúng từng màn (scroll snap mềm).
- 6 chấm nhỏ ở cạnh phải cho biết đang ở màn nào.
- Thiết kế cho khung 390×844. Máy thấp (iPhone SE, 667px) thì thu nhỏ cả bố cục chứ không cắt.
- Trên máy tính: bộ thiệp nằm giữa màn hình, hai bên là nền vải lanh.

## 3. Chi tiết 6 trang

### Trang 1 · Phong bì

- **Bố cục:** nền vải lanh. Phong bì đóng nằm giữa, hơi nghiêng −2°. Con dấu sáp DL ở mũi nắp.
- **Chữ trên phong bì:** "Thiệp mời", chữ serif in lên giấy, nằm ở nửa dưới. Nếu link có tên thì thêm dòng nghiêng "Gửi **{tên}**". Không có tên thì chỉ ghi "Thiệp mời".
- **Dưới phong bì:** "Chạm để mở", chữ nhỏ, nhấp nháy rất chậm.
- **Khi chạm:**
  1. Con dấu nứt và mờ đi (0,3s).
  2. Nắp lật lên, lộ lớp lót đỏ rượu vang. Ảnh phong bì đóng chuyển sang ảnh phong bì mở.
  3. Một tấm thiệp nhỏ trượt lên từ trong phong bì.
  4. Trang tự cuộn xuống trang 2.
- **Ảnh AI:** 01, 03, 04, 05.

### Trang 2 · Lễ thành hôn

- **Bố cục:** ảnh in `9302` lớn (khoảng 70% chiều rộng), nghiêng −3°. Phía sau lấp ló một tấm thiệp trơn nghiêng +4°. Tấm giấy can phủ lên mép dưới ảnh, có ruy băng lụa vắt dọc qua.
- **Chữ trên giấy can:**
  - LỄ THÀNH HÔN
  - **Khánh Linh & Xuân Đạt**
  - THỨ BA · 24.11.2026 · 11:00
- **Chạm vào giấy can:** tấm giấy hơi nhấc lên để thấy rõ ảnh phía dưới. Chi tiết nhỏ, không bắt buộc.
- **Ảnh AI:** 01, 06 (tấm thiệp lót), 07.

### Trang 3 · Trân trọng kính mời

- **Bố cục:** một thiệp mời mép xé đứng giữa, chiếm khoảng 85% chiều rộng, thẳng. Ảnh in nhỏ `9566` (sân thượng mái vòm) cài ở góc dưới phải, nghiêng +6°. Một cành hoa khô đặt ở góc trên trái.
- **Chữ trên thiệp** (in nổi, lấy từ thiệp cũ), từ trên xuống:
  - Monogram DL màu đỏ rượu vang
  - *Trân trọng kính mời*
  - **{tên khách}** *đến chung vui trong ngày thành hôn của chúng mình*. Không có tên thì ghi "**bạn và gia đình** đến chung vui…", giống thiệp cũ.
  - NHÀ GÁI: Ông Nguyễn Minh Tuân, Bà Hồ Thị Thu Huyền
  - NHÀ TRAI: Ông Trần Xuân Kế, Bà Nguyễn Thị Thanh Xuân
  - CÔ DÂU **Nguyễn Khánh Linh** · CHÚ RỂ **Trần Xuân Đạt**
- Thứ tự nhà gái trước, cô dâu trước theo thiệp cũ, thống nhất với "Khánh Linh & Xuân Đạt".
- **Ảnh AI:** 01, 02, 06, 08.

### Trang 4 · Thời gian & địa điểm

- **Bố cục:** thiệp thông tin mép xé, nhỏ hơn thiệp mời, nằm lệch xuống dưới. Ảnh in `9170` (đèn chùm) nằm phía trên, nghiêng −4°, đè một góc lên thiệp.
- **Chữ trên thiệp:**
  - THỨ BA
  - **11:00** (chữ to nhất trang)
  - 24 · 11 · 2026
  - *Ngày 16 tháng 10 năm Bính Ngọ*
  - Một dòng nhỏ: 10:30 Đón khách · 11:00 Lễ thành hôn · 11:30 Khai tiệc
  - Đường kẻ mảnh
  - **Trung tâm tổ chức sự kiện Âu Cơ**
  - 1A Nguyễn Hữu Cầu, P. Hải Dương, TP. Hải Phòng
- **Một nút** làm như nhãn giấy nhỏ in chữ: **Mở Google Maps**.
- Không có lịch tháng hay đếm ngược như thiệp cũ, vì hướng này ít chữ. Thông tin vẫn giữ đủ.
- **Ảnh AI:** 01, 02, 06.

### Trang 5 · Ảnh cưới

- **Bố cục:** 5 ảnh in xếp chồng tự nhiên trên nền vải, mỗi tấm một góc nghiêng, không theo lưới. Không có chữ.
- **Ảnh:** `9333` (nến và cửa cổ điển), `9620` (rèm), `9513` (cô dâu), `9364` (chú rể), `9049` (tay nắm tay, ảnh ngang).
- **Chạm một ảnh:** ảnh nhấc lên và phóng to giữa màn hình trên nền tối mờ. Vuốt ngang để xem ảnh khác, chạm ra ngoài để đặt ảnh về chỗ cũ.
- **Ảnh AI:** 01.

### Trang 6 · Hồi âm

- **Bố cục:** thiệp hồi âm nằm ngang, là ảnh prompt 06 xoay 90°. Ảnh in `9746` (hoàng hôn) đặt chéo phía trên. Cuối trang có monogram DL nhỏ.
- **Chữ và form trên thiệp:**
  - XÁC NHẬN THAM DỰ
  - Tên: một dòng kẻ như để điền tay, tự điền sẵn từ link
  - Hai ô chọn kiểu đánh dấu bằng mực, giữ đúng đáp án thiệp cũ: ◻ Tất nhiên rồi / ◻ Mình bận mất rồi
  - Đi mấy người (tính cả bạn): 1 · 2 · 3+
  - Lời chúc gửi chúng mình (không bắt buộc), một dòng
  - Nút **Gửi**
- **Sau khi gửi:** một con dấu sáp nhỏ "đóng" xuống góc thiệp. Chữ lấy từ thiệp cũ:
  - Tham dự: "Cảm ơn {tên}. Ngày vui của chúng mình sẽ trọn vẹn hơn khi có {tên}."
  - Không đi: "Tiếc là lần này chưa gặp được {tên}, hẹn {tên} dịp khác nhé."
  - Mở lại link thì vẫn nhớ trạng thái đã gửi, giống thiệp cũ.
- Ký tên **Linh & Đạt** dưới thiệp.
- **Ảnh AI:** 01, 02, 05, 06.

## 4. Danh sách tài sản

| File | Nguồn | Kích thước xuất | Dùng ở |
|---|---|---|---|
| `linen.webp` | AI 01 | Ô lặp 1024px | Nền mọi trang |
| `paper.webp` | AI 02 | Ô lặp 512px | Mặt thiệp |
| `envelope-closed.webp` | AI 03, tách nền | Rộng 900px | Trang 1 |
| `envelope-open.webp` + `envelope-pocket.webp` | AI 04, tách nền và cắt phần túi trước | Rộng 900px | Trang 1 (tấm thiệp trượt giữa hai lớp) |
| `seal.webp` | AI 05, tách nền | 300px | Trang 1, 6 |
| `card-deckle.webp` | AI 06, tách nền, làm khuôn | 1000px | Trang 2, 3, 4, 6 |
| `ribbon.webp` | AI 07, tách nền | Rộng 1200px | Trang 2 |
| `sprig.webp` | AI 08, tách nền | 500px | Trang 3 |
| `monogram.webp` | Có sẵn (DL.jpg) | 600px | Con dấu, trang 3, favicon |
| `photo-*.webp` | Ảnh cưới | Cạnh dài 1200px (ảnh lớn), 800px (ảnh nhỏ) | Trang 2–6 |
| `og.jpg` | Ghép từ các tài sản trên | 1200×630 | Ảnh xem trước khi gửi link |

**Mục tiêu dung lượng:** tổng dưới 2,5MB. Trang 1 tải xong dưới 400KB, để phong bì hiện ngay cả khi mạng 4G yếu.

## 5. Quy trình tạo ảnh AI

1. **Bạn tạo ảnh** theo [[gemini-prompts]], lưu ảnh gốc vào `drafts/ai/` (thư mục này không được deploy).
2. **Bạn chọn bản ưng nhất** theo bảng kiểm bên dưới.
3. **Claude hậu kỳ:**
   - Tách nền (nền phẳng một màu nên tách bằng ImageMagick được).
   - Xóa logo ✦ của Gemini.
   - Chỉnh màu về đúng bảng màu.
   - Làm ô lặp liền mạch cho vải và giấy.
   - Cắt túi phong bì.
   - Nén WebP.

**Bảng kiểm khi chọn ảnh AI:**
- [ ] Không có chữ, ký tự hay hoa văn giống chữ nào.
- [ ] Ánh sáng từ góc trên trái, mềm, không bóng gắt.
- [ ] Màu gần đúng mã trong prompt, không bóng loáng kiểu "ảnh AI".
- [ ] Vật thể thẳng với máy ảnh (nhìn từ trên xuống), không bị phối cảnh xiên.
- [ ] Nền phẳng một màu, có khoảng trống quanh vật thể, mép vật thể rõ ràng.
- [ ] Phóng to 200% không thấy chi tiết lỗi như mép giấy chảy hay sợi vải méo.
- [ ] Phong bì đóng (03) và mở (04) giống nhau về giấy, màu và kích thước.

## 6. Chức năng

- **Tên khách:** giống hệt thiệp cũ. Đọc `?to=` (cũng nhận `?name=`, `?guest=`). Có tên thì thay cả cụm "bạn và gia đình", ví dụ `?to=Gia đình chị Hoa`. Hiện ở trang 1, 3, 6 và điền sẵn vào form.
- **Hồi âm:** dùng nguyên Google Form của thiệp cũ, **không cần sửa form**. Các trường: `entry.708023101` tên, `entry.696420221` tham dự, `entry.532501918` số người, `entry.2011435420` lời chúc.
- **Ảnh xem trước khi gửi link** (Zalo, Messenger): một bức ảnh bộ thiệp đặt trên vải lanh, gồm phong bì, con dấu và ảnh in. Tiêu đề và mô tả giữ như thiệp cũ: "Khánh Linh & Xuân Đạt - Thiệp cưới", "Trân trọng kính mời bạn đến dự lễ thành hôn của Khánh Linh và Xuân Đạt, 11:00 Thứ Ba, 24.11.2026."
- **Không có:** mừng cưới hay QR, nút lưu vào lịch, nhạc.
- **Đường dẫn:** `txdat.github.io/notes/linh-dat-wedding-invitation/`. Thêm thư mục vào `rawPageDirs` khi deploy.
- **Trang cũ:** giữ nguyên, không chuyển hướng.

## 7. Tiến độ (cưới 24.11, hôm nay 07.11)

| Ngày | Việc | Ai |
|---|---|---|
| 07–09.11 | Tạo ảnh AI 01–08, chọn bản tốt | Bạn |
| 09–10.11 | Hậu kỳ tài sản, dựng trang 1–3 để xem trên điện thoại | Claude |
| 10–11.11 | Dựng trang 4–6, form, lịch, ảnh xem trước | Claude |
| 11–12.11 | Thử trên iPhone, Android, Zalo, Messenger; sửa | Cả hai |
| **13.11** | **Gửi thiệp** (trước cưới 11 ngày) | Bạn |

## 8. Đã chốt

1. Tên luôn là **Khánh Linh & Xuân Đạt**: cô dâu trước, nhà gái trước.
2. Thiệp do cô dâu và chú rể gửi, xưng **"chúng mình"**, câu chữ theo thiệp cũ.
3. **Có** cành hoa khô (prompt 08).
4. **Bỏ** mừng cưới.
5. **Bỏ** giờ kết thúc và nút lưu vào lịch.
6. Không thêm thông tin nào mà thiệp cũ không có.
