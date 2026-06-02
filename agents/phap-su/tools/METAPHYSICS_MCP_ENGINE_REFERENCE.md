# Metaphysics MCP Engine Reference — Bát Tự · Tử Vi · Phong Thủy

> **Mục đích:** File tra cứu kỹ thuật cho **maintainer** (chị Jennie + Claude) khi tra tool / nâng cấp engine.
> **Khác với** `llm-wiki/agents/phong-thuy-de-vuong/tools/bazi-mcp.md` (guide agent-facing, ngắn gọn cho runtime).
> **Last verified:** 2026-06-02 (audit + nâng cấp wrapper v4.0.0 → thêm quan hệ + Đại Vận bát tự)

---

## 0. Bản đồ nhanh (TL;DR)

```
4 MCP server huyền học  (khai báo trong mỗi agent: <agent>/mcp.json)
├── bazi       → node  bazi_wrapper.mjs   (App Phong Thủy/web-dashboard/scripts)  ← engine chính VN, 7 tool
│                 └─ engines: tyme4ts + cantian-tymext + iztro  (node_modules)
├── taibu  🆕  → node  vendor/taibu/packages/mcp/dist/index.js  (App Phong Thủy/web-dashboard) ← 15 tool, +8 hệ MỚI
│                 └─ engines: tyme4ts + iztro + lunar-javascript + liuren-ts-lib + circular-natal-horoscope-js (MIT vendored)
├── phongthuy  → python phongthuy-mcp-server.py  (crypto-pattern-scanner/scripts) ← Bát Trạch, Phi Tinh, Kỳ Môn
└── timemap    → uvx    timemap-mcp        (pip package ngoài, github.com/cnick26)  ← Tiết khí, Hexagram, Day Quality
```

> **`taibu` (太卜, MIT, hhszzzz)** — vendored + cắt gọn (chỉ `packages/core`+`packages/mcp`, web/app AGPL đã gỡ). 8 hệ MỚI server cũ KHÔNG có: `ziwei_flying_star`, `liuyao`, `meihua`, `tarot`, `daliuren`, `xiaoliuren`, `taiyi`, `astrology`. 7 tool trùng (`bazi`/`bazi_dayun`/`ziwei`/`ziwei_horoscope`/`almanac`/`qimen`/`bazi_pillars_resolve`) = đối chiếu chéo, KHÔNG thay server `bazi` Việt hóa. Output chữ Hán. So sánh + verify lá số vàng: `crypto-pattern-scanner/memory/reports/2026-06-02-taibu-vs-current-metaphysics-engine-comparison.md`. Rollout 8 tool: `...2026-06-02-taibu-8-tools-rollout-plan.md`.

⚠️ **Naming theo runtime:** Claude = `mcp__bazi__<tool>` (double underscore) · Gemini CLI = `mcp_bazi_<tool>` (single).

---

## 1. Kiến trúc — 3 MCP server

| Server        | Command  | File / Source                                                    | Engine nền                                   |
| ------------- | -------- | ---------------------------------------------------------------- | -------------------------------------------- |
| **bazi**      | `node`   | `App Phong Thủy Đế Vương/web-dashboard/scripts/bazi_wrapper.mjs` | tyme4ts, cantian-tymext, iztro               |
| **phongthuy** | `python` | `crypto-pattern-scanner/scripts/phongthuy-mcp-server.py`         | (Python nội bộ)                              |
| **timemap**   | `uvx`    | `timemap-mcp` (pip, github.com/cnick26/timemap-mcp, MIT)         | NASA JPL DE421 ephemeris, 740+ test Joey Yap |

> Khai báo cụ thể trong `<agent>/mcp.json` (vd `llm-wiki/agents/phong-thuy-de-vuong/mcp.json`).
> Wrapper chạy **StdIO** → agent gọi trực tiếp, KHÔNG cần Next.js server bật.

### ⚙️ SSOT engine bát tự (2026-06-02) — chống drift agent ↔ web

