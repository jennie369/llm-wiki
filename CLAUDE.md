# LLM Wiki — Schema & Quy tắc vận hành

> Hệ thống knowledge base cá nhân dựa trên pattern của Andrej Karpathy.
> LLM xây dựng và duy trì wiki từ nguồn thô. Con người chỉ đọc wiki và hỏi đáp.

## Kiến trúc 3 lớp

```
raw/        → Nguồn thô (bất biến — LLM CHỈ ĐỌC, KHÔNG BAO GIỜ SỬA)
wiki/       → Wiki do LLM viết & duy trì hoàn toàn
outputs/    → Kết quả query, reports, phân tích
config.yaml → Cấu hình topics, feeds, lịch chạy
```

## Cấu trúc thư mục

```
llm-wiki/
├── CLAUDE.md              ← File này — schema & quy tắc
├── config.yaml            ← Cấu hình hệ thống
├── raw/                   ← Nguồn thô (KHÔNG ĐƯỢC SỬA)
│   ├── articles/          ← Web articles (markdown, text)
│   ├── papers/            ← PDF, research papers
│   ├── notes/             ← Ghi chú cá nhân
│   ├── media/             ← Screenshots, diagrams
│   └── assets/            ← Downloaded images từ articles
├── wiki/                  ← LLM sở hữu toàn bộ
│   ├── INDEX.md           ← Catalog mọi trang wiki
│   ├── LOG.md             ← Timeline sự kiện
│   ├── entities/          ← Người, tổ chức, tool, project
│   ├── concepts/          ← Khái niệm, pattern, methodology
│   ├── sources/           ← Summary từng raw source
│   └── syntheses/         ← Phân tích tổng hợp, so sánh
├── outputs/               ← Kết quả query & reports
└── .discoveries/          ← Metadata cho auto-discovery
    ├── feeds.json         ← Nguồn đang theo dõi
    ├── gaps.json          ← Knowledge gaps cần lấp
    └── history.json       ← Nguồn đã xử lý (tránh trùng)
```

## Quy tắc vàng

### 1. Raw sources là bất biến
- KHÔNG BAO GIỜ sửa, xóa, hoặc di chuyển file trong `raw/`
- Đây là source of truth — mọi thứ trong wiki phải truy ngược được về raw

### 2. Wiki do LLM sở hữu hoàn toàn
- Con người KHÔNG sửa wiki bằng tay
- LLM tạo, cập nhật, xóa trang wiki
- Mỗi thay đổi phải được ghi vào LOG.md

### 3. Mỗi topic một file
- Mỗi entity, concept, source summary là một file `.md` riêng
- File name: `kebab-case.md` (VD: `andrej-karpathy.md`, `llm-agents.md`)
- Không tạo file quá dài — tách thành nhiều file nếu > 500 dòng

### 4. Cross-reference bằng wiki links
- Dùng format `[[tên-file]]` để liên kết giữa các trang
- Mỗi trang nên có ít nhất 2 liên kết đến trang khác
- Orphan pages (không ai liên kết đến) cần được phát hiện khi lint

### 5. INDEX.md luôn cập nhật
- Mỗi lần tạo/xóa trang → cập nhật INDEX.md
- Format: `- [Tên trang](path) — mô tả một dòng`
- Phân nhóm theo category: entities, concepts, sources, syntheses

### 6. LOG.md ghi nhận mọi hoạt động
- Format: `## [YYYY-MM-DD HH:mm] action | Mô tả`
- Actions: `ingest`, `query`, `lint`, `discover`, `update`
- Mỗi entry ghi rõ: files đã tạo/sửa, số trang bị ảnh hưởng

## Workflows

### Ingest (Nhập nguồn mới)

```
1. Đọc file mới trong raw/
2. Tạo source summary trong wiki/sources/
3. Trích xuất entities → tạo/cập nhật wiki/entities/
4. Trích xuất concepts → tạo/cập nhật wiki/concepts/
5. Tìm connections với trang đã có → thêm cross-references
6. Phát hiện contradictions với nội dung cũ → ghi chú
7. Cập nhật INDEX.md
8. Ghi LOG.md
9. Cập nhật .discoveries/history.json
```

