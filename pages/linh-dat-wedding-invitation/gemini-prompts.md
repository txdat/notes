---
title: Khánh Linh & Xuân Đạt - Gemini prompts (thiệp giấy)
draft: true
---

Chất liệu cho thiệp hướng B · Thiệp giấy, xem [[plan]]. Mỗi file trong `prompts/` là **một prompt hoàn chỉnh**: mở file, chọn hết, sao chép, rồi dán vào Gemini (gemini.google.com).

## Quy tắc chung

- **Chỉ tạo chất liệu trơn.** Không có chữ, không có monogram. Chữ và monogram DL sẽ được đặt lên bằng code.
- Chọn model **Pro** (Nano Banana Pro) nếu có.
- **Mỗi prompt dùng một chat mới.** Muốn sửa nhỏ thì nhắn tiếp trong chat đó.
- Tạo 2–3 lần cho mỗi prompt và chọn bản tốt nhất theo bảng kiểm trong [[plan#5. Quy trình tạo ảnh AI]].
- **Không cần tự xóa nền.** Ảnh có nền phẳng một màu để Claude tách.
- Lưu ảnh gốc, chưa chỉnh sửa, vào `drafts/ai/` với đúng tên trong bảng dưới.

## Thứ tự làm

Ảnh **03 (phong bì đóng)** là ảnh gốc về phong cách. Các ảnh vật thể khác đính kèm ảnh này để cùng ánh sáng và cùng chất ảnh, trông như chụp chung một buổi.

1. **03** (phong bì đóng): chat mới, không đính kèm. Chọn kỹ, vì 04–08 đều dựa vào ảnh này.
2. **04** (phong bì mở): chat mới, **đính kèm ảnh 03**. Phải giống hệt phong bì.
3. **05–08** (con dấu, thiệp, ruy băng, hoa khô): mỗi prompt một chat mới, **đính kèm ảnh 03**. Riêng **05b** đính kèm hai ảnh theo đúng thứ tự: ảnh 03 trước, `DL.jpg` sau. Ảnh 03 chỉ dùng làm tham chiếu phong cách, prompt đã dặn Gemini không chép lại phong bì.
4. **01, 02** (vải, giấy): chat mới, không đính kèm. Đây chỉ là vân chất liệu, màu sẽ chỉnh khi hậu kỳ.

Không đính kèm ảnh cưới làm tham chiếu, vì Gemini dễ chép luôn người hoặc đồ vật vào ảnh.

| Prompt | Lưu thành | Dùng ở |
|---|---|---|
| [[prompts/01-linen]] | `drafts/ai/linen.png` | Nền vải lanh mọi trang · không đính kèm |
| [[prompts/02-paper]] | `drafts/ai/paper.png` | Vân giấy mặt thiệp · không đính kèm |
| [[prompts/03-envelope-closed]] | `drafts/ai/envelope-closed.png` | Trang 1 · **ảnh gốc**, không đính kèm |
| [[prompts/04-envelope-open]] | `drafts/ai/envelope-open.png` | Trang 1 · đính kèm 03 |
| [[prompts/05-wax-seal]] | `drafts/ai/seal.png` | Trang 1, 6 · đính kèm 03 · dấu trơn, DL đặt bằng code (phương án an toàn) |
| [[prompts/05b-wax-seal-monogram]] | `drafts/ai/seal-dl.png` | Thử: đính kèm 03 **và** `DL.jpg`, Gemini in DL vào sáp. Chỉ dùng nếu nét chữ giống hệt bản gốc. |
| [[prompts/06-card-deckle]] | `drafts/ai/card.png` | Thiệp trang 2, 3, 4, 6 · đính kèm 03 |
| [[prompts/07-ribbon]] | `drafts/ai/ribbon.png` | Trang 2 · đính kèm 03 |
| [[prompts/08-dried-sprig]] | `drafts/ai/sprig.png` | Trang 3 · đính kèm 03 |

## Sửa nhanh khi ảnh chưa đạt

Nhắn tiếp trong cùng chat:

- Có chữ hoặc hoa văn lạ: "Remove all text, letters and markings. Keep everything else identical."
- Màu quá rực hoặc quá bóng: "Make it more matte and muted, less saturated, like film photography. Keep everything else identical."
- Bị nhìn xiên: "Make it perfectly top-down and square to the camera, no perspective."
- Có bóng đổ lên nền: "Remove the cast shadow on the background; keep the plain flat background."
- Phong bì mở khác phong bì đóng: "Match the attached envelope exactly: same paper colour, texture, size and flap shape."
- Gemini chép lại phong bì vào ảnh 05–08: "Do not include the envelope. Show only the [seal / card / ribbon / sprig] on the plain background."
- Ánh sáng khác ảnh 03: "Match the lighting of the attached image: soft daylight from the upper left, same softness and colour grading."
