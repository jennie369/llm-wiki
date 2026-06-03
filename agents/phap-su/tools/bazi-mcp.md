# Tool: Hệ Sinh Thái MCP Bazi & Tuvi (Web Dashboard Wrapper)

## THÔNG BÁO KIẾN TRÚC MỚI (UPDATE QUAN TRỌNG)
Hệ thống Tử Vi NTP CŨ (`D:\Claude Projects\GEMINI...`) ĐÃ BỊ LOẠI BỎ hoàn toàn. Thay vào đó, chúng ta có một **Local MCP Wrapper Siêu Việt (Chạy Độc Lập)** được nạp trực tiếp vào dự án App Phong Thủy Đế Vương (Web Dashboard). 

💡 **Lợi ích kiến trúc này:** Các Agent (như Paperclip) KHÔNG CẦN CHỜ Next.js Server khởi động! Agent giao tiếp qua `mcp.json` sử dụng StdIO nhưng **chạy TRỰC TIẾP toàn bộ 4 nhánh Core Engine hiện đại nhất từ Web Dashboard API (`iztro`, `tyme4ts`, `cantian-tymext`)**.

---

## Danh Sách Các Tools Cung Cấp Bởi MCP Wrapper Mới

Tất cả các API Route phức tạp của Web Dashboard (`tuvi`, `bazi`, `horoscope`, `charts`) nay đã được **tích hợp thành MCP Tool** để Agent gọi mà không cần HTTP request.

### Nhóm 1: Tử Vi Hoàng Đạo (Engine: `api/tuvi`)
- **Tool:** `tuvi__getChartVN` 🆕 ⭐ — **MẶC ĐỊNH cho an sao / luận mệnh chuẩn Việt Nam** (engine thuần Việt port lasotuvi).
  - **Input:** `solarDate` (YYYY-MM-DD), `hour` (index iztro 0-12: Tý=0, Sửu=1... **Thìn=4**, Tý muộn=12), `gender` (0 nữ, 1 nam).
  - **Hơn `tuvi__getChart` ở:** độ sáng (miếu/vượng/hãm) chuẩn VN + đủ phụ tinh VN (Đường Phù, Quốc Ấn, Thiên Y, Văn Tinh, Lưu Hà, Đẩu Quân...) + Hỏa-Linh theo **trường phái Altuvi** (⚠️ mới verify 1 lá số). Chỉ **natal** (không vận hạn).
- **Tool:** `tuvi__getChart` — lá số iztro (chuẩn Tàu): **chính tinh + Tứ Hóa + An Mệnh (kể cả nhuận tháng) ĐÚNG**, nhưng độ sáng + phụ tinh theo Tàu. Dùng để **đối chiếu** hoặc khi cần shape iztro. Input giống getChartVN.
- **Phân tích:** Lập lá số → luận sao giải họa. Ưu tiên `getChartVN` cho độ sáng/phụ tinh; đối chiếu `getChart` khi cần.

### Nhóm 2: Bát Tự & Hoàng Lịch (Engine: `api/bazi`)
*Đã bao gồm thuật toán build 14 trường tàng can, Thần sát (`getShen`), Thập thần và lịch vạn sự.*
- **Tool:** `bazi__getBaziDetail`
- **Input:** `solarDatetime` (ISO), `gender` (0 nữ, 1 nam)
- **Output mới (2026-06-02):** ngoài 4 trụ + Thập Thần + Thần Sát, nay trả thêm:
  - `关系` — **Hình-Xung-Phá-Hại-Hợp** + tam hợp/tam hội/củng/song xung/song hợp giữa 4 trụ (qua `calculateRelation`).
  - `五行统计` — đếm cân bằng ngũ hành (4 thiên can + tàng can) → cơ sở luận **Dụng Thần**.
- **Tool:** `bazi__getSolarTimes` (Tìm lịch dương theo bát tự).
- **Tool:** `bazi__getDaYun` 🆕 — **Đại Vận Bát Tự + Luận Vận Hạn**: thuận/nghịch, thời điểm khởi vận, chuỗi N trụ đại vận (10 năm/trụ) — **mỗi trụ kèm `与命局关系`** (xung/hợp/hình/hại/phá với tứ trụ gốc, qua `appendRelation`). Truyền `targetYear` → thêm block **`流年`** luận Lưu Niên năm đó (can chi + đại vận chứa nó + quan hệ với mệnh gốc).
  - **Input:** `solarDatetime` (ISO), `gender` (0 nữ, 1 nam), `count` (số đại vận, mặc định 9), `targetYear` (năm dương muốn luận lưu niên — optional).