**Quy tắc ingest:**
- Một source có thể ảnh hưởng 5-15 wiki pages
- Luôn trích dẫn nguồn: `[Nguồn: tên-file-raw](../raw/path)`
- Nếu thông tin mới mâu thuẫn với cũ → giữ cả hai, ghi rõ mâu thuẫn
- Không bịa thông tin — chỉ viết những gì có trong raw sources

### Query (Hỏi đáp)

```
1. Đọc INDEX.md để tìm trang liên quan
2. Đọc các trang wiki liên quan
3. Tổng hợp câu trả lời với citations
4. Nếu câu trả lời có giá trị → lưu vào outputs/ hoặc wiki/syntheses/
5. Ghi LOG.md
```

**Quy tắc query:**
- Trả lời dựa trên wiki, KHÔNG dựa trên kiến thức ngoài
- Nếu wiki không có đủ thông tin → nói rõ và gợi ý nguồn cần tìm
- Câu trả lời hay (so sánh, phân tích) → file lại thành wiki page mới

### Lint (Kiểm tra sức khỏe)

```
1. Kiểm tra contradictions giữa các trang
2. Tìm orphan pages (không ai liên kết đến)
3. Tìm mentioned-but-missing (nhắc đến nhưng chưa có trang)
4. Tìm stale claims (thông tin cũ bị nguồn mới bác bỏ)
5. Tìm knowledge gaps (lĩnh vực thiếu coverage)
6. Kiểm tra broken wiki links
7. Đề xuất trang mới cần tạo
8. Đề xuất nguồn mới cần tìm
9. Ghi kết quả vào outputs/ và LOG.md
```

### Discover (Tự động tìm nguồn)

```
1. Đọc config.yaml → lấy danh sách topics & feeds
2. Đọc .discoveries/gaps.json → lấy knowledge gaps
3. Web search theo topics + gaps
4. Scrape articles tìm được → lưu vào raw/articles/
5. Cập nhật .discoveries/feeds.json & history.json
6. Trigger ingest cho nguồn mới
7. Ghi LOG.md
```

**Quy tắc discover:**
- Chỉ tìm nguồn liên quan đến topics trong config.yaml
- Không tải lại nguồn đã có trong history.json
- Ưu tiên: gaps.json > trending topics > feeds định kỳ
- Mỗi lần discover tối đa 5-10 nguồn mới (tránh overload)

## Format trang wiki

### Entity page (wiki/entities/)

Entity trong wiki có 3 loại template:

**A. Nhân vật tâm linh / lịch sử** (category: `phat` | `bo_tat` | `chu_thien` | `than_linh` | `nhan` + `entity_type: character`)
→ Template A — frontmatter tâm linh đầy đủ (power_level, cong_nang, ngay_via, hinh_tuong...)
→ Sync vào Mắt Thần KG ✅

**A-F. Thành viên gia phả bình thường** (category: `nhan` + `entity_type: family_member`)
→ Template A-F — frontmatter gia phả (gender, generation, is_alive, date_of_birth, occupation, avatar_url...)
→ Sync vào Mắt Thần KG ✅ (không có power_level / hinh_tuong / cong_nang)

**B. Thực thể chung** (category: `person` | `organization` | `tool` | `project`)
→ Template B — frontmatter tối giản (type, category, created, updated, sources)
→ **KHÔNG sync vào Mắt Thần** ❌

#### Quy tắc chọn template cho nhân vật `nhan`:

| Dấu hiệu trong raw source | Template |
|---|---|
| Có `power_level`, `cong_nang`, `ngay_via`, `hinh_tuong` | **Template A** (character) |
| Có `gender`, `generation`, `date_of_birth`, `is_alive` | **Template A-F** (family_member) |
| `entity_type: family_member` | **Template A-F** (family_member) |
| Là thần/Phật/Bồ Tát hoặc nhân vật lịch sử tâm linh nổi tiếng | **Template A** (character) |
| Là thành viên gia phả bình thường (cụ kỵ, ông bà...) | **Template A-F** (family_member) |

