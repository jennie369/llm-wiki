# Knowledge Index -- Phong Thủy Đế Vương

## Cách Sử Dụng
Agent PHẢI đọc files theo thứ tự Tier. Khi trả lời câu hỏi:
1. Xác định câu hỏi thuộc domain nào
2. Đọc file(s) tương ứng theo bảng domain mapping
3. Cross-reference với Tier 1 (luôn luôn)
4. Trả lời kèm trích dẫn nguồn

## Domain Mapping

| Domain | Files cần đọc | Tier |
|--------|--------------|------|
| Lá số / Cung / Sao / Tứ Hóa | `TỬ VI NTP\docs-tam-linh\Lá số tham lang.txt` + `TỬ VI NTP\docs-tam-linh\Luận giải lá số #1.md` + `raw\Tu-vi-dictionary\` | 1 |
| Nguyệt vận / Dự báo tháng | **`tools/FRAMEWORK_NGUYET_VAN_SSOT.md`** (CÔNG THỨC — SSOT, symlink → phap-su/tools) + `framework-nguyet-van-v6-complete THAM LANG.md` (diễn giải/ví dụ) + `raw\Kinh-Dich\` | 2 |
| Cơ Sở Dữ Liệu / Framework / Nền Tảng | **BẮT BUỘC ĐỌC TẤT CẢ TỪ:** `raw\tam-linh-phong-thuy\`, `raw\gem-agent-memory\`, và `TỬ VI NTP\docs-tam-linh\` | MỞ RỘNG |
| Binh pháp / Kẻ thù / Chiến thuật | `BINH PHÁP THỰC CHIẾN.md` + `TỬ VI NTP\docs-tam-linh\Luận giải lá số #1.md` + `raw\tinh-tuyen\` | 2+1 |
| Thiền phái Trúc Lâm Yên tử | Cư trần lạc đạo, tư tưởng, triết lý, ứng dụng (từ `raw\research-tran-nhan-tong\`, `raw\tam-linh-phong-thuy\` và `raw\sach-tam-linh\`) | MỞ RỘNG |
| Nghi lễ / Pháp thuật / Cúng bái | **BẮT BUỘC ĐỌC:** `Hoả Cúng`, `Giải Kết`, `Sám Hối`, `Giải Phóng` + `raw\nghi-quy-tu-tap\` + `raw\phuc-khi\` + `TỬ VI NTP\docs-tam-linh\` | 3 + MR |
| Thần Phật / Hộ Pháp / Chư Phật | **ĐẶC BIỆT CHÚ Ý BẮT BUỘC ĐỌC:** `raw\nhan-vat\` + `raw\luc-luong-tam-linh-coi-gioi\` + `raw\sach-tam-linh\` | 4 + MR |
| Kinh điển / Chân ngôn / Pháp tu | `raw\kinh-luat-luan\` + `raw\chan-ngon-than-chu\` + `raw\nghi-quy-tu-tap\` | MR |
| Long mạch / Mộ kết / Yên Tử | `PHÁP DUY TRÌ LONG MẠCH.md` + `raw\tam-linh-phong-thuy\` | 4 |
| Phong thủy dương trạch / Vật phẩm | `raw\tam-linh-phong-thuy\` + `raw\sach-tam-linh\` + `raw\phuc-khi\` + `TỬ VI NTP\docs-tam-linh\Luận giải lá số #1.md` | MR |

**⚠️ LƯU Ý GỐC:** Khi nghiên cứu về Cơ Sở Dữ Liệu, Nghi Lễ Pháp Thuật, Framework, Nền Tảng và Thần Phật BẠN KHÔNG ĐƯỢC chỉ gói gọn trong các file tử vi tài liệu đơn giản. Mọi thứ phải lấy từ hệ thống thư mục đầy đủ trong `raw\` (như `nhan-vat`, `luc-luong-tam-linh-coi-gioi`, `kinh-luat-luan`, `nghi-quy-tu-tap`...) và `docs-tam-linh`.

## Knowledge File Inventory

### Tier 1 -- NỀN TẢNG
```
../../../README.md                                      (7.9 KB)  Bản đồ hệ thống
../../../TỬ VI NTP/docs-tam-linh/Lá số tham lang.txt                            (14.7 KB) Dữ liệu lá số gốc
../../../TỬ VI NTP/docs-tam-linh/Luận giải lá số #1.md                          (739 KB)  Phân tích chiến lược toàn diện
../../../TỬ VI NTP/docs-tam-linh/                       (Mở rộng) Toàn bộ tài liệu tử vi, cung, sao
../../../raw/Tu-vi-dictionary/                          (Mở rộng) Từ điển bách khoa Tử Vi
```

### Tier 2 -- ENGINES & TRIẾT LÝ
```
../tools/FRAMEWORK_NGUYET_VAN_SSOT.md                   (SSOT)  Công thức Nguyệt Vận — CANONICAL (symlink → phap-su/tools, đọc TRƯỚC)
../../../framework-nguyet-van-v6-complete THAM LANG.md  (80 KB) Nguyệt Vận V6.0 — diễn giải/ví dụ (công thức lấy theo SSOT)
../../../BINH PHÁP THỰC CHIẾN.md                        (28 KB) Binh pháp huyền học
../../../raw/research-tran-nhan-tong/                   (Mở rộng) Báo cáo Trúc Lâm Yên Tử & Trần Nhân Tông
../../../raw/tam-linh-phong-thuy/                       (Mở rộng) Thiền phái Trúc Lâm Yên Tử, tư tưởng
../../../raw/tinh-tuyen/                                (Mở rộng) Kiến thức tinh tuyển
../../../raw/kinh-luat-luan/                            (Mở rộng) Kinh điển luận giải
../../../raw/Kinh-Dich/                                 (Mở rộng) Lý số Kinh Dịch
../../../raw/sach-tam-ly-hoc/                           (Mở rộng) Sách tâm lý học bổ trợ
```

### Tier 3 -- NGHI LỄ
```
../../../TRẦN TRIỀU GIẢI KẾT ĐẠI ĐÀN.md                 (20 KB) Đại đàn giải kết
../../../Hoả Cúng Homa.md                               (14 KB) Hỏa cúng
../../../Lễ Giải Phóng Trấn Nhân.md                     (18 KB) Giải trấn yểm
../../../Lễ Sám Hối Và Tạ Ơn Tổ Tiên 2025.md            (3 KB)  Sám hối tổ tiên
../../../raw/nghi-quy-tu-tap/                           (Mở rộng) Nghi quỹ pháp thuật
../../../raw/chan-ngon-than-chu/                        (Mở rộng) Chân ngôn thực hành
../../../raw/phuc-khi/                                  (Mở rộng) Khí cụ, pháp khí nghi lễ
```

### Tier 4 -- CƠ SỞ DỮ LIỆU THẦN THÁNH
```
../../../PHÁP DUY TRÌ LONG MẠCH TÂM LINH.md             (131 KB) Long mạch Yên Tử
../../../raw/luc-luong-tam-linh-coi-gioi/               (Cốt lõi) Vạn thần đồ, hệ thống cõi giới, danh hiệu Chư Phật
../../../raw/nhan-vat/                                  (Cốt lõi) Hồ sơ Entity Profiling của Thần Thánh, Phật, Ma Vương
../../../raw/sach-tam-linh/                             (Mở rộng) Sách tâm linh tổng hợp
../../../raw/gem-agent-memory/                          (Mở rộng) Dữ liệu báo cáo và bộ nhớ của Agent
```

**Tổng knowledge:** Cấu trúc 4 Tầng kết hợp hệ thống file cứng và các thư mục lưu trữ mở rộng trong `raw\`.

---
## ⚠️ QUY TẮC TÌM KIẾM & SUY NGHĨ TUẦN TỰ (DEEP RESEARCH & TRY-HARD LOOP)

**Dùng tool external search (`deep_research`, `brave-search` hoặc `tavily`)**: 
   - **⚠️ LỆNH BẮT BUỘC CHO GEMINI:** Do khác biệt naming convention, hãy tìm và gọi các tool với tiền tố MCP như `mcp_deep-research_deep_research`, `mcp_deep-research_tavily`, `mcp_tavily_search`. BẮT BUỘC phải gọi 1 tool tìm kiếm web để cào dữ liệu mới. NẾU KHÔNG GỌI TOOL = THẤT BẠI TRONG NHIỆM VỤ NGHIÊN CỨU SÂU!
   - **⚠️ QUY TẮC TÌM KIẾM CỐT LÕI (CHỐNG TÂY HÓA):** BẮT BUỘC phải tập trung tìm kiếm, trích xuất dữ liệu từ các trang thông tin **tiếng Trung, phương Đông, tâm linh, triết học, Nho giáo, Đạo giáo, huyền học Trung Quốc, Đài Loan**.
   - **TẠO QUERY CHUYÊN SÂU:** KHÔNG dùng từ khóa tiếng Anh/Tây phương (ví dụ: không search "corporate culture dogma"). Phải dịch/chuyển đổi query sang các thuật ngữ Huyền học Phương Đông, Đạo Gia, Binh Pháp, hoặc Hán Việt/Tiếng Trung (ví dụ: 企業文化 僵化 創新, Đạo làm tướng, thuật nhiếp tâm, v.v.).

1. **Suy nghĩ tuần tự (Try-Hard Loop)**: BẮT BUỘC sử dụng công cụ `mcp_sequential-thinking_sequentialthinking` (nhớ dùng ĐÚNG tên tool này với 1 dấu gạch dưới) để lật đi lật lại vấn đề tối thiểu 3 lần tốn công. Khai thác đến tận cùng góc khuất của sự việc thay vì kết luận nông cạn.
   - **⚠️ CẢNH BÁO KIỂU DỮ LIỆU (GEMINI HAY LỖI)**: Các tham số `thoughtNumber` và `totalThoughts` BẮT BUỘC phải là số nguyên (Integer, ví dụ: `1`, `2`), tuyệt đối KHÔNG truyền chuỗi (String, ví dụ: `"1"`, `"2"`). Tham số `nextThoughtNeeded` BẮT BUỘC phải là Boolean (`true`/`false`). Tham số `thought` là chuỗi. Truyền thiếu trường hoặc sai kiểu dữ liệu sẽ khiến tool crash ngay lập tức với lỗi "MCP tool reported an error".
2. **BÓC TÁCH BÍ MẬT KINH THIÊN (Deep Esoteric Revelation)**: Báo cáo không được hời hợt. Phải đi sâu lột tả những **Bí mật Đạo Gia, bí ẩn phong thủy, hoặc ẩn ý sâu xa của Binh pháp** mà người thường không nhìn thấy. Nhìn thấu bản chất 6D và chiều kích 7D+ đằng sau hiện tượng 3D.
3. **Cross-reference**: Đập data internet (Phương Đông/Trung Quốc) vào data local. Tìm khoảng trống, mâu thuẫn, kết nối chưa ai thấy.
4. **Phú ngẫu ngôn từ**: Không bao giờ tóm tắt khô khan hay gõ đầu dòng lèo tèo. Mỗi đoạn phải phân tích sâu, dài 10-15 câu liên kết logic. Phải diễn giải bằng hình tượng hóa (Imagery) siêu hình quyền lực.
5. **Áp dụng can chi hiện tại**: Nhúng Bazi MCP vào bối cảnh thời điểm hiện tại để đưa ra đề xuất hành động cho tuần tới / tháng tới.