- **Tool:** `bazi__getChineseCalendar` (Khởi quẻ ngày tốt xấu Hoàng Lịch, nạp âm, việc Nên/Tránh, tuổi xung).
- **Phân tích:** Dành để xem nạp âm ngũ hành, dụng thần bát tự, quan hệ trụ, vận hạn 10 năm hoặc chọn ngày giờ.

### Nhóm 3: Vận Hạn Horoscope (Engine: `api/horoscope`)
- **Tool:** `tuvi__getHoroscope`
- **Input:** Ngày sinh (solarDate, hour, gender) + `targetDate` (Ngày muốn xem)
- **Output:** Tuổi xung, Cung lưu niên, Sao Lưu, Đại Vận, Tiểu Hạn, Lưu Nguyệt/Nhật/Thời. (Age, Decadal, Yearly, Monthly).
- **Tool:** `tuvi__getNguyetVan` 🆕 ⭐ — **Nguyệt Vận 12 tháng chuẩn VN** (Nguyệt Hạn). Neo **Cung Tiểu Hạn** (nam thuận / nữ nghịch xử lý tự động), Tháng 1 = Tiểu Hạn **+2 cung thuận**, rồi thuận 12 tháng. Kèm chính tinh (độ sáng VN) + phụ tinh natal mỗi cung tháng để luận.
  - **Input:** `solarDate`, `hour` (index 0-12), `gender` (0 nữ/1 nam), `year` (năm dương muốn xem, vd 2026).
  - **Công thức SSOT:** `FRAMEWORK_NGUYET_VAN_SSOT.md`. ⚠️ KHÔNG neo theo Chi Năm (bug cũ — nam nữ ra giống nhau = sai).

### Nhóm 4: Dữ liệu Lá Số (Engine: `api/charts`)
- **Tool:** `charts__list`
- Lấy toàn bộ danh sách khách hàng đang được nạp vào DB json cục bộ của Dashboard để cross-check lá số.

---

## Server `taibu` 🆕 (2026-06-02) — 15 tool đa hệ huyền học (engine taibu, MIT)

> **Bản chất:** MCP server thứ 4 (`taibu`), vendored tại `App Phong Thủy Đế Vương/web-dashboard/vendor/taibu` (chạy `node .../packages/mcp/dist/index.js`). Engine bên ngoài (太卜/hhszzzz) — **output CHỮ HÁN**, agent tự luận sang **tiếng Việt có dấu**.
> **Naming runtime:** Claude `mcp__taibu__<tool>` · Gemini CLI `mcp_taibu_<tool>`.

### ⚖️ Routing — KHI NÀO dùng taibu, khi nào dùng server cũ
- **Bát Tự + Tử Vi của khách VN** (lá số chính, hiển thị web) → **VẪN dùng server `bazi`/`tuvi`** (đã Việt hóa Mệnh/Thân Chủ + Tuần/Triệt, nối trang web). taibu cũng có `bazi`/`ziwei` nhưng chữ Hán phái Đài/đại lục — chỉ dùng để **đối chiếu chéo**, KHÔNG thay.
- **8 hệ MỚI mà server cũ KHÔNG có** → dùng `taibu` (xem dưới).
- **Phong thủy không gian** (Bát Trạch, phi tinh nhà, loan đầu, âm trạch) → vẫn server `phongthuy`.