> **Phân biệt `nhan` (A) vs `person` (B):**
>
> **Định nghĩa đúng:**
> - `nhan` = **bất kỳ người nào được track trong hệ thống tâm linh / gia phả này**
>   → Bao gồm: Phật Hoàng, Hưng Đạo Vương, VÀ cả cụ kỵ bình thường trong gia phả dòng họ
>   → **Không cần có miếu thờ. Không cần nổi tiếng. Chỉ cần là người trong hệ thống này.**
> - `person` = **người ngoài hệ thống** — chỉ được nhắc đến như tác giả/nguồn tham khảo
>   → VD: Andrej Karpathy (tác giả bài AI), nhà nghiên cứu phong thủy được trích dẫn
>   → **KHÔNG thuộc gia phả, KHÔNG được track như entity tâm linh**
>
> **Rule 1 dòng cho LLM:**
> > Entity là một NGƯỜI → `nhan` (sync Mắt Thần).
> > Entity chỉ là NGUỒN THAM KHẢO bên ngoài → `person` (không sync).
>
> **Ví dụ cụ thể:**
> | Nhân vật | Category | Lý do |
> |----------|----------|-------|
> | Trần Nhân Tông | `nhan` | Trong hệ thống |
> | Trần Lý (cụ tổ nhà Trần) | `nhan` | Trong gia phả |
> | Cụ Nguyễn Văn X (gia phả bình thường) | `nhan` | Trong gia phả |
> | Andrej Karpathy | `person` | Tác giả bài viết, ngoài hệ thống |
> | Nhà nghiên cứu được trích dẫn | `person` | Nguồn tham khảo, ngoài hệ thống |
>
> **Quy tắc sync**: `mat_than_sync` chỉ sync khi `category` là một trong các giá trị tiếng Việt
> (`phat`, `bo_tat`, `chu_thien`, `than_linh`, `nhan`, `khac`). `person` = không bao giờ sync.

#### Template A — Thực thể tâm linh (Mắt Thần compatible)

