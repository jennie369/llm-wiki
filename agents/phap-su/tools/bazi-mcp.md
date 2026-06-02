# Tool: Hệ Sinh Thái MCP Bazi & Tuvi (Web Dashboard Wrapper)

## THÔNG BÁO KIẾN TRÚC MỚI (UPDATE QUAN TRỌNG)
Hệ thống Tử Vi NTP CŨ (`D:\Claude Projects\GEMINI...`) ĐÃ BỊ LOẠI BỎ hoàn toàn. Thay vào đó, chúng ta có một **Local MCP Wrapper Siêu Việt (Chạy Độc Lập)** được nạp trực tiếp vào dự án App Phong Thủy Đế Vương (Web Dashboard). 

💡 **Lợi ích kiến trúc này:** Các Agent (như Paperclip) KHÔNG CẦN CHỜ Next.js Server khởi động! Agent giao tiếp qua `mcp.json` sử dụng StdIO nhưng **chạy TRỰC TIẾP toàn bộ 4 nhánh Core Engine hiện đại nhất từ Web Dashboard API (`iztro`, `tyme4ts`, `cantian-tymext`)**.

---

## Danh Sách Các Tools Cung Cấp Bởi MCP Wrapper Mới

Tất cả các API Route phức tạp của Web Dashboard (`tuvi`, `bazi`, `horoscope`, `charts`) nay đã được **tích hợp thành MCP Tool** để Agent gọi mà không cần HTTP request.

### Nhóm 1: Tử Vi Hoàng Đạo (Engine: `api/tuvi`)
*Đã bao gồm thuật toán tính Tuần Không, Triệt Lộ, isLeapMonth, Mệnh/Thân Chủ chuẩn Việt Nam.*
- **Tool:** `tuvi__getChart`
- **Input:** `solarDate` (YYYY-MM-DD), `hour` (ví dụ Tí là 0), `gender` (0 nữ, 1 nam).
- **Phân tích:** Dành để luận sao giải họa tổng quát.

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
- **Output:** Tuổi xung, Cung lưu niên, Sao Lưu, Đại Vận, Tiểu Hạn, Nguyệt Vận. (Age, Decadal, Yearly, Monthly).

### Nhóm 4: Dữ liệu Lá Số (Engine: `api/charts`)
- **Tool:** `charts__list`
- Lấy toàn bộ danh sách khách hàng đang được nạp vào DB json cục bộ của Dashboard để cross-check lá số.

## Quy Trình Chuẩn Khi Tư Vấn Lá Số
1. Hỏi khách hàng: Ngày giờ sinh dương lịch hoặc âm lịch + Giới tính.
2. Dùng tool `tuvi__getChart` hoặc `bazi__getBaziDetail` tùy hệ quy chiếu do khách mong muốn (Tử vi hay Tứ trụ).
3. Luận Nguyệt Vận bằng cách gọi `tuvi__getHoroscope` với `targetDate` chỉ định để ra các Đại vận và Tiểu hạn.
4. KHÔNG TỰ TÍNH ÂM DƯƠNG LỊCH HOẶC SAO BẰNG TAY vì LLM hay sai lịch Nhuận. Luôn dùng kết quả từ Wrapper do thư viện `tyme4ts` phân giải.
5. Bát Tự nâng cao: `bazi__getBaziDetail` nay trả thêm `关系` (Hình-Xung-Phá-Hại-Hợp) + `五行统计` (cân bằng ngũ hành / dụng thần); `bazi__getDaYun` cho Đại Vận bát tự (thuận/nghịch + chuỗi 10 năm).

> **Maintainer / nâng cấp engine:** xem reference kỹ thuật đầy đủ (tool inventory, coverage map, gotchas, backlog) tại `tools/METAPHYSICS_MCP_ENGINE_REFERENCE.md` (cùng folder). Engine wrapper code: `App Phong Thủy Đế Vương/web-dashboard/scripts/bazi_wrapper.mjs`.
