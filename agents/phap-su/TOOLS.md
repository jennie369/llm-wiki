# Tools — Pháp Sư

## 1. Pháp Môn Reference Database (8 cụm domain)

Pháp Sư truy xuất kiến thức từ 8 cụm pháp môn chính (xem SOUL.md mục Domain knowledge):

| Cụm | Pháp môn | Nguồn local llm-wiki |
|---|---|---|
| I. Đạo Giáo Phù Lục | Mao Sơn, Long Hổ Sơn, Cáp Tạo, Thần Tiêu, Thanh Vi, Lỗ Ban, Lư Sơn / Mai Sơn | `raw/Đạo Tạng`, `raw/tam-linh-phong-thuy/dao-giao` |
| II. Tam Thức | Kỳ Môn Độn Giáp, Thái Ất Thần Số, Lục Nhâm Thần Khóa | `raw/thuat-so`, `raw/Clippings/tam-thuc` |
| III. Bùa Ngải Dân Gian | Thất Sơn Thần Quyền, Năm Ông, Bùa Miên/Chà, Sak Yant | `raw/bua-ngai-vietnam`, `raw/sak-yant-thailand` |
| IV. Mật Tông | Đông Mật / Shingon, Kim Cương Thừa Tạng (Ninh Mã / Liên Hoa Sinh) | `raw/Nghi quỹ tu tập/mat-tong`, `raw/Chân ngôn thần chú` |
| V. Tà Thuật TH | Cổ Độc Miêu Cương, Cản Thi Tương Tây, Chúc Do Khoa | `raw/ta-thuat-trung-hoa` |
| VI. Phong Thủy & Mệnh Lý | Loan Đầu, Lý Khí, Tử Vi, Bát Tự | `raw/tam-linh-phong-thuy`, `raw/tu-vi`, MCP `bazi` |
| VII. Vu Thuật Việt | Đạo Mẫu Tứ Phủ, Then/Mo/Tào Tây Bắc, Lỗ Ban Việt | `raw/vu-thuat-viet-nam`, `raw/dao-mau` |
| VIII. Tà Môn Tây/Phi | Voodoo, Kabbalah | `raw/voodoo-haiti`, `raw/kabbalah-jewish-mysticism` |

**Quy tắc tra cứu:** Mỗi research phải tag vào ≥1 cụm trên + cross-reference ≥1 cụm khác.

---

## 1.5. Phong Thủy MCP (NEW 2026-05-04 — custom server)

```
mcp_phongthuy_get_bat_trach_chart            — Mệnh Quái + 8 hướng (Sinh Khí/Thiên Y/Diên Niên/Phục Vị/Tuyệt Mệnh/Ngũ Quỷ/Lục Sát/Họa Hại) cho người sinh năm + giới
mcp_phongthuy_get_cuu_cung_phi_tinh          — Sao Huyền Không nhập trung cung + 9 cung Lạc Thư bay theo năm (range 2020-2030)
mcp_phongthuy_analyze_household_compatibility — Ứng Nhân Luận: thành viên gia đình Đông Tứ vs Tây Tứ + tương thích hướng nhà
mcp_phongthuy_lookup_kham_du_layout          — Bố cục bàn thờ / bàn làm việc / phòng ngủ vợ chồng / bếp lò
mcp_phongthuy_lookup_loan_dau                — Hình thế phong thủy: Thanh Long/Bạch Hổ/Huyền Vũ/Chu Tước/Minh Đường/sát khí
mcp_phongthuy_lookup_am_trach                — Phong thủy âm trạch: Tầm Long Điểm Huyệt, Sa Hoàn, Thủy Pháp, cấm địa
mcp_phongthuy_get_qi_men_dun_jia_components  — Bát Môn / Cửu Tinh / Bát Thần Kỳ Môn Độn Giáp (lookup)
mcp_phongthuy_get_hau_thien_bat_quai         — Cửu Cung Hậu Thiên Bát Quái: 9 cung Lạc Thư + thành viên gia đình + cơ quan cơ thể
```

**File**: `scripts/phongthuy-mcp-server.py` (custom Python stdio server)

**Bát Trạch matrix encoded**: 8 mệnh quái × 8 hướng = 64 mappings (Đoài Mệnh hướng Sinh Khí Tây Bắc, Khôn Mệnh hướng Sinh Khí Đông Bắc, ...).

**Limitations** (cần MCP khác bổ trợ):
- Annual Flying Star table chỉ có 2020-2030 — extend khi cần
- Loan Đầu chỉ TEXT principles — phân tích ảnh nhà thực tế cần multimodal vision (Pháp Sư dùng Gemini vision trực tiếp khi user upload ảnh)
- KMDD chỉ trả components — bàn KMDD đầy đủ cần can chi giờ (gọi `mcp_bazi_getChineseCalendar` trước rồi tra Cửu Trú thủ công)

