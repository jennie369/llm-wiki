# Skill: Nguyệt Vận Analysis (Monthly Fortune)

## Khi nào kích hoạt
Khi Chủ Tướng hỏi về vận tháng, dự báo tháng, kế hoạch tháng, hoặc bất kỳ câu hỏi "tháng này/tháng sau nên làm gì?"

## Quy trình thực hiện

### Bước 1: Khởi xuất Nguyệt Vận qua MCP Tool (BẮT BUỘC)
- Gọi tool `tuvi__getNguyetVan({ solarDate, hour, gender, year })` 🆕 — ra thẳng **12 cung Nguyệt Vận chuẩn VN** (neo **Cung Tiểu Hạn**, T1 = Tiểu Hạn +2 thuận; nam thuận / nữ nghịch xử lý TỰ ĐỘNG). Mỗi tháng kèm chính tinh (độ sáng VN) + phụ tinh natal. Field `months[m-1]` = tháng m.
- LƯU Ý: KHÔNG tự đếm cung bằng tay (sai tháng nhuận / sai chiều giới tính). KHÔNG neo theo Chi Năm (bug cũ — nam nữ ra giống nhau). Công thức SSOT: `tools/FRAMEWORK_NGUYET_VAN_SSOT.md` (dùng chung phap-su).
- Đại Vận / Lưu Niên / Lưu Nhật-Thời (cấp khác) dùng `tuvi__getHoroscope` với `targetDate`. Chỉ tự chuyển đổi sao mệnh cũ lá số Tham Lang nếu đã verify 100%.

### Bước 2: Tra cứu dữ liệu sẵn có
- Đọc `nguyet-van-2026-tham-lang.html` → lấy phân tích tổng quan tháng.
- Đọc `framework-nguyet-van-v6-complete THAM LANG.md` → áp dụng 15 bước phân tích V6.0 theo framework.

### Bước 3: Tính điểm 5 lớp (Áp dụng từ kết quả của MCP)
```
Lớp 1: Chính Tinh gốc tại cung lưu nguyệt (Miếu/Vượng/Hãm)
Lớp 2: Tứ Hóa Lưu Nguyệt (Can tháng do MCP trả về)
Lớp 3: Tứ Hóa Lưu Niên 2026 chồng lên
Lớp 4: Tứ Hóa Đại Vận 45-54 chồng lên
Lớp 5: Tứ Hóa Gốc (Can Ất) chồng lên
```

### Bước 4: Quét Red Flags
- Áp dụng 10 Red Flag codes (RF-01 đến RF-10) vào dữ liệu MCP truy xuất.
- Đặc biệt chú ý RF-01 (Song Kỵ) và RF-08 (Phúc Đức bị Kỵ)

### Bước 5: Xuất báo cáo
Format output theo template trong AGENTS.md (section "Báo cáo nguyệt vận")

## Dữ liệu Nguyệt Vận 2026 Tham Lang (Quick Reference)

| Tháng | Điểm | Cung | Nhận xét chính |
|-------|------|------|---------------|
| T1 | +18 | Phu Thê | Tử Vi + Thiên Phủ Miếu, kết liên minh |
| T2 | -12 | Huynh Đệ | NGUY HIỂM NHẤT, Song Kỵ, ĐÓNG BĂNG |
| T3 | +5 | Mệnh | Mạnh ở nhà, yếu ở ngoài, KHÔNG đi xa |
| T4 | -8 | Phụ Mẫu | Tham Lang Kỵ, KHÔNG cờ bạc/đầu cơ |
| T5 | -10 | Phúc Đức | Kỵ Lưu Niên, BẮT BUỘC cúng tổ tiên |
| T6 | +22 | Điền Trạch | ĐỈNH CAO NĂM, Song Lộc + Song Quyền, ALL-IN BĐS |
| T7 | +12 | Quan Lộc | Thất Sát Miếu, mở rộng sự nghiệp |
| T8 | +18 | Nô Bộc | Tam Lộc, xây đội ngũ, ủy quyền |
| T9 | +10 | Thiên Di | Tham Lang Lộc vào Mệnh, networking |
| T10 | +2 | Tật Ách | Kiểm tra sức khỏe, Tham Lang Quyền |
| T11 | +8 | Tài Bạch | Đại Vận cộng hưởng, tái cấu trúc tài chính |
| T12 | +15 | Tử Tức | Lộc Gốc, ra mắt sản phẩm, thu hoạch cuối năm |

## 5 Quy Tắc Vàng 2026
1. **T2 đóng băng** -- không hành động mới, không ký hợp đồng
2. **T6 all-in** -- dồn toàn lực vào BĐS, tài sản lớn
3. **Cảnh giác đồng nghiệp nữ** -- Thái Âm Kỵ Gốc suốt năm
4. **Chuyển đổi tiền mặt** -- sang BĐS/vàng (tránh mất thanh khoản)
5. **Cúng tổ tiên đều đặn** -- đặc biệt T5 bắt buộc