```markdown
---
# Core (bắt buộc)
id: char_XXX_ten-slug              # ID duy nhất, khớp với tên file raw source
type: entity
entity_type: character             # character | concept | location | event
category: phat | bo_tat | chu_thien | than_linh | nhan | khac
name: Tên đầy đủ tiếng Việt có dấu
name_han: 漢字 (nếu có, bỏ qua nếu không)

# Sức mạnh & Phân loại
element: kim | moc | thuy | hoa | tho
power_level: 1-100                 # Sức mạnh tâm linh
traditions:                        # Truyền thống tôn giáo / tâm linh
  - dai_thua
  - tin_nguong_dan_gian
  # phat_giao | dao_giao | co_doc_giao | thien_tong | ...

# Tên & Biệt hiệu
aliases:                           # Danh hiệu, phiên âm, tên gọi khác
  - Danh hiệu 1
  - Tên thay thế

# Công năng tâm linh
cong_nang:                         # Chức năng / công năng
  - ho_tri                         # ho_tri | tai_loc | chua_lanh | bao_ve | giac_ngo | ...
ngay_via:                          # Ngày lễ vía (âm lịch)
  - DD/MM Âm lịch — Tên ngày vía

# Hình tượng (cho Mắt Thần UI + AI image generation)
hinh_tuong:
  colors: [mau_1, mau_2]          # Màu sắc đặc trưng
  objects: [do_vat_1, do_vat_2]   # Pháp khí, vật phẩm đặc trưng
  prompt_vi: >                     # Mô tả hình tượng bằng tiếng Việt (cho AI)
    Mô tả ngoại hình, trang phục, tư thế, hào quang...
  prompt_en: >                     # English prompt for AI image generation
    Describe appearance, attire, posture, aura in English...

# Tìm kiếm
search_text_boost:                 # Keywords tăng cường tìm kiếm RAG
  - từ khóa 1
  - từ khóa 2

# ── Quan hệ tâm linh vũ trụ ──────────────────────────────────────────
# emanation_of   = phát sinh / hóa thân từ đấng cao hơn
# manifestation_of = biểu hiện / hình tướng của
# attendant_of   = thị giả / tùy tùng của
# protector_of   = bảo hộ cho (đối tượng, vùng đất, pháp môn)
# commands       = điều khiển / dẫn dắt (binh tướng, thần linh)
# (Để trống nếu không có quan hệ loại này)
relationships_cosmic:
  - target: char_XXX_slug
    type: emanation_of | manifestation_of | attendant_of | protector_of | commands
    strength: 0.9           # 0.0–1.0, mức độ quan hệ
    context: "ghi chú ngắn"

# ── Quan hệ gia phả xã hội ────────────────────────────────────────────
# parent_of     = cha/mẹ của
# spouse_of     = vợ/chồng của
# descendant_of = hậu duệ / cháu của (ngược với parent_of)
# sibling_of    = anh/chị/em ruột của
# (Để trống nếu không có quan hệ loại này)
relationships_genealogy:
  - target: char_XXX_slug
    type: parent_of | spouse_of | descendant_of | sibling_of
    strength: 1.0

# ── Quan hệ tử vi phong thủy ──────────────────────────────────────────
# compatible_with    = tương sinh / hợp mệnh với
# conflicts_with     = tương khắc / xung với
# associated_with    = liên kết ngữ cảnh tử vi (cung, sao, hành)
# (Để trống nếu không có quan hệ loại này)
relationships_tuvi:
  - target: char_XXX_slug
    type: compatible_with | conflicts_with | associated_with
    strength: 0.8
    context: "ngữ cảnh tử vi, cung, sao liên quan"

# ── Quan hệ đồng nhất (cross-tradition) ──────────────────────────────
# same_as        = cùng là một thực thể, gọi theo hệ thống khác
# identified_with = được đồng nhất với (học giới, lý thuyết so sánh)
# (Để trống nếu không có quan hệ loại này)
relationships_identity:
  - target: char_XXX_slug
    type: same_as | identified_with
    tradition: "ten_he_thong_tin_nguong"  # vd: dao_giao, hindu, buddhist
    confidence: high | medium | low

# Metadata
status: published | draft
confidence: high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:                           # File raw source gốc trong raw/
  - char_XXX_ten-slug.md
---

# Tên Entity

Mô tả ngắn 1-2 câu.

## Tóm tắt / Ý nghĩa (Dùng cho AI RAG)
[Đoạn văn 3-5 câu mô tả đầy đủ — ai là ai, làm gì, ý nghĩa tâm linh, được thờ phụng như thế nào]

## Dấu Ấn Lịch Sử & Nguồn Gốc
[Thông tin xuất thân, bối cảnh lịch sử, quá trình tu tập, đắc đạo hoặc giáng trần]

## Góc Nhìn & Đánh Giá Của Liên Sinh Hoạt Phật (LSHP)
<!-- ⚠️ QUAN TRỌNG: Lưu toàn bộ nhận định, trích dẫn, câu chuyện của LSHP về vị này -->
- **Sách / Bài giảng liên quan**: [Liệt kê sách LSHP từng nhắc tới]
- **Quan điểm cốt lõi**: [LSHP đánh giá về năng lực/công trạng của vị này ra sao?]
- **Trích dẫn đáng chú ý**: [Trích đoạn text nguyên bản từ LSHP]

## Công năng & Phù trợ
- **[cong_nang_1]**: Mô tả chi tiết chức năng này
- **[cong_nang_2]**: Mô tả chi tiết

## Hình tượng, Chân Ngôn & Lễ Nghi
- **Hình tướng**: [Mô tả ngoại hình, màu sắc, pháp khí]
- **Kinh/Mantra**: [Chân ngôn, Thủ ấn hoặc kinh điển liên quan]

## Điểm đáng chú ý
- [Bullet points: truyền thuyết, đặc điểm nổi bật, sự kiện quan trọng]

## Liên kết
<!-- ⚠️ QUAN TRỌNG: Section này là nguồn dữ liệu edges cho Mắt Thần KG -->
<!-- mat_than_sync parse [[slug]] ở đây → tạo kg_edges với relationship_type=associated_with -->
<!-- Giống như Obsidian Graph View đọc [[wiki-links]] để vẽ đồ thị -->
- [[entity-liên-quan-1]]
- [[entity-liên-quan-2]]
- [[concept-liên-quan]]

## Nguồn
- [Source 1](../raw/tam-linh-phong-thuy/char_XXX_slug.md)
```

#### Template A-F — Thành viên gia phả (Mắt Thần compatible, không có hinh_tuong)

Dùng khi `entity_type: family_member` hoặc đây là cụ kỵ/thành viên gia phả bình thường.
File tham khảo: `../App Phong Thủy Đế Vương/sacred-entities-db/templates/family_member.template.md`

