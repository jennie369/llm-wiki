# LLM Wiki — Project Context

## Overview
Knowledge base wiki về Chân Phật Tông / tâm linh phong thủy. LLM ingest từ raw sources → wiki pages.

<!-- handoff:start -->
## SESSION HANDOFF — 2026-04-14

### Công việc đang dang dở
**Nhiệm vụ chính:** Ingest toàn bộ `raw/OBSIDIAN/Clippings/Tinh Tuyển/TS Liên Anh*.md` → `wiki/sources/tt-ts-lien-anh-*.md`

**Đã xử lý (12/35 files):**
- tt-ts-lien-anh-bao-on-chung-sinh.md ✓
- tt-ts-lien-anh-chia-se-tai-phap-hoa-duong-28112024.md ✓
- tt-ts-lien-anh-giang-cao-vuong-kinh.md ✓
- tt-ts-lien-anh-khai-thi-hoi-cung-dai-luc-kim-cang-112024.md ✓
- tt-ts-lien-anh-khai-thi-sau-ho-ma-bat-dong-minh-vuong.md ✓
- tt-ts-lien-anh-khai-thi-sau-ho-ma-lien-hoa-dong-tu.md ✓
- tt-ts-lien-anh-khai-thi-tai-chan-do-loi-tang-tu.md ✓
- tt-ts-lien-anh-long-chung-thuong-ton-vuong-phat.md ✓
- tt-ts-lien-anh-phap-long-vuong-bao-binh.md ✓
- tt-ts-lien-anh-ve-hoi-huong-va-bao-on.md ✓
- tt-ts-lien-anh-ve-phap-kim-cang-tat-doa.md ✓
- tt-ts-lien-anh-ve-thinh-phu.md ✓
- tt-ts-lien-anh-y-nghia-thinh-phat-tru-the.md ✓

**Còn lại (23 files — theo thứ tự raw/):**
1. TS Liên Anh Bái thổ địa công các hướng nghĩa là thế nào.md
2. TS Liên Anh Báo danh siêu độ nên phát tâm thế nào mới đúng.md
3. TS Liên Anh Bất Động Minh Vương.md
4. TS Liên Anh Chân Phật Bảo Sám.md
5. TS Liên Anh Cần có nhận thức đúng khi thỉnh Phật hỏi việc.md
6. TS Liên Anh Cần phân biệt thế gian và xuất thế gian.md
7. TS Liên Anh Hãy biết trân quý quán đảnh pháp.md
8. TS Liên Anh Học Phật cần có quan niệm và tri kiến đúng đắn.md
9. TS Liên Anh Khai thị Pháp hội Hội Cúng Diêu Trì Kim Mẫu ngày 01.01.2025.md
10. TS Liên Anh Khai thị tinh yếu về Bất Động Minh Vương.md
11. TS Liên Anh Khai thị về tu Hộ pháp.md
12. TS Liên Anh Khẩu quyết tu Cửu tiết Phật phong.md
13. TS Liên Anh Nói về Thất Phúc Thần.md
14. TS Liên Anh Quét dọn Phật đường, lau tượng Phật cũng có thể tiêu tai, tăng phúc.md
15. TS Liên Anh Tháng 7 âm lịch niệm chú báo ơn cha mẹ.md
16. TS Liên Anh Thường nghĩ về cái chết.md
17. TS Liên Anh Thủ ấn Phật kham.md
18. TS Liên Anh Truyền thuyết về Diêu Trì Kim Mẫu.md
19. TS Liên Anh Tâm đắc đọc văn tập "Nghìn chiếc thuyền pháp".md
20. TS Liên Anh Vì sao phải siêu độ.md
21. TS Liên Anh Ứng dụng của pháp hơ lửa.md
22. TS Liên Anh khai thị về Kính sư, Trọng pháp, Thực tu.md
23. TS Liên Anh Tu pháp Diêu Trì Kim Mẫu lập tức có tiền.md (nếu có trong raw/)

**Sau khi xong TS Liên Anh → cần xử lý:**
- Các file Tinh Tuyển khác (không phải TS Liên Anh)
- Cập nhật wiki/INDEX.md và wiki/LOG.md sau khi hoàn tất

### Kỹ thuật quan trọng
- Files > 10000 tokens (size > ~12KB): dùng Bash Python để đọc: `python -c "with open(r'path', encoding='utf-8') as f: print(f.read()[:8000])"`
- Xử lý song song 4 files: read 4 → write 4 đồng thời
- File naming: `tt-{kebab-slug}.md` trong `wiki/sources/`

### Tổng tiến độ wiki
- wiki/sources/: 60 tt-* files (bao gồm 13 TS Liên Anh)
- Tổng wiki pages: khoảng 200+ pages
<!-- handoff:end -->