Logic bát tự (computeBaziDetail + computeDaYun) nằm DUY NHẤT ở **`web-dashboard/lib/engine/bazi.js`**.
Cả 2 nơi import từ đó — sửa 1 chỗ, cả 2 ăn theo:
- **MCP wrapper** (`scripts/bazi_wrapper.mjs`) — cho agent (Pháp Sư/PTĐV/Buddha).
- **Web API routes** — cho trang Tử Vi: `app/api/bazi` (getBaziDetail) + `app/api/dayun` (getDaYun). Trang `app/tu-vi/[id]` render qua `BaziSectionFull` (quan hệ + ngũ hành) + `BatTuDaiVanTable` (đại vận + lưu niên).

> ⚠️ Trước đây web có engine copy riêng (drift): `api/bazi` thiếu 关系/五行统计, không có đại vận. Đã gộp về SSOT 2026-06-02.

---

## 2. Engine layer (thư viện) — server `bazi`

| Package            | Version | Vai trò                                                                                                  | Loại dep                         |
| ------------------ | ------- | -------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **tyme4ts**        | 1.4.5   | Lõi lịch + bát tự (SolarTime, LunarHour, EightChar, ChildLimit, DecadeFortune). "Bản nâng cấp của Lunar" | **trực tiếp**                    |
| **cantian-tymext** | 0.0.26  | Thần Sát (`getShen`) + **quan hệ trụ** (`calculateRelation`) + sinh khắc (`getWuxingRelation`)           | **trực tiếp**                    |
| **iztro**          | 2.5.8   | Tử Vi đẩu số 12 cung + tứ hóa + độ sáng sao + vận hạn                                                    | (import trực tiếp trong wrapper) |
| lunar-typescript   | 1.8.6   | (lịch/bát tự — qua tyme4ts)                                                                              | gián tiếp                        |
| lunar-lite         | 0.2.8   | (chuyển đổi âm/dương)                                                                                    | gián tiếp                        |

> Engine = thư viện npm (read-only, KHÔNG sửa — mất khi `pnpm install`). Logic chị sở hữu = **`bazi_wrapper.mjs`**.
> Clone máy mới: `cd web-dashboard && pnpm install` (có `pnpm-lock.yaml`).

---

## 3. Tool inventory

### 3.1 Server `bazi` — `bazi_wrapper.mjs` (7 tool)

| Tool                         | Input                                                                        | Output (field chính)                                                                                       | Engine call                                                          | Status                     |
| ---------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------- |
| `bazi__getBaziDetail`        | `solarDatetime`\|`lunarDatetime`, `gender`(0/1), `eightCharProviderSect`(=2) | 4 trụ + Thập Thần + Nạp âm + Tinh vận + Thai nguyên/Mệnh cung/Thân cung + **`神煞`** + **`关系`** + **`五行统计`** | tyme4ts + `getShen` + `calculateRelation` + tally                    | ✅ + nâng cấp 2026-06-02    |
| `bazi__getSolarTimes`        | `bazi` (vd `"乙卯 己丑 甲戌 己巳"`)                                                  | mảng ngày dương khả dĩ 1900-2050                                                                           | `EightChar.getSolarTimes`                                            | ✅                          |
| `bazi__getDaYun`             | `solarDatetime`, `gender`(0/1), `count`(=9), `targetYear`(optional)          | `八字` + `顺逆` + `起运` + `大运[]`(can chi + tuổi + năm + **`与命局关系`**) + **`流年`** (nếu có targetYear)             | `ChildLimit` + `DecadeFortune` + `appendRelation` + `SixtyCycleYear` | 🆕 2026-06-02 (+ vận hạn)  |
| `bazi__getChineseCalendar`   | `solarDatetime`(optional)                                                    | Hoàng lịch: 干支, 28 tú, Bành Tổ, 5 thần phương vị, 宜/忌, 冲煞                                                  | tyme4ts LunarDay                                                     | ✅                          |
| `tuvi__getChart`             | `solarDate`(YYYY-MM-DD), `hour`(0=Tý), `gender`(0/1)                         | 12 cung + chính/phụ tinh + độ sáng + tứ hóa + **Tuần/Triệt + Mệnh/Thân Chủ chuẩn VN**                      | iztro + override VN                                                  | ✅                          |
| `tuvi__getHoroscope`         | + `targetDate`, `targetHour`(optional)                                       | Đại hạn / Lưu niên / Lưu nguyệt / **Lưu nhật** / **Lưu thời** + lưu sao + mutagen                          | `computeHoroscope` (lib/engine/tuvi)                                 | ✅ +daily/hourly 2026-06-02 |
| `tuvi__getSanFangSiZheng` 🆕 | `branch` (địa chi Hán 子..亥)                                                  | Tam Phương Tứ Chính: Bản cung + Tam hợp (2) + Đối cung (xung chiếu)                                        | `getSanFangSiZheng` (lib/engine/tuvi)                                | 🆕 2026-06-02              |
| `charts__list`               | —                                                                            | List khách đã lưu (`web-dashboard/data/charts.json`)                                                       | fs đọc JSON local                                                    | ✅                          |