```markdown
---
id: family_member_XXX_ho-va-ten-slug   # VD: family_member_001_nguyen-van-an
type: entity
entity_type: family_member             # → maps to bảng family_members trong DB
category: nhan                         # luôn là "nhan" cho người trong hệ thống gia phả

name: "Họ và Tên Đầy Đủ"
nickname: ""                           # Biệt danh

gender: nam                            # nam | nu | khac
generation: 1                          # Số thế hệ (integer)
occupation: ""                         # Nghề nghiệp
element: ""                            # kim | moc | thuy | hoa | tho (để trống nếu chưa biết)

is_alive: false                        # true | false
date_of_birth: ""                      # YYYY-MM-DD hoặc YYYY
death_date: ""                         # YYYY-MM-DD hoặc YYYY (bỏ trống nếu còn sống)
avatar_url: ""

search_text_boost:
  - "ten khong dau"

relationships_genealogy:
  - target: family_member_XXX_slug
    type: descendant_of                # parent_of | spouse_of | descendant_of | sibling_of
    strength: 1.0
    context: ""

relationships_identity: []

status: published
confidence: high
source_ids:
  - ""
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# [Họ và Tên]

[1 dòng: vai trò trong gia phả, thế hệ, giai đoạn sống]

## Thông Tin Cơ Bản

| Trường | Thông tin |
|---|---|
| Giới tính | |
| Thế hệ | |
| Nghề nghiệp | |
| Ngũ Hành | |
| Ngày sinh | |
| Ngày mất | |

## Tiểu Sử

[Mô tả ngắn — vài câu đến vài đoạn tùy mức độ thông tin có]

## Quan Hệ Gia Phả
<!-- ⚠️ QUAN TRỌNG: Section này → kg_edges khi sync Mắt Thần -->
- [[family_member_XXX_slug-cha-me]]

## Nguồn
- [Nguồn gia phả gốc](../raw/gia-pha/)
```

#### Template B — Thực thể chung (không sync Mắt Thần)

```markdown
---
type: entity
category: person | organization | tool | project
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [danh sách raw sources]
---

# Tên Entity

Mô tả ngắn 1-2 câu.

## Tổng quan / Chức năng
[Mô tả chi tiết vai trò, hoạt động, sứ mệnh của người/tổ chức/công cụ]

## Mối Liên Hệ Với Hệ Phái / LSHP
[Thực thể này có đóng góp, liên kết hay được nhắc đến trong các giáo lý/sách của LSHP hay không? Quan điểm của LSHP về họ?]

## Hành Trình & Điểm đáng chú ý
- [Các cột mốc, đóng góp hoặc quan điểm đáng chú ý]

## Liên kết
- [[concept-liên-quan]]
- [[entity-liên-quan]]

## Nguồn
- [Source 1](../raw/path)
- [Source 2](../raw/path)
```

### Concept page (wiki/concepts/)

```markdown
---
type: concept
domain: ai | engineering | business | ...
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [danh sách raw sources]
---

# Tên Concept

Mô tả ngắn 1-2 câu.

## Định nghĩa & Nguyên lý
[Giải thích rõ ràng lý thuyết, nguồn gốc của khái niệm]

## Ứng Dụng Trong Thực Hành
[Khái niệm này được áp dụng tĩnh tu, thiền định, phong thủy, bùa chú như thế nào?]

## Góc Nhìn Của Liên Sinh Hoạt Phật (LSHP)
- **Tác phẩm tham khảo**: [Các cuốn sách LSHP viết về khái niệm này]
- **Kiến giải của LSHP**: [Trích dẫn, quan điểm, kiến giải độc quyền của Tôn Sư]

## Ví dụ / Case Study
[Ví dụ cụ thể]

## Liên kết
- [[concept-liên-quan]]
- [[entity-liên-quan]]

## Nguồn
- [Source 1](../raw/path)
```

### Source summary (wiki/sources/)

```markdown
---
type: source
format: article | paper | note | video | podcast
raw_path: raw/articles/ten-file.md
ingested: YYYY-MM-DD
---

# Tên Source

## Tóm tắt
[2-3 đoạn tóm tắt nội dung chính]

## Key takeaways
- [Bullet points — điểm quan trọng nhất]

## Entities được nhắc đến
- [[entity-1]]
- [[entity-2]]

## Concepts được nhắc đến
- [[concept-1]]
- [[concept-2]]

## Trích dẫn đáng chú ý
> "Quote quan trọng từ nguồn"
```