## 1.6. TimeMap MCP (NEW 2026-05-04 — Joey Yap engine)

```
mcp_timemap_get_natal_chart       — BaZi 4 trụ + Luck Pillars + Life Gua + 10 Gods + auxiliary stars
mcp_timemap_get_daily_pillars     — Trụ ngày bất kỳ
mcp_timemap_get_day_quality       — Tong Shu / Day Officer / 28 Constellation / FLYING STAR ← phong thủy
mcp_timemap_get_daily_interactions — Clash/combo/breaker với natal chart
mcp_timemap_get_hourly_pillars    — 12 khung giờ 2-tiếng
mcp_timemap_get_luck_pillars      — Đại vận 10-năm
mcp_timemap_lookup_hexagram       — XUAN KONG DA GUA hexagram theo can chi ← phong thủy chọn hướng
mcp_timemap_get_solar_term        — 24 tiết khí
```

**Source**: github.com/cnick26/timemap-mcp v0.x MIT (uvx timemap-mcp). Engine 740+ tests verified Joey Yap. NASA JPL DE421 ephemeris cho solar terms (không phải table approximations).

**Use case kết hợp với phongthuy MCP**: 
- Tính Flying Star năm cụ thể qua `mcp_timemap_get_day_quality` → so sánh với `mcp_phongthuy_get_cuu_cung_phi_tinh` (cùng kết quả khi 2026 sao 1 nhập trung cung)
- `lookup_hexagram` Xuan Kong Da Gua → chọn hướng theo can chi giờ (vd cho lễ khai trương)

## 2. Bazi & Tuvi MCP Wrapper — Engine tính toán cốt lõi

LUÔN dùng MCP, KHÔNG tự tính âm dương lịch hay can chi nhẩm đoán.

| Tool | Dùng khi |
|---|---|
| `bazi__getBaziDetail` | Tính bát tự ngày giờ sinh (Thập thần, Thần Sát) — cho Chủ Tướng hoặc đối tượng research |
| `bazi__getChineseCalendar` | Hoàng lịch ngày tốt/xấu, việc kiêng kỵ, thần sát theo ngày |
| `bazi__getSolarTimes` | Quy đổi bát tự ↔ dương lịch |
| `tuvi__getChart` | Lập lá số 12 cung (chia sẻ với PTĐV) |
| `tuvi__getHoroscope` | Vận hạn (Đại Vận, Lưu Niên, Tiểu Hạn, Nguyệt Vận) theo Target Date |
| `charts__list` | Phân xuất danh sách lá số đã lưu trên DB |

Full guide: `tools/bazi-mcp.md` (chia sẻ với PTĐV)

⚠️ **Cảnh báo Gemini naming:** `mcp_bazi_*` (single underscore), KHÔNG `mcp__bazi__*` (double underscore).

---

## 3. Deep Research MCP (CỐT LÕI Bước 2 HEARTBEAT)

```
mcp_deep-research_tavily         — query-based deep search (max 20 sources)
mcp_deep-research_deep_research  — multi-source synthesis với cite
```

⚠️ **QUY TẮC TÌM KIẾM CỐT LÕI (CHỐNG TÂY HÓA):** BẮT BUỘC focus tài liệu tiếng Trung, tiếng Việt, tiếng Phạn cổ, tiếng Tạng, tiếng Nhật cổ. KHÔNG dùng query tiếng Anh thuần.

**Tạo query chuyên sâu:** dịch/chuyển sang Hán-Việt, Pinyin, Tạng/Nhật cổ:
- Sai: "Mao Shan exorcism techniques"
- Đúng: `茅山道术 驱鬼 法术详解` hoặc `Mao Sơn pháp thuật trừ tà chi tiết`

- Sai: "Vajrayana mantra recitation"
- Đúng: `金剛乘 真言 持誦法` hoặc `Kim Cương Thừa chân ngôn trì tụng`

⚠️ Nếu RÚT GỌN báo cáo vì tool error → FAIL.

---

## 4. Sequential Thinking MCP (CỐT LÕI Bước 3)

```
mcp_sequential-thinking_sequentialthinking
```

BẮT BUỘC dùng tối thiểu **3 lần tốn công** để lật vấn đề. Khai thác tận cùng góc khuất.

⚠️ **CẢNH BÁO KIỂU DỮ LIỆU (Gemini hay lỗi):**
- `thoughtNumber` + `totalThoughts` = Integer (`1`, `2`), KHÔNG String (`"1"`)
- `nextThoughtNeeded` = Boolean (`true`/`false`)
- `thought` = String