**Chi tiết field MỚI (sau nâng cấp):**
- **`关系`** = `calculateRelation(zhuArray)` → mỗi trụ trả `{天干:{冲,合}, 地支:{冲,害,破,暗合,合,刑,三合,三会,三刑,半合}}` + `拱`/`双合`/`双冲`/`伏吟`. **Đây là toàn bộ Hình-Xung-Phá-Hại-Hợp.**
- **`五行统计`** = đếm 4 thiên can + tàng can địa chi → `{木,火,土,金,水}`. Cơ sở luận **Dụng Thần** (không trùng Thập Thần như `getWuxingRelation` từng cặp).

### 3.2 Server `phongthuy` (Python) — 8 tool

| Tool                              | Dùng khi                                       |
| --------------------------------- | ---------------------------------------------- |
| `get_bat_trach_chart`             | Mệnh Quái + 8 hướng tốt/xấu (Đông/Tây Tứ Mệnh) |
| `get_cuu_cung_phi_tinh`           | Cửu cung phi tinh (Huyền Không)                |
| `get_hau_thien_bat_quai`          | Hậu thiên Bát Quái                             |
| `get_qi_men_dun_jia_components`   | Kỳ Môn Độn Giáp                                |
| `analyze_household_compatibility` | Hợp tuổi cả nhà                                |
| `lookup_am_trach`                 | Âm trạch (mộ phần)                             |
| `lookup_kham_du_layout`           | Khám dư (bố cục)                               |
| `lookup_loan_dau`                 | Loan đầu (hình thế)                            |

### 3.3 Server `timemap` (uvx) — 8 tool

| Tool                                       | Dùng khi                               |
| ------------------------------------------ | -------------------------------------- |
| `get_solar_term`                           | 24 tiết khí chính xác theo năm (DE421) |
| `get_daily_pillars` / `get_hourly_pillars` | Trụ ngày / trụ giờ                     |
| `get_day_quality`                          | Day Officer + 28 tú (chọn ngày)        |
| `get_daily_interactions`                   | Tương tác can chi trong ngày           |
| `get_luck_pillars`                         | Đại vận (engine timemap)               |
| `get_natal_chart`                          | BaZi 4 trụ                             |
| `lookup_hexagram`                          | Quẻ Kinh Dịch                          |

> ⚠️ **Trùng lặp có chủ đích:** cả `bazi` và `timemap` đều tính được 4 trụ + đại vận. `bazi` (tyme4ts) = output tiếng Trung chi tiết + Việt hóa Tử Vi; `timemap` = verify chéo Joey Yap + tiết khí DE421. Dùng `bazi` làm chính, `timemap` để đối chiếu.

---