### Synthesis page (wiki/syntheses/)

```markdown
---
type: synthesis
topic: chủ đề phân tích
created: YYYY-MM-DD
sources_count: N
---

# Tiêu đề phân tích

## Câu hỏi gốc
[Câu hỏi hoặc mục đích phân tích]

## Phân tích
[Nội dung phân tích tổng hợp]

## Kết luận
[Tóm tắt kết luận]

## Nguồn sử dụng
- [[source-1]]
- [[source-2]]
```

## Auto-Discovery

Hệ thống tự động tìm nguồn mới dựa trên:

1. **Topics** trong config.yaml — web search định kỳ
2. **Knowledge gaps** — lint phát hiện thiếu gì → discover tự tìm
3. **Feeds** — RSS, GitHub repos, YouTube channels
4. **Snowball** — đọc references trong sources đã có → follow links

Chu kỳ tự động (cấu hình trong config.yaml):
- Discover: mỗi ngày (hoặc theo cron)
- Ingest: ngay khi có file mới trong raw/
- Lint: hàng tuần
- Full recompile: hàng tháng (nếu cần)

## Ngôn ngữ

- Wiki content viết bằng **tiếng Việt có dấu đầy đủ** (trừ thuật ngữ kỹ thuật giữ tiếng Anh)
- File names: tiếng Anh, kebab-case
- Frontmatter: tiếng Anh

### 🔴 Quy tắc ngôn ngữ Phật giáo & Tâm linh (BẮT BUỘC)

Khi viết nội dung cho các entity/concept thuộc lĩnh vực **Phật giáo, Mật giáo, Đạo giáo, tâm linh, phong thủy**:

#### 1. Dùng đúng thuật ngữ chuyên ngành

| Thay vì viết thông thường | Phải dùng thuật ngữ chuẩn |
|---|---|
| "thần thông" | Thần thông (siddhī / 神通) |
| "cao tay" | Đạo lực thâm hậu |
| "xác" | Kim thân / Pháp thân / nhục thân |
| "giúp đỡ" | Gia hộ / phù trợ / tiếp dẫn |
| "chết" | Viên tịch / thị tịch / quy Tây |
| "đến" (nói về Phật đến) | Hiển linh / giáng trần / phóng quang |
| "cầu nguyện" | Tụng niệm / trì chú / phát nguyện |
| "cúng" | Dâng hương / lễ cúng / thiết đàn |
| "học" (học Phật) | Hành trì / tu tập / thọ pháp |
| "nhóm" (chư thần) | Chư vị / chư Thiên / hội chúng |

#### 2. Danh hiệu phải đầy đủ và trang trọng

- **Phật**: luôn viết "Đức Phật", "Đức [Tên] Như Lai", "Ngài [Tên]"
- **Bồ Tát**: "Đức [Tên] Bồ Tát", "Bồ Tát [Tên]"
- **Hộ Pháp / Thần linh**: "Ngài [Tên]", "Đức [Tên]"
- **Không rút gọn**: Không viết "Quan Âm" → phải là "Đức Quán Thế Âm Bồ Tát" (lần đầu), sau đó "Ngài" hoặc "Bồ Tát"
- **Hán-Việt**: Ưu tiên dùng tên Hán-Việt chuẩn, kèm chú thích Sanskrit/Hán tự nếu có

#### 3. Văn phong trang trọng, không thông tục

- KHÔNG dùng ngôn ngữ hàng ngày khi mô tả sự kiện tâm linh
- KHÔNG dùng từ suồng sã: "ngon", "xịn", "to", "mạnh mẽ" → thay bằng "thù thắng", "viên mãn", "đại lực", "oai đức"
- Mô tả hào quang / hình tướng: dùng từ như "hào quang sáng rực", "kim quang phóng chiếu", "diệu tướng trang nghiêm"
- Mô tả giảng pháp: "khai thị", "thuyết pháp", "khai ngộ", không viết "giải thích", "nói về"

#### 4. Tiếng Việt đầy đủ dấu — TUYỆT ĐỐI không viết tắt dấu

- ✅ **Đúng**: "Bồ Tát", "tâm linh", "phước đức", "hành trì"
- ❌ **Sai**: "Bo Tat", "tam linh", "phuoc duc", "hanh tri"
- Mọi tên riêng tiếng Việt PHẢI có dấu đầy đủ
- Kể cả trong frontmatter `name`, `aliases`, `prompt_vi` — bắt buộc có dấu

