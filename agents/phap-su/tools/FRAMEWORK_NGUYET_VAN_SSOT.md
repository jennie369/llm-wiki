# 📐 FRAMEWORK NGUYỆT VẬN — SSOT (Single Source of Truth)

> **Đây là nguồn DUY NHẤT cho CÔNG THỨC TÍNH CUNG NGUYỆT VẬN.**
> Mọi nơi khác (file V6 `...THAM LANG.md`, file V4 `...THIÊN ĐỒNG THÁI ÂM V4.md`,
> code web `HoroscopeSection.js`) đều phải khớp file này. Nếu lệch → file này đúng.
>
> - **Trạng thái:** ✅ Canonical · engine-verified
> - **Cập nhật:** 2026-06-03 03:32 (Asia/Ho_Chi_Minh)
> - **Engine kiểm chứng:** `iztro` (qua `lib/engine/tuvi.js` → `computeHoroscope`, field `age` = Tiểu Hạn)

---

## 1. CÔNG THỨC (quy tắc vàng)

> **NGUYỆT VẬN THÁNG 1 = CUNG TIỂU VẬN (Tiểu Hạn của năm) + 2 CUNG THUẬN.**
> Sau đó **đi thuận** qua 12 cung cho 12 tháng.

3 bước:

1. **Xác định Cung Tiểu Vận (Tiểu Hạn)** của năm cần xem.
2. Từ cung Tiểu Vận, **đếm thuận 2 cung** → cung Nguyệt Vận **Tháng 1**.
3. Từ cung Nguyệt Vận T1, **đi thuận** từng cung cho các tháng còn lại (T2 = T1+1, … T12 = T1+11).

---

## 2. GIỚI TÍNH — XỬ LÝ TỰ ĐỘNG (điểm cốt lõi, đừng làm sai lại)

**KHÔNG có quy tắc thuận/nghịch riêng cho Nguyệt Vận.** Giới tính chỉ đi vào DUY NHẤT
qua **Cung Tiểu Hạn**:

- **Tiểu Hạn NAM → đi THUẬN** (cung tăng theo tuổi)
- **Tiểu Hạn NỮ → đi NGHỊCH** (cung giảm theo tuổi)

Vì Tiểu Hạn nam/nữ chạy ngược chiều nhau, **Nguyệt Vận của nam và nữ TỰ KHẮC khác nhau**
dù cùng năm. → Tuyệt đối **KHÔNG** neo Nguyệt Vận theo "Chi Năm (Lưu Niên)", vì cách đó
bỏ qua con người → nam nữ ra giống hệt nhau = **SAI** (đây là bug đã sửa 2026-06-03).

### Cách lấy Cung Tiểu Hạn
- **Engine (khuyến nghị):** dùng `computeHoroscope(...).age.earthlyBranch` — iztro đã tính sẵn nam-thuận/nữ-nghịch.
- **Bấm tay (lệ cổ điển):** chi năm sinh chia 4 nhóm tam hợp, khởi Tiểu Hạn tuổi 1 tại cung cố định, nam thuận / nữ nghịch, mỗi năm 1 cung:
  - Thân-Tý-Thìn → khởi **Tuất**
  - Dần-Ngọ-Tuất → khởi **Thìn**
  - Tỵ-Dậu-Sửu → khởi **Mùi**
  - Hợi-Mão-Mùi → khởi **Sửu**

---

## 3. VÍ DỤ KIỂM CHỨNG (lá số NỮ Quý Dậu 16/05/1993, Mệnh Đồng Âm tại Tý)

Nữ, chi năm sinh **Dậu** ∈ nhóm Tỵ-Dậu-Sửu → khởi Tiểu Hạn tại **Mùi**, **đi nghịch**.

| Tuổi | Năm | Cung Tiểu Vận | Địa chi | Nguyệt Vận T1 (+2 thuận) |
|------|-----|---------------|---------|--------------------------|
| 33 | 2025 | Huynh Đệ | Hợi | **Sửu** (Phụ Mẫu) |
| 34 | 2026 | Phu Thê | Tuất | **Tý** (Mệnh) |
| 35 | 2027 | Tử Tức | Dậu | **Hợi** (Phụ Mẫu) |

Bảng 12 tháng năm 2026 (nữ, Tiểu Hạn Tuất → T1 Tý):
`Tý → Sửu → Dần → Mão → Thìn → Tỵ → Ngọ → Mùi → Thân → Dậu → Tuất → Hợi`

Cùng người nhưng **NAM** (Tiểu Hạn 2026 = Thìn → T1 Ngọ):
`Ngọ → Mùi → Thân → Dậu → Tuất → Hợi → Tý → Sửu → Dần → Mão → Thìn → Tỵ`
→ Khác hẳn nữ, đúng như kỳ vọng.

---

## 4. TRIỂN KHAI TRONG CODE

| Nơi | Chi tiết |
|-----|----------|
| Engine Tiểu Hạn | `web-dashboard/lib/engine/tuvi.js` → `computeHoroscope` trả `age` (Tiểu Hạn, nam thuận/nữ nghịch) |
| Engine Nguyệt Vận (SSOT công thức) | `web-dashboard/lib/engine/tuvi-vn/nguyetVan.js` → `nguyetVanBranch(ageBranchCn, month)` = `(ageIdx + 2 + (month-1)) % 12` + `computeNguyetVanYear(ageBranchCn)` (12 tháng) |
| UI | `…/components/tuvi/HoroscopeSection.js` → import `nguyetVanBranch` từ engine (SSOT, không inline nữa) |
| **MCP tool** 🆕 | `tuvi__getNguyetVan({solarDate, hour, gender, year})` (`bazi_wrapper.mjs`) → trả thẳng 12 cung tháng + chính/phụ tinh natal. Engine-verified golden 2026-06-03 (nữ 2026 子丑..亥 / nam 午未..巳). |
| API | `…/app/api/horoscope/route.js` (POST, gọi `computeHoroscope`) |

`nguyetVanBranch` **chỉ nhận** `ageBranchCn` (= `data.age.earthlyBranch`) + `month` — **KHÔNG nhận `genderNum`** (giới tính đã nằm trong Tiểu Hạn).

---

## 5. ĐÍNH CHÍNH LỊCH SỬ (để không lặp lại)

1. **Bỏ phương pháp "Chi Năm → bảng cố định"** (V6 cũ): neo theo Lưu Niên, mù giới tính → nam nữ giống nhau. SAI.
2. **Bỏ comment bịa "NỮ = THUẬN"** trong code cũ: framework gốc chỉ ghi "NAM = THUẬN", phần nữ chưa từng được định nghĩa; suy luận "luôn thuận" là sai.
3. **Sửa lỗi gõ máy V4 §8/§9:** Tiểu Vận 2027 (tuổi 35) bản V4 ghi "Thìn" → đúng là **Dậu (Tử Tức)** (engine + lệ cổ điển + xác nhận của chuyên gia 2026-06-03).

---

## 6. LIÊN QUAN
- File luận giải đầy đủ (playbook 15 bước, quét kỵ, diễn giải sao): `framework-nguyet-van-v6-complete THAM LANG.md` — **chỉ là tài liệu DIỄN GIẢI/ví dụ**, công thức tính lấy theo file SSOT này.
- File nguồn V4: `GEM_Knowledge_Vault/.../FRAMEWORK_NGUYET_VAN_THIÊN ĐỒNG THÁI ÂM V4.md` (§8 công thức gốc).