## 3.5 LUẬN (interpretation) — nguồn ở đâu (audit 2026-06-02)

> **Phân biệt cốt lõi: TÍNH (engine, deterministic) ≠ LUẬN (diễn giải ý nghĩa).** Mọi tool §3.1-3.3 chỉ **TÍNH** (trả số/can chi/sao/quan hệ). Phần LUẬN hiện ở tầng UI web, KHÔNG ở engine/MCP. Bảng dưới nói rõ mỗi surface luận ở đâu:

| Surface (web Tử Vi)                        | Cột Luận — nguồn                                                     | Bản chất                                                                                   |
| ------------------------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Bình Giải Tổng Quan** (panel cạnh lá số) | `components/tuvi/TuViSections.js` → `InterpPanel` + dict `STAR_DESC` | **Rule-based template** (điền chỗ trống: cung + chính tinh + sát tinh + tứ hóa). KHÔNG AI. |
| Mô tả sao Đại Hạn                          | `components/tuvi/DaiVanTable.js` + `STAR_DESC` (SSOT)                | Dictionary cứng (câu 1)                                                                    |
| Mô tả sao Vận Hạn                          | `components/tuvi/HoroscopeSection.js`                                | Template + `STAR_DESC` (SSOT)                                                              |
| **"Phân Tích AI Tổng Quát"**               | field `ai_interpretation` (DB)                                       | **NHẬP TAY** — không auto-sinh. Rỗng = "Chưa có phân tích AI". Tên "AI" gây hiểu nhầm.     |
| Bát Tự (4 trụ, 关系, 五行, đại vận)            | engine (`lib/engine/bazi.js`)                                        | **CHỈ TÍNH — chưa có luận** (agent tự luận thủ công nếu cần)                               |
| (AI Opus chat)                             | `app/api/ai/phong-thuy-chat` (claude-opus)                           | Có endpoint nhưng **CHƯA nối** vào trang Tử Vi                                             |

> **SSOT mô tả sao**: `lib/utils/tuviDict.js` → `STAR_DESC` — nay **DERIVE TỪ CSDL 114 sao** `web-dashboard/data/tu-vi-dictionary/TuVi-114-Stars-Dictionary.json` (3D/5D/6D, update dần trong app; llm-wiki `raw/Tu-vi-dictionary` = symlink về đây cho agents). Derive Chinh_Tinh_14 + Luc_Sat_Tinh = 20 sao Hán-keyed (Phu_Tinh chưa có pinyin → chưa key). Update JSON → STAR_DESC tự đổi (chống drift). Trước đó (2026-06-02) gộp từ 3 bản hardcode trùng (TuViSections local + HoroscopeSection STAR_DESC_DV dead + tuviDict). Câu 1 = loại tinh (DaiVanTable cắt `split('.')[0]`), phần sau = keywords (InterpPanel full).
>
> **Tóm lại**: Tử Vi web hiện luận bằng **template + từ điển cứng**, KHÔNG phải AI. Muốn luận AI → nối `phong-thuy-chat` (Opus) sinh `ai_interpretation`.

---

## 4. Coverage map — đã dùng vs CHƯA dùng (audit 2026-06-02)

### cantian-tymext (28 hàm export)
| Đã dùng ✅                                | CHƯA dùng (tiềm năng nâng cấp)                                                           |
| ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| `getShen` (thần sát 4 trụ)               | `getShenFromDayun` / `getShenFromSizhu` — thần sát theo **Đại Vận** (gắn vào `getDaYun`) |
| `calculateRelation` (quan hệ 4 trụ gốc)  | `baziToMarkdown` / `getChineseCalendarMarkdown` — output markdown sẵn                    |
| `appendRelation` ✅ MỚI (đại vận/lưu niên vs mệnh gốc — trong `getDaYun`) | `buildBaziFromLunar` / `buildBaziFromSolar` — builder thay thế |

