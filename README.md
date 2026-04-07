# LLM Wiki

Hệ thống knowledge base cá nhân hoàn toàn tự động, vận hành bởi LLM. Dựa trên pattern [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) của Andrej Karpathy.

LLM tự tìm nguồn, tự tổng hợp thành wiki có cấu trúc, tự duy trì cross-references, phát hiện mâu thuẫn, và giữ mọi thứ cập nhật — bạn chỉ cần đọc và hỏi.

> **Lưu ý:** Hiện tại hệ thống chỉ hỗ trợ [Claude Code](https://claude.ai/code) (Anthropic) làm engine. Cần có Claude Code CLI hoặc VS Code extension để sử dụng.

## Khác gì so với RAG?

| | RAG truyền thống | LLM Wiki |
|---|---|---|
| Kiến thức | Tìm lại từ đầu mỗi lần hỏi | Biên dịch 1 lần, duy trì liên tục |
| Cross-references | Không có | Tự động tạo và duy trì |
| Mâu thuẫn | Không phát hiện | Đánh dấu ngay khi ingest |
| Tích lũy | Không | Compound theo thời gian |
| Hạ tầng | Vector DB + embeddings | Chỉ cần folders + markdown |

## Bắt đầu nhanh

### 1. Clone & Cài đặt

```bash
git clone https://github.com/mduongvandinh/llm-wiki.git
cd llm-wiki

# Copy file cấu hình mẫu
cp config.example.yaml config.yaml

# Cài skill vào Claude Code
cp -r skills/llm-wiki ~/.claude/skills/llm-wiki
```

### 2. Cấu hình chủ đề quan tâm

Sửa `config.yaml` — thêm topics, keywords, và nguồn theo dõi:

```yaml
topics:
  - name: "Chủ đề của bạn"
    keywords: ["từ khóa 1", "từ khóa 2"]
    priority: high
```

### 3. Chạy

```bash
# Trong Claude Code hoặc VS Code có Claude Code extension:
/llm-wiki run          # Chạy full cycle: discover → ingest → lint
/llm-wiki status       # Xem trạng thái wiki
/llm-wiki query "..."  # Hỏi đáp
```

### 4. Xem wiki

- **Obsidian**: File → Open vault → chọn folder `llm-wiki` → Graph View
- **Browser**: mở `wiki-viewer.html` để xem dashboard + graph (hỗ trợ mobile)

---

## Danh sách lệnh

| Lệnh | Mô tả |
|-------|--------|
| `/llm-wiki init "Topic"` | Thêm chủ đề mới |
| `/llm-wiki ingest` | Xử lý nguồn mới trong `raw/` |
| `/llm-wiki query "..."` | Hỏi đáp dựa trên wiki, tự lưu kết quả |
| `/llm-wiki lint` | Kiểm tra sức khỏe: mâu thuẫn, orphans, gaps |
| `/llm-wiki discover` | Tự tìm nguồn mới từ internet |
| `/llm-wiki run` | Full cycle: discover → ingest → lint |
| `/llm-wiki status` | Xem trạng thái tổng quan |
| `/llm-wiki digest` | Bản tin hàng ngày: nguồn mới, insights, pain points |
| `/llm-wiki pain-rank` | Xếp hạng pain points theo tiềm năng kinh doanh |

---

## Chạy tự động

### Cách 1: `/loop` trong Claude Code (khuyến nghị)

```bash
/loop 1h /llm-wiki run    # Mỗi 1 giờ
/loop 30m /llm-wiki run   # Mỗi 30 phút
/loop 2h /llm-wiki run    # Mỗi 2 giờ
```

Chạy trong session hiện tại. Không tốn thêm chi phí. Dừng khi đóng session.

### Cách 2: Lập lịch hệ thống (chạy nền, không cần mở Claude Code)

**Windows** (PowerShell, chạy với quyền Admin):
```powershell
powershell -ExecutionPolicy Bypass -File "scripts/setup-scheduler.ps1"
```

**macOS/Linux** (crontab):
```bash
# Thêm vào crontab -e:
0 */2 * * * cd /path/to/llm-wiki && claude --print "/llm-wiki run" >> outputs/auto-run.log 2>&1
```

### So sánh

| | `/loop` (trong session) | Lập lịch hệ thống |
|---|---|---|
| Khi nào chạy | Khi mở Claude Code/VS Code | Bất cứ lúc nào máy bật |
| Tần suất | Linh hoạt (10 phút đến 2 giờ) | Cố định (VD: mỗi 2 giờ) |
| Chi phí token | Thấp (cùng session) | Cao hơn (mỗi lần = session mới) |
| Cài đặt | Gõ lệnh là xong | Chạy script 1 lần (quyền admin) |

---

## Thêm nguồn

### Thủ công

Tạo file markdown rồi bỏ vào `raw/articles/`, `raw/reddit/`, hoặc `raw/notes/`:

```markdown
---
title: "Tiêu đề bài viết"
url: "https://example.com/article"
author: "Tên tác giả"
discovered: 2026-04-07
topic: "Tên chủ đề"
---

Nội dung bài viết ở đây...
```

Sau đó chạy `/llm-wiki ingest`.

### Qua Obsidian Web Clipper

1. Cài extension [Obsidian Web Clipper](https://obsidian.md/clipper)
2. Thấy bài hay → click icon clipper → lưu vào `raw/articles/`
3. Chạy `/llm-wiki ingest`

---

## Cấu trúc thư mục

```
llm-wiki/
├── CLAUDE.md              ← Schema & quy tắc cho LLM
├── config.yaml            ← Cấu hình chủ đề, nguồn, lịch chạy
├── config.example.yaml    ← File mẫu cho người dùng mới
├── wiki-viewer.html       ← Trình xem wiki (mobile-first, dark theme, graph)
├── raw/                   ← Nguồn thô (LLM KHÔNG ĐƯỢC SỬA)
│   ├── articles/          ← Bài viết, papers
│   ├── reddit/            ← Pain points, use cases từ Reddit
│   ├── twitter/           ← Tweets (follow-builders + Web Clipper)
│   ├── notes/             ← Ghi chú cá nhân
│   └── media/             ← Ảnh chụp, sơ đồ
├── wiki/                  ← Wiki do LLM viết & duy trì
│   ├── INDEX.md           ← Danh mục tất cả trang wiki
│   ├── LOG.md             ← Nhật ký hoạt động
│   ├── entities/          ← Người, tổ chức, công cụ, dự án
│   ├── concepts/          ← Khái niệm, pattern, phương pháp
│   ├── sources/           ← Tóm tắt từng nguồn thô
│   └── syntheses/         ← Phân tích tổng hợp, so sánh
├── outputs/               ← Kết quả hỏi đáp, báo cáo, xếp hạng
├── .discoveries/          ← Metadata cho auto-discovery
├── scripts/               ← Scripts tự động
│   ├── run-wiki.sh        ← Cho lập lịch hệ thống
│   └── setup-scheduler.ps1
├── skills/                ← Claude Code skill (copy vào ~/.claude/skills/)
│   └── llm-wiki/
│       └── SKILL.md
└── docs/plans/            ← Tài liệu thiết kế
```

---

## Kiến trúc

```
┌──────────────────────────────────────────────────────┐
│                  BẠN (đọc & hỏi)                      │
├──────────────────────────────────────────────────────┤
│  wiki/          │  outputs/        │  wiki-viewer     │
│  (Obsidian)     │  (bản tin, rank) │  (.html)         │
├──────────────────────────────────────────────────────┤
│                  LLM (viết & duy trì)                 │
├──────────┬───────────┬──────────┬────────────────────┤
│ discover │  ingest   │  query   │  lint              │
│ (tìm)    │ (xử lý)   │ (đáp)    │ (kiểm tra)        │
├──────────┴───────────┴──────────┴────────────────────┤
│  raw/           │  config.yaml     │  CLAUDE.md       │
│  (nguồn thô)    │  (cấu hình)      │  (quy tắc)       │
└──────────────────────────────────────────────────────┘
```

**Luồng chính:** discover → raw/ → ingest → wiki/ → query → outputs/

**Vòng lặp tự cải thiện:** lint phát hiện gaps → discover tìm nguồn → ingest lấp đầy → wiki ngày càng giàu

---

## Tác giả & Nguồn cảm hứng

- Pattern gốc: [Andrej Karpathy — LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Hướng dẫn thực hành: [Nick Spisak — How to Build Your Second Brain](https://x.com/NickSpisak_/status/2040448463540830705)
- Engine: [Claude Code](https://claude.ai/code) (Anthropic)
- Xem wiki: [Obsidian](https://obsidian.md/)
- Bản tin Twitter: [follow-builders](https://github.com/zarazhangrui/follow-builders)

## Giấy phép

MIT