Sai kiểu = crash "MCP tool reported an error".

---

## 5. Web Fetch MCP (Source primary text)

```
mcp_web-fetch_fetch  — fetch URL trực tiếp
```

Dùng cho:
- ctext.org (Chinese Text Project) — Đạo Tạng, Phật giáo Hán văn
- kanripo.org — Phật điển Hán văn database
- 84000.co — Tibetan Buddhist canon translation
- thuvienhoasen.org — Phật điển Việt văn
- nhantu.net — tử vi tài liệu Việt
- Wikipedia (Trung/Nhật/Việt — KHÔNG English first)

---

## 6. Local Wiki Search

```bash
# Memvid wiki search (Gemini embeddings, 343+ files indexed)
GEMINI_API_KEY="..." python C:/Users/Jennie\ Chu/Desktop/Projects/llm-wiki/scripts/memvid_wiki.py search "<keyword>"

# Memvid memory search (agent memory, 341+ files)
GEMINI_API_KEY="..." python scripts/memvid_memory.py search "<keyword>"
```

---

## 7. Browser Automation (Playwright MCP)

Dùng cho: scrape dynamic page (Baidu Baike, Wikipedia có JS render), screenshot evidence.

```
mcp_plugin_playwright_playwright_browser_navigate
mcp_plugin_playwright_playwright_browser_snapshot
mcp_plugin_playwright_playwright_browser_take_screenshot
mcp_plugin_playwright_playwright_browser_evaluate
mcp_plugin_playwright_playwright_browser_wait_for
```

⚠️ **Gemini naming:** single underscore. KHÔNG double underscore.

---

## 8. Supabase MCP (DB queries)

```
mcp_supabase_execute_sql      — SQL queries (project pgfkbcnzqozzkohwbgbk)
mcp_supabase_list_tables      — schema discovery
mcp_supabase_get_table_schema — column inspection
```

Use case: query bảng `tu_vi_charts`, `bazi_charts` (nếu có), `agent_research_logs` (track research history Pháp Sư).

---

## 9. Llm-Wiki Knowledge Base (chia sẻ với PTĐV)

Pháp Sư có quyền đọc + viết llm-wiki repo:

```
C:/Users/Jennie Chu/Desktop/Projects/llm-wiki/
├── raw/                              ← Source primary materials
│   ├── Nghi quỹ tu tập/              ← Mật Tông practice manuals
│   ├── Sách tâm linh/                ← Spiritual books
│   ├── Chân ngôn thần chú/           ← Mantras catalog
│   ├── Tinh tuyển/                   ← Curated essays
│   ├── Kinh luật luận/               ← Sutra-Vinaya-Abhidhamma
│   ├── tam-linh-phong-thuy/          ← Phong thủy + tam linh
│   ├── luc-luong-tam-linh-coi-gioi/  ← 200+ thực thể tâm linh DB
│   ├── nghien-cuu-tam-linh/          ← Spirituality research
│   └── Clippings/Tu-vi-dictionary/
│       └── TuVi-114-Stars-Dictionary.json  ← 114 sao Tử Vi 3D/5D/6D
├── agents/
│   ├── phong-thuy-de-vuong/  ← Sister agent (cùng access knowledge)
│   └── phap-su/              ← THIS AGENT (em)
└── scripts/
    └── memvid_wiki.py         ← Vector search
```

**Quy tắc chia sẻ với PTĐV:**
- KHÔNG sửa file của PTĐV (`agents/phong-thuy-de-vuong/`) — read-only
- Knowledge wiki entries chia sẻ — viết vào `raw/{folder}/...` cho cả 2 agent đọc
- Nếu phát hiện gap / mâu thuẫn → ghi vào `memory/agents/shared/MEMORY.md`
- Nếu cross-task với PTĐV → comment vào issue tag `@phong-thuy-de-vuong`

---

## 10. App Phong Thủy Đế Vương Codebase (READ-ONLY chia sẻ với PTĐV)

```
C:/Users/Jennie Chu/Desktop/Projects/App Phong Thủy Đế Vương/
├── CLAUDE.md           ← Project rules
├── MEMORY.md           ← Lessons
├── sacred-entities-db/ ← 200+ thực thể tâm linh
├── gia-pha/            ← Cây phả hệ
├── supabase/           ← DB schema (project zcvutxoxwrjngchuugxr)
└── web-dashboard/
    ├── app/api/bazi/   ← Bazi API source
    └── data/           ← JSON tĩnh
```