### tyme4ts
| Đã dùng ✅ | CHƯA dùng |
|-----------|-----------|
| SolarTime, LunarHour, EightChar, ChildLimit, DecadeFortune | `Fortune` — **lưu niên trong đại vận** (gắn vào `getDaYun`: vận từng năm) |
| `getExtraEarthBranches` (gián tiếp) | `SixtyCycle.getExtraEarthBranches()` — **Tuần Không (空亡) bát tự** chưa trích vào `getBaziDetail` |
| | `SixtyCycle.getTen()` — tuần (旬) |

### iztro (khai thác tốt ~85%)
| Đã dùng ✅                                                                                                                         | CHƯA dùng |
| --------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `.horoscope()` decadal/yearly/monthly + **daily/hourly** (Lưu nhật/Lưu thời ✅ 2026-06-02, qua `lib/engine/tuvi.computeHoroscope`) | —         |
| palaces + stars + brightness + mutagen + **三方四正** (`getSanFangSiZheng` ✅ 2026-06-02)                                              | —         |

---

## 5. Upgrade backlog (việc nên làm tiếp, ưu tiên giảm dần)

1. **Tuần Không bát tự** → thêm `空亡` vào mỗi trụ trong `getBaziDetail` qua `SixtyCycle.getExtraEarthBranches()` (native, đang tự tính tay cho Tử Vi). _Nhỏ, giá trị cao._
2. **Thần sát theo Đại Vận** → trong `getDaYun`, mỗi trụ đại vận gắn `getShenFromDayun`.
3. **Liệt kê 10 lưu niên trong 1 đại vận** → `getDaYun` dùng `Fortune` để xổ can chi từng năm (hiện đã có luận lưu niên đơn lẻ qua `targetYear` + `appendRelation`).
4. **Lưu nhật / lưu thời Tử Vi** → `getHoroscope` mở `daily`/`hourly` scope.
5. **Đồng nhất phái khởi vận** → cân nhắc `LunarSect2ChildLimitProvider` cho `getDaYun` để khớp phái Sect2 của bát tự (hiện dùng default).

✅ **Đã làm 2026-06-02:** wire `appendRelation` vào `getDaYun` (mỗi đại vận + lưu niên kèm quan hệ xung/hợp/hình/hại/phá với tứ trụ gốc) + input `targetYear` luận Lưu Niên.

---

## 6. Gotchas / Hard rules (ĐỌC TRƯỚC KHI SỬA)

| #   | Rule                                                                                               | Lý do                                                                                                                                     |
| --- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Timezone ép `Asia/Ho_Chi_Minh`** trước khi `SolarTime.fromYmdHms` (dòng ~59, 114, getDaYun)      | Server có thể chạy UTC → lệch trụ giờ. Tool mới PHẢI tái dùng pattern `toLocaleString('en-US',{timeZone})`                                |
| 2   | **`ChildLimit.getEndTime()` = giờ khởi vận**, KHÔNG phải `getStartTime()` (=giờ sinh)              | `ChildLimit` là giai đoạn TỪ sinh (start) ĐẾN khởi vận (end). Đã từng nhầm — test bắt được 2026-06-02                                     |
| 3   | **`calculateRelation` là aggregator** — 1 call bao trọn xung/hợp/hình/hại/phá/tam hợp/tam hội/củng | KHÔNG cần gọi tay từng `checkZhiXing/checkSanxing...`                                                                                     |
| 4   | **`getWuxingRelation` từng cặp ≈ trùng Thập Thần**                                                 | Dùng `五行统计` (đếm cân bằng) cho sinh khắc, không pairwise                                                                                  |
| 5   | **Tử Vi: Mệnh/Thân Chủ + Tuần/Triệt override chuẩn VN** (dòng 154-217)                             | iztro tính theo phái Đài Loan; bảng `MENH_CHU`/`THAN_CHU` + `trietMap` Việt hóa. KHÔNG xóa                                                |
| 6   | **`eightCharProviderSect=2`** (晚子时) mặc định                                                       | Khách sinh 23h-24h sẽ khác phái 1. Có chủ đích                                                                                            |
| 7   | **Restart MCP để áp code mới**                                                                     | Wrapper là process stdio dài hạn, KHÔNG hot-reload. Sửa xong phải restart server `bazi` (session mới / kill process)                      |
| 8   | **KHÔNG đóng băng số liệu phụ thuộc lá số vào doc**                                                | File `tu-vi-engine.md` cũ ghi cứng tứ hóa Đại Vận → sai khi đổi giờ sinh → đã XÓA 2026-06-02. Tứ hóa Đại Vận luôn gọi `getHoroscope` live |

