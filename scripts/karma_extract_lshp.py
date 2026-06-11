# -*- coding: utf-8 -*-
"""karma_extract_lshp.py — Trích đoạn về NGHIỆP từ văn tập Liên Sinh Hoạt Phật (Chân Phật Tông).

Nguồn gốc: raw/sach-tam-linh/Liên Sinh Hoạt Phật - Chân Phật Tông/ (bản dịch Việt đầy đủ — SSOT,
KHÔNG duplicate). Script trích các ĐOẠN VĂN HOÀN CHỈNH chứa từ khóa nghiệp/siêu độ/sám hối/
nguyên thần... (kèm 1 đoạn ngữ cảnh trước-sau, merge đoạn liền kề) → raw/karma/lshp/<slug>.md
với frontmatter source_ref trỏ về sách gốc. Layer: lshp (ADR-05).

Usage: PYTHONUTF8=1 python scripts/karma_extract_lshp.py
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT, "raw", "sach-tam-linh", "Liên Sinh Hoạt Phật - Chân Phật Tông")
OUT_DIR = os.path.join(ROOT, "raw", "karma", "lshp")

KEYWORDS = [
    "nghiệp chướng", "tiêu nghiệp", "nghiệp lực", "túc nghiệp", "nhân quả",
    "siêu độ", "sám hối", "oan thân trái chủ", "chiết linh", "nguyên thần", "hóa thân",
]

# (file sách, slug output, chủ đề chính)
BOOKS = [
    ("040. Thông linh bí pháp thư.md", "040-thong-linh-bi-phap-thu", "nguyên thần / sám hối / nhân quả"),
    ("131. Chuyện lạ về siêu độ.md", "131-chuyen-la-ve-sieu-do", "siêu độ / nghiệp chướng"),
    ("081. Chân Phật Nghi Quỹ Kinh.md", "081-chan-phat-nghi-quy-kinh", "sám hối / nghi quỹ tiêu nghiệp"),
    ("220. Đương Đại Pháp Vương giải đáp nghi hoặc.md", "220-giai-dap-nghi-hoac", "hỏi đáp nghiệp chướng / siêu độ / oan thân trái chủ"),
    ("022. Khởi linh học.md", "022-khoi-linh-hoc", "nguyên thần / tiêu nghiệp / túc nghiệp"),
]

CONTEXT = 1  # số đoạn ngữ cảnh trước/sau đoạn match


def extract(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    low = [p.lower() for p in paras]
    keep = set()
    for i, p in enumerate(low):
        if any(k in p for k in KEYWORDS):
            for j in range(max(0, i - CONTEXT), min(len(paras), i + CONTEXT + 1)):
                keep.add(j)
    # gom các run liền kề thành block
    blocks, cur = [], []
    for i in sorted(keep):
        if cur and i != cur[-1] + 1:
            blocks.append(cur)
            cur = []
        cur.append(i)
    if cur:
        blocks.append(cur)
    out_blocks = ["\n\n".join(paras[i] for i in b) for b in blocks]
    # bỏ block quá ngắn (tiêu đề lẻ)
    return [b for b in out_blocks if len(b) >= 200]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for fname, slug, topic in BOOKS:
        src = os.path.join(SRC_DIR, fname)
        blocks = extract(src)
        title = fname.replace(".md", "")
        body = ("\n\n[...]\n\n").join(blocks)
        fm = f"""---
title: "Trích về Nghiệp — {title}"
type: kien-giai-lshp
source_layer: lshp
source_ref: "Liên Sinh Hoạt Phật Lư Thắng Ngạn — văn tập «{title}» (bản dịch Việt, raw/sach-tam-linh/Liên Sinh Hoạt Phật - Chân Phật Tông/)"
topic: "{topic}"
extracted: 2026-06-12
extraction_note: "Trích tự động các đoạn văn hoàn chỉnh chứa từ khóa nghiệp ({', '.join(KEYWORDS[:5])}...) kèm 1 đoạn ngữ cảnh; dấu [...] = phần lược. Nguyên văn đầy đủ xem sách gốc."
tags: [karma-engine, lshp, chan-phat-tong]
---

"""
        out = os.path.join(OUT_DIR, f"{slug}-trich-nghiep.md")
        open(out, "w", encoding="utf-8", newline="\n").write(fm + body + "\n")
        print(f"{slug}: {len(blocks)} blocks, {len(body)} chars")


if __name__ == "__main__":
    main()