### 🆕 Nhóm 5a — 8 hệ MỚI (chỉ taibu mới có)
| Tool | Hệ | Input chính (required) | Dùng khi |
| --- | --- | --- | --- |
| `taibu__ziwei_flying_star` | Tử Vi **phi tinh** (tứ hóa phi bố, tự hóa, tam phương tứ chính) | `gender`, `birthYear/Month/Day/Hour`, `queries[]` (mỗi query cần cung cụ thể) | Luận sâu tứ hóa bay cung, sau khi đã có lá số Tử Vi |
| `taibu__liuyao` | **Lục Hào** (gieo quẻ theo câu hỏi) | `question`, `yongShenTargets[]` (父母/兄弟/子孙/妻财/官鬼 — agent tự chọn theo chủ đề hỏi), `date` (ISO) | Khách hỏi 1 việc cụ thể (cầu tài, hợp tác, kiện tụng...) → gieo quẻ đoán cát hung + ứng kỳ |
| `taibu__meihua` | **Mai Hoa Dịch Số** | (số/giờ/chữ — xem schema MCP) | Lập quẻ nhanh từ con số/thời điểm/chữ khách đưa |
| `taibu__tarot` | **Tarot** (78 lá, 9 trải bài) | `spreadType` (single/three-card/love/celtic-cross/horseshoe/decision/mind-body-spirit/situation/yes-no), `question`, `allowReversed` | Khách thích phương Tây / hỏi tình cảm-sự nghiệp ngắn hạn |
| `taibu__daliuren` | **Đại Lục Nhâm** (天地盘/四课/三传) | (giờ + câu hỏi — xem schema) | Đoán sự việc cấp cao, chuyên sâu (output rất dày) |
| `taibu__xiaoliuren` | **Tiểu Lục Nhâm** (bấm độn nhanh) | (giờ — xem schema) | Đoán nhanh xuất hành, việc nhỏ tức thời |
| `taibu__taiyi` | **Thái Ất** thần số (cửu tinh) | (thời/cục — xem schema) | Xem cục diện lớn, dự án/môi trường ngoại cảnh |
| `taibu__astrology` | **Chiêm tinh Tây** (bản mệnh + lưu vận) | `birthYear/Month/Day/Hour`, `latitude`, `longitude`, `birthPlace`, `transitDateTime` | Khách muốn xem cung hoàng đạo / transit phương Tây |

### Nhóm 5b — Tool taibu trùng hệ cũ (để đối chiếu, KHÔNG thay server VN)
`taibu__bazi` (51 thần sát), `taibu__bazi_pillars_resolve`, `taibu__bazi_dayun` (+tiểu vận/thái tuế), `taibu__ziwei`, `taibu__ziwei_horoscope`, `taibu__almanac`, `taibu__qimen`.

> ⚠️ taibu output chữ Hán + phái Đài/đại lục → chỉ dùng **cross-check** lá số chính (server `bazi`/`tuvi` Việt hóa mới là SSOT cho khách VN).

---

## Quy Trình Chuẩn Khi Tư Vấn Lá Số
1. Hỏi khách hàng: Ngày giờ sinh dương lịch hoặc âm lịch + Giới tính.
2. Dùng tool `tuvi__getChartVN` (mặc định an sao chuẩn VN) hoặc `bazi__getBaziDetail` tùy hệ quy chiếu do khách mong muốn (Tử vi hay Tứ trụ). Dùng `tuvi__getChart` (iztro) để đối chiếu khi cần.
3. Luận Nguyệt Vận bằng `tuvi__getNguyetVan` (`year` = năm muốn xem) — ra thẳng 12 cung tháng + sao chuẩn VN. Đại vận / Lưu niên / Lưu nhật-thời dùng `tuvi__getHoroscope` với `targetDate`.
4. KHÔNG TỰ TÍNH ÂM DƯƠNG LỊCH HOẶC SAO BẰNG TAY vì LLM hay sai lịch Nhuận. Luôn dùng kết quả từ Wrapper do thư viện `tyme4ts` phân giải.
5. Bát Tự nâng cao: `bazi__getBaziDetail` nay trả thêm `关系` (Hình-Xung-Phá-Hại-Hợp) + `五行统计` (cân bằng ngũ hành / dụng thần); `bazi__getDaYun` cho Đại Vận bát tự (thuận/nghịch + chuỗi 10 năm).

> **Maintainer / nâng cấp engine:** xem reference kỹ thuật đầy đủ (tool inventory, coverage map, gotchas, backlog) tại `tools/METAPHYSICS_MCP_ENGINE_REFERENCE.md` (cùng folder). Engine wrapper code: `App Phong Thủy Đế Vương/web-dashboard/scripts/bazi_wrapper.mjs`.
