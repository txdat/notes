---
title: Khánh Linh & Xuân Đạt wedding - Gemini mascot prompts
draft: true
---

Mascot: vịt vàng (cô dâu Khánh Linh) + khủng long xanh (chú rể Xuân Đạt). Phong cách storybook, đỏ champagne + beige.

Mỗi file trong `prompts/` là **một prompt hoàn chỉnh**: mở file → Ctrl+A → Ctrl+C → dán vào Gemini chat (gemini.google.com).

## Chuẩn bị

- Đăng nhập tài khoản có gói Google AI, chọn model **Pro** (Nano Banana Pro) nếu có lựa chọn.
- Mỗi prompt dùng **một chat mới**. Sửa nhỏ thì nhắn tiếp trong chat đó, đừng mở chat mới.

## Thứ tự làm

Làm theo số thứ tự prompt:

1. **Reference.** [[prompts/01-reference]], chat mới, không đính kèm gì. Tạo vài lần, chọn bản ưng nhất, lưu `assets/reference.png`. Mọi ảnh sau đều dựa vào ảnh này nên chọn kỹ.
2. **Các prompt còn lại** (02 → 10). Mỗi prompt một chat mới, **đính kèm `reference.png`** rồi dán prompt.
   - Cảnh truyện (03 → 06): so với [[drafts/storyboard]], chưa đúng ý thì nhắn sửa.
   - Ảnh mở màn (09, 10): **xoá nền** (remove.bg, Canva…), lưu PNG trong suốt.
3. Gửi lại cho Claude: ghép vào trang, cắt logo ✦ nếu có, nén ảnh.

| Prompt | Lưu ảnh thành | Dùng ở |
|---|---|---|
| [[prompts/01-reference]] | `reference.png` | gốc cho mọi ảnh |
| [[prompts/02-hero]] | `hero.png` | ảnh bìa |
| [[prompts/03-story-ramen]] | `story-ramen.png` | truyện 1: lần đầu gặp |
| [[prompts/04-story-hotay]] | `story-hotay.png` | truyện 2: tỏ tình |
| [[prompts/05-story-birthday]] | `story-birthday.png` | truyện 3: cầu hôn |
| [[prompts/06-story-home]] | `story-home.png` | truyện 4: về chung nhà |
| [[prompts/07-map]] | `map.png` | địa điểm |
| [[prompts/08-thanks]] | `thanks.png` | cuối trang |
| [[prompts/09-duck-walk]] | `duck-walk.png` | mở màn: vịt đi vào |
| [[prompts/10-dino-walk]] | `dino-walk.png` | mở màn: khủng long đi vào |

## Sửa lỗi thường gặp

Gửi thêm trong cùng chat nếu cần:

- Nhân vật bị lệch so với reference: `Keep the veil, bow tie, colors and proportions identical to the reference image.`
- Ra quá chi tiết / giống 3D: `Simple, flat, sticker-like, minimal details, no 3D rendering.`
- Có chữ trong ảnh: `Absolutely no text, letters or numbers anywhere.`
- Không vuông: `Square 1:1 image.`
- Chân vịt thành que nâu: `Change only the duck's legs to short orange webbed duck feet, the same orange as her beak. Change nothing else.`
- Cảnh truyện khó hiểu: nói rõ chi tiết cần thấy, ví dụ `Make the duck look much more bored, chin resting on her wing.`

## Ảnh mở màn (`duck-walk.png`, `dino-walk.png`)

- Cả hai đều phải **nhìn sang phải**; trang tự lật khủng long lại.
- **Bắt buộc xoá nền** (PNG trong suốt).
- Cắt sát nhân vật, chân chạm mép dưới ảnh.