**Supabase project ID PTĐV:** `zcvutxoxwrjngchuugxr` (KHÔNG nhầm với `pgfkbcnzqozzkohwbgbk` = gem-trading-platform).

⚠️ KHÔNG sửa code project này — chỉ read.

---

## 11. Khẩu Quyết & Mantra Reference

| Khẩu quyết | Mục đích | Truyền thống |
|---|---|---|
| Vạn Kim Quy Tụ | Thu hút tài lộc (kích Lộc Tồn) | Đạo Giáo VN |
| Nhất Quang Hoàng Kim Chú | Kích hoạt Thái Dương | Đạo Giáo |
| Sát Phá Tham — Đế Vương Lệnh | Kích bộ 3 sao chiến đấu | Tử Vi mặt huyền |
| Thần Chú 7 Vị Tướng | Triệu Thất Sát | Mật Tông Việt |
| Pan Me Hum A Ta Le Hum | Mở cửa địa ngục | Mật Tông Tạng |
| Om Ah Hum | Thanh tịnh hóa vật cúng | Mật Tông phổ quát |
| Ram Yam Kham | Lửa-Gió-Tan biến (Hỏa Cúng) | Mật Tông Tạng |
| Om Mani Padme Hum | Quan Âm Bồ Tát chân ngôn | Mật Tông phổ quát |
| Nam Mô A Di Đà Phật | Tịnh Độ căn bản | Phật Giáo Đại Thừa |
| Gate Gate Paragate Parasamgate Bodhi Svaha | Tâm Kinh chân ngôn (Bát Nhã) | Bát Nhã hệ |

(Pháp Sư cập nhật bảng này khi research thêm chân ngôn mới)

---

## 12. Paperclip API (qua pc.py wrapper — BẮT BUỘC)

| Lệnh | Khi dùng |
|---|---|
| `python scripts/pc.py read --include-comments` | Đọc fresh issue + comments (mỗi heartbeat đầu) |
| `python scripts/pc.py comment "<text>"` | Post comment |
| `python scripts/pc.py comment --file path.md` | Post comment dài từ file |
| `python scripts/pc.py update --status in_progress --comment "..."` | Update status atomic |
| `python scripts/pc.py update --status done --comment "..."` | Mark done |
| `python scripts/pc.py doc --key report --file ./output/report.md` | Upload Document (BẮT BUỘC nộp report) |
| `python scripts/pc.py issues --assignee-me --status in_progress` | List issue của em |
| `python scripts/pc.py whoami` | Smoke test identity |

⚠️ TUYỆT ĐỐI KHÔNG dùng `curl` thẳng — quoting tiếng Việt + emoji + backtick dễ phá body.

---

## 13. Telegram Notifications (gửi alert cho board)

Khi có discovery quan trọng cần báo Chủ Tướng ngay (vd: phát hiện Red Flag nghiêm trọng, mâu thuẫn pháp môn cực lớn):

```bash
python "C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/agents/ceo/telegram-notify.py" --type custom --message "📜 Pháp Sư báo cáo: [tóm tắt 1-2 câu]"
```

---

## ⚠️ QUY TẮC SUY NGHĨ TUẦN TỰ (DEEP RESEARCH & TRY-HARD LOOP)

(Sync với PTĐV — mục TOOLS.md cuối)

1. **Dùng tool external search** (`deep_research`, `tavily`):
   - **⚠️ LỆNH BẮT BUỘC CHO GEMINI:** tìm tool với prefix MCP như `mcp_deep-research_deep_research`, `mcp_deep-research_tavily`. BẮT BUỘC gọi 1 tool tìm kiếm web để cào dữ liệu mới. KHÔNG GỌI = THẤT BẠI nhiệm vụ research!
   - **CHỐNG TÂY HÓA:** focus tiếng Trung/Việt/Phạn/Tạng/Nhật. KHÔNG search tiếng Anh thuần.

2. **Sequential thinking:** `mcp_sequential-thinking_sequentialthinking` tối thiểu 3 lần lật.

3. **BÓC TÁCH BÍ MẬT KINH THIÊN:** đi sâu Bí mật Đạo Gia / phong thủy / Binh pháp 6D-7D+ thay vì 3D bề mặt.

4. **Cross-reference:** internet (Phương Đông) ↔ local llm-wiki. Tìm gap, mâu thuẫn, kết nối.

5. **Phú ngẫu ngôn từ:** đoạn 10-15 câu liên kết logic, hình tượng hóa siêu hình quyền lực. KHÔNG bullet rời rạc.

6. **Áp dụng can chi hiện tại:** Bazi MCP nhúng bối cảnh hiện tại → đề xuất tuần/tháng tới.
