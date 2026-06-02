# Tool: Ritual Protocol Engine

## Mô tả
Tra cứu và hướng dẫn các nghi lễ tâm linh, hỏa cúng, giải kết, sám hối ứng dụng trong hệ thống Phong Thủy & Tâm Linh. 
Mọi nghi thức phải bắt buộc tuân thủ nguyên tắc: **Tâm thành, Ngã mạn ngắt, Ý chí thanh tịnh.**

## Chức năng

### 1. tra_cuu_nghi_le (Ritual Lookup)
**Input:** Tên nghi lễ hoặc mục đích (VD: "Muốn xả xui", "Cúng mùng 2")
**Output:** Quy trình đầy đủ, vật phẩm, thời gian, khẩu quyết

**Danh mục 10 nghi lễ & pháp môn chính:**

| # | Tên Pháp Môn/Nghi Lễ | Nguồn chiếu | Mục đích & Ý nghĩa |
|---|----------------------|-------------|--------------------|
| 1 | **Hỏa Cúng Homa** | `Hoả Cúng Homa.md` | Pháp môn đốt cháy cúng dường qua nguyên tố Lửa. Chia 4 mục đích: Tăng Ích, Trừ Tai, Hàng Phục, Kính Ái. |
| 2 | **Giải Kết Đại Đàn Trần Triều** | `TRẦN TRIỀU GIẢI KẾT.md` | Giải oan trái nghiệp chướng dòng họ, cắt oán khí nhiều đời. |
| 3 | **Giải Phóng Trấn Nhân** | `Lễ Giải Phóng Trấn Nhân.md` | Hóa giải bùa ngải, ác tinh, nguyền rủa mượn từ đối thủ cạnh tranh. |
| 4 | **Sám Hối Tổ Tiên** | `Lễ Sám Hối.md` | Sám hối nợ nần gia tiên, thường niên 01/11 ÂL. |
| 5 | **Triệu Hồi Hội Đồng Phúc Đức**| `BINH PHÁP THỰC CHIẾN.md` | Triệu thỉnh 5 vị Tổ tiên chiến đấu, thiết lập hàng rào phòng thủ Tâm linh. |
| 6 | **Nuôi & Cúng Lộc Tồn** | `BINH PHÁP THỰC CHIẾN.md` | Tại gia/Công ty, Cúng mùng 2 & 16 ÂL lấy sinh khí mở kho tài lộc. |
| 7 | **Cửu Ngũ Chí Tôn** | `CÔNG THỨC CỬU NGŨ CHÍ TÔN.md` | Dùng trầm hương đặc chế kích hoạt hào quang, nạp Thiên Hỏa Dương Cực. |
| 8 | **Đại Lễ Tiếp Dẫn Long Mạch Yên Tử**| `PHÁP DUY TRÌ LONG MẠCH TÂM LINH.md`| Đồng bộ hóa trục Tâm linh nội thể vào Đại Long Mạch quốc gia, tiếp dẫn nguyên khí. |
| 9 | **Tẩy Tịnh Xả Trược (Daily)** | *New/Daily Practice* | Thanh tẩy rác năng lượng bằng sương, nước muối hạt và trầm trước khi đi ngủ. |
| 10| **Thiền Cư Trần Lạc Đạo (Daily)**| *Tư tưởng Trúc Lâm* | Thiền định "Đối cảnh vô tâm", xả ngã mạn, đưa não bộ về sóng Alpha/Theta. |

---

### 2. chuan_bi_vat_pham (Ritual Items Checklist)
**Input:** Tên nghi lễ
**Output:** Checklist vật phẩm đầy đủ (Prompt the user to prepare before proceeding)

**Vật phẩm cơ bản (Mandatory Core):**
- [ ] Trầm hương (Dòng cao cấp Cửu Ngũ Chí Tôn / Thất Bảo, hoặc Trúc Lâm Đại Quế)
- [ ] Nến đỏ/trắng tùy tính chất dương/âm (tối thiểu 1, thường 3 hoặc 5)
- [ ] Chén tịnh thủy (nước suối sạch)
- [ ] Hoa tươi (Sen, Cúc Vàng, Lay Ơn)
- [ ] Đĩa Nhất Quả / Ngũ Quả
- [ ] Gạo + Muối thô (để rắc sau khi làm lễ)

**Vật phẩm đặc trị (Add-ons):**
- *Hỏa Cúng Homa:* Lò đồng, củi đàn hương, các loại hạt (mè đen, mù tạt, vừng), bơ ghee.
- *Triệu Hồi Phúc Đức:* Kiếm kim loại chỉ hướng Bắc, làm lễ 23h.
- *Kết Nối Long Mạch:* Lệnh bài, la bàn phong thủy định hướng trục Bắc - Nam.
- *Giải Trấn Ngải:* Chuông Kim Cang (Chùy Kim Cang) để phá vỡ tần số thấp, vải trắng xả trược.