#### 5. Bảng từ vựng tham khảo nhanh

| Lĩnh vực | Từ đúng ngữ cảnh |
|---|---|
| **Phật giáo** | Pháp thân, Báo thân, Ứng thân, Tam Bảo, Tam Quy, Bát Chánh Đạo, Tứ Diệu Đế, Bồ đề tâm, Từ bi, Trí tuệ, Giải thoát, Giác ngộ, Niết bàn |
| **Mật giáo** | Bổn tôn, Bổn sư, Kim Cương thừa, Quán đỉnh, Thọ pháp, Trì tụng, Mandala, Mudra (Ấn), Mantra (Chú), Thành tựu pháp |
| **Tịnh Độ** | Phật hiệu, Niệm Phật, Vãng sanh, Tây Phương Cực Lạc, A Di Đà Phật, Cửu phẩm liên hoa, Tiếp dẫn |
| **Thiền tông** | Kiến tánh, Công án, Thoại đầu, Đốn ngộ, Thiền định, Tam muội |
| **Đạo / Tâm linh** | Âm Dương, Ngũ Hành, Cửu Cung, Thái Cực, Bát Quái, Pháp khí, Linh phù, Thần chú, Khai quang, An vị |
| **Nghi lễ** | Thiết đàn, Dâng hương, Phát nguyện, Hồi hướng, Cúng dường, Trai giới, Sám hối |

## Mắt Thần Integration (App Phong Thủy Đế Vương)

Wiki là SSOT cho toàn bộ dữ liệu tâm linh. Mắt Thần KG (Knowledge Graph) lấy dữ liệu từ wiki.

### Pipeline

```
wiki/entities/*.md
    ↓ (frontmatter structured fields)
/llm-wiki mat_than_sync
    ↓ (HTTP POST)
App Phong Thủy: /api/ops/kg/seed
    ↓
Supabase kg_nodes + kg_edges
    ↓
Mắt Thần UI auto-refresh
```

### Quy tắc

1. **Wiki KHÔNG kết nối trực tiếp Supabase** — chỉ gọi REST API của app
2. **Seed endpoint**: `http://localhost:3000/api/ops/kg/seed` (cấu hình trong config.yaml → mat_than.seed_url)
3. **Nodes**: frontmatter fields (id, element, power_level...) → kg_nodes
4. **Edges (kg_edges)**: Có 2 nguồn:
   - **`## Liên kết` section**: `[[slug]]` links → `associated_with` edges (tự động, tất cả entities)
   - **`related_entities` frontmatter** (optional): format `id|type|strength` → typed edges (attendant_of, parent_of, commands...)
   - Nguyên lý y chang Obsidian Graph View — Obsidian đọc `[[wiki-links]]` vẽ đồ thị, mat_than_sync đọc `[[wiki-links]]` tạo kg_edges
5. **Chỉ sync** khi entity có `status: published`
6. **Body section** `## Tóm tắt / Ý nghĩa` → field `summary` trong kg_nodes
7. **Sacred-entities-db archive** (`../App Phong Thủy Đế Vương/sacred-entities-db/data/`) chỉ còn là archive — mọi cập nhật phải làm trong wiki
8. **Concepts** (`wiki/concepts/`) cũng được sync nếu có `status: published` → entity_type: concept nodes

### Khi ingest raw/tam-linh-phong-thuy/char_*.md

Quy trình bổ sung cho ingest entity tâm linh:
1. Parse YAML frontmatter từ raw source (id, element, power_level, aliases, v.v.)
2. Merge vào wiki entity frontmatter (giữ đầy đủ các field)
3. Viết `## Tóm tắt / Ý nghĩa` từ nội dung raw
4. Viết `prompt_vi` và `prompt_en` trong `hinh_tuong` dựa trên mô tả ngoại hình
5. Sau khi tạo entity → NẾU `config.yaml → mat_than.auto_sync_on_ingest: true` → gọi `mat_than_sync` tự động

### Xem thêm

- Seed API: `App Phong Thủy Đế Vương/web-dashboard/app/api/ops/kg/seed/route.ts`
- Config: `config.yaml → mat_than`
- Command: `/llm-wiki mat_than_sync` (xem SKILL.md)