---

## 7. Verification recipe (cách test khi sửa)

```js
// Chạy trong web-dashboard/ (node_modules resolve được)
// Lá số chuẩn để đối chiếu (Chủ Tướng): 1976-01-23, GIỜ MÃO (卯, 05:00-07:00), nam
//   Âm lịch: 23/12/1975  |  Bát tự: 乙卯 己丑 甲戌 丁卯
//   Tử Vi: Mệnh Tham Lang (戌/Tuất), Thân cư Vũ Khúc (辰/Thìn)
//   ⚠️ KHÔNG dùng giờ Tỵ/10:00 — đó là giả định sai cũ (cho ra Mệnh Vũ Tướng, lệch lá số)
```
1. **Round-trip:** `getBaziDetail` (giờ Mão) → lấy `八字` → `getSolarTimes` phải ra lại `1976-1-23` trong khung 05:00-07:00.
2. **Quan hệ:** `关系` phải có `卯-戌 hợp Hỏa` + `丑-戌 Hình` (giờ Mão có 2 trụ 卯 = năm + giờ).
3. **Đại Vận:** `getDaYun` nam Ất Mão → `顺逆 = 逆行`, chuỗi `戊子→丁亥→丙戌...` (lùi từ trụ tháng 己丑).
4. **node --check** chỉ chứng cú pháp — PHẢI chạy logic thật để chứng nghĩa.

---

## 8. Changelog

| Ngày             | Thay đổi                                                                                                                                                                                                                                                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-06-02       | Audit toàn bộ. Xóa import chết `calculateRelation` (→ dùng thật). `getBaziDetail` +`关系`+`五行统计`. Tool mới `bazi__getDaYun`. Fix `getStartTime`→`getEndTime`. Xóa `tu-vi-engine.md` (theo lệnh — LƯU Ý: phần "Mệnh Tham Lang Tuất" của doc đó thực ra ĐÚNG với giờ Mão; audit ban đầu đối chiếu nhầm bằng giờ Tỵ). |
| 2026-06-02 (sửa) | Sửa lá số verify: giờ thật = **Mão** (Mệnh Tham Lang Tuất), KHÔNG phải Tỵ (Mệnh Vũ Tướng) như giả định sai trước đó.                                                                                                                                                                                             |
| 2026-06-02 (+vận hạn) | Wire `appendRelation` vào `getDaYun`: mỗi đại vận + lưu niên kèm `与命局关系` (xung/hợp/hình/hại/phá với tứ trụ gốc). Thêm input `targetYear` → block `流年` luận Lưu Niên. Biến getDaYun từ "liệt kê" thành "luận vận hạn". |
| 2026-06-02 (web SSOT) | Tách `web-dashboard/lib/engine/bazi.js` SSOT (computeBaziDetail + computeDaYun). Wrapper + `api/bazi` + `api/dayun` (mới) cùng import. Web trang Tử Vi hiển thị 关系 + 五行 (BaziSectionFull) + Đại Vận Bát Tự (BatTuDaiVanTable). Hết drift agent↔web. Build xanh. |
| (trước)          | Wrapper v4.0.0: 6 tool, Việt hóa Tử Vi (Mệnh/Thân Chủ + Tuần/Triệt)                                                                                                                                                                                                                                              |