---

### 3. huong_dan_thuc_hanh (Practice Guide)
**Input:** Tên nghi lễ + mục đích
**Output:** Hướng dẫn 3 Phase: Preparation -> Execution -> Conclusion

**Ví dụ: Tứ Đại Hỏa Cúng:**
1. **TRỪ TAI (Tiêu trừ ác nghiệp, hóa giải bệnh):** Xoay mặt hướng Nam, mặc trang phục sáng màu (Trắng), dùng hạt Mè Đen ném vào lửa mang ý nghĩa rũ bỏ xui xẻo.
2. **TĂNG ÍCH (Tích phúc, cầu tài):** Nhìn hướng Bắc, trang phục Vàng/Cam. Cúng bằng bơ trong, mật ong, lúa mạch sấy. Mơ về sự nở rộ kinh doanh.
3. **KÍNH ÁI (Thu hút tình duyên, nhân sự):** Nhìn hướng Tây, trang phục Đỏ/Hồng. Cúng cúc hoa, cánh sen, dầu hoa hồng. Trì chú Chuẩn Đề.
4. **HÀNG PHỤC (Khống chế tiểu nhân, đối thủ):** Nhìn hướng Nam, mặc đồ u tối/Đỏ bầm. Vật cúng có vị cay đắng (Ớt, hạt tiêu, củ cải đắng). Tính sắt máu cao, chỉ dùng khi cùng cực.

**Thiền Xả Ngã Mạn (Phương pháp Trần Nhân Tông):**
- Ngồi kiết già/bán già. Thở sâu 4 nhịp. Định hình tư tưởng "Mọi sự ở đời là tùy duyên". 
- Hình dung cái "Tôi" đang thu nhỏ lại và tan biến vào Không Gian. Câu quyết: *"Đối cảnh vô tâm mạc vấn thiền"*.

---

### 4. tinh_thoi_gian_le (Ritual Timing Calculator)
**Input:** Lịch âm dương, tháng hiện tại
**Output:** Chốt ngày, giờ cụ thể để thi triển pháp môn (Canh theo Lưỡng Cực Âm - Dương).

**Lịch Cố Định Thường Niên:**
- **Thanh Minh:** Mở dòng chảy, phù hợp Kết Nối Long Mạch.
- **Rằm tháng 5 (Tết Đoan Ngọ):** Khí Dương cực thịnh -> Cúng Cửu Ngũ Chí Tôn, nạp linh khí Trầm.
- **Rằm tháng 7 (Vu Lan):** Khí Âm cực thịnh -> Trần Triều Giải Kết Đại Đàn, Siêu Độ, Phóng Sinh.
- **Đông Chí:** Đêm dài nhất -> Triệu thỉnh Âm binh, Giải Phóng Trấn Nhân ban đêm.
- **Mùng 1/11 ÂL:** Lễ đản sinh & Nhập Niết Bàn [[Phật Hoàng]] -> Sám Hối Tổ Tiên Đại Đàn.

**Giờ Hoàng Đạo Trong Ngày (Theo Mục Đích):**
- **05h - 07h (Giờ Mão):** Giao thoa sinh khí. Tốt cho nạp năng lượng 540Hz, Thiền quán, Sám hối.
- **11h - 13h (Giờ Ngọ):** Dương khí cực thịnh. Tốt cho Hỏa cúng Tăng Ích, nạp Thiên Hỏa cho văn phòng.
- **17h - 19h (Giờ Dậu):** Hoàng hôn giao thời. Tốt cho phóng sinh, thả trôi phiền muộn, lễ xả trược.
- **23h - 01h (Giờ Tý):** Âm dương nhập giao. Tối ưu cho Triệu Hồi Tổ Tiên, đàm đạo tâm linh, đánh trận ngầm (hàng phục).

## Quy Trình Bắt Buộc Trước Mọi Nghi Lễ (The Golden Rule)
1. Vệ sinh thân thể sạch sẽ. Súc miệng nước muối.
2. Tịnh hóa không gian bằng Trầm Hương / Tinh dầu 5-10 phút trước khi bắt đầu.
3. Không ôm tâm niệm sân hận cao độ khi bước vào đàn lễ (trừ Hàng Phục cần khởi nộ, nhưng sau đó phải xả).
4. **Khóa đàn lễ:** Mọi nghi lễ sau khi hoàn tất phải có bước Khóa đàn (Tạ ơn chư vị, vỗ tay 3 lần hoặc gõ Chuông để rẽ sóng năng lượng quay về đời thực 3D).
