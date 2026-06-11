# One-off: cắt nguyên văn từng kinh từ text budsas -> file raw/karma/*.md có frontmatter
import re, os

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f), encoding='utf-8').read()

def fm(title, pali, sutta_id, url, extra_note=''):
    note = "Bản dịch Việt: Hòa thượng Thích Minh Châu. Nguồn điện tử: BuddhaSasana (budsas.org) — Bình Anson hiệu đính."
    if extra_note:
        note += ' ' + extra_note
    return f"""---
title: "{title}"
title_pali: "{pali}"
sutta_id: "{sutta_id}"
type: kinh-dien-goc
source: "{url}"
dich_gia: "Hòa thượng Thích Minh Châu"
source_note: "{note}"
fetched: 2026-06-12
immutable: true
tags: [karma-engine, kinh-dien, nikaya]
---

"""

def cut(text, start_pat, end_pat):
    s = re.search(start_pat, text)
    assert s, f'start not found: {start_pat}'
    e = re.search(end_pat, text[s.start():])
    body = text[s.start(): s.start() + e.start()] if e else text[s.start():]
    return body.strip()

jobs = []

# MN 135/136/142: từ tiêu đề kinh đến dòng credit dịch giả (giữ cả dòng credit)
for f, title, pali, sid, url, startpat in [
    ('trung135.txt', '135. Tiểu kinh Nghiệp phân biệt', 'Cūḷakammavibhaṅga Sutta', 'MN 135',
     'https://www.budsas.org/uni/u-kinh-trungbo/trung135.htm', r'135\. Tiểu kinh Nghiệp phân biệt'),
    ('trung136.txt', '136. Đại kinh Nghiệp phân biệt', 'Mahākammavibhaṅga Sutta', 'MN 136',
     'https://www.budsas.org/uni/u-kinh-trungbo/trung136.htm', r'136\. Ðại kinh Nghiệp phân biệt'),
    ('trung142.txt', '142. Kinh Phân biệt cúng dường', 'Dakkhiṇāvibhaṅga Sutta', 'MN 142',
     'https://www.budsas.org/uni/u-kinh-trungbo/trung142.htm', r'142\. Kinh Phân biệt cúng dường'),
]:
    text = read(f)
    body = cut(text, startpat, r'Chân thành cám ơn')
    jobs.append((title, pali, sid, url, body, '', f.replace('.txt', '') + '-final'))

# AN 3.99 Hạt Muối — trích từ phẩm X của tangchi03-0810
t3 = read('tangchi03-0810.txt')
body = cut(t3, r'99\.- Hạt Muối\.', r'100\.')
body = 'X. Phẩm Hạt Muối (trích)\n\n' + body
jobs.append(('Kinh Hạt Muối', 'Loṇakapalla Sutta', 'AN 3.99', 'https://www.budsas.org/uni/u-kinh-tangchibo/tangchi03-0810.htm',
             body, 'Trích từ Tăng Chi Bộ — Chương Ba Pháp, Phẩm X (Hạt Muối), kinh 99 theo đánh số Minh Châu (SuttaCentral: AN 3.100).', None))

# AN 6.63 Một Pháp Môn Quyết Trạch — trích từ tangchi06-0612
t6 = read('tangchi06-0612.txt')
body = cut(t6, r'\(IX\) \(63\) Một Pháp Môn Quyết Trạch', r'\(X\) \(64\)')
jobs.append(('Kinh Một Pháp Môn Quyết Trạch', 'Nibbedhika Sutta', 'AN 6.63', 'https://www.budsas.org/uni/u-kinh-tangchibo/tangchi06-0612.htm',
             body, 'Trích từ Tăng Chi Bộ — Chương Sáu Pháp, Đại Phẩm, kinh 63.', None))

names = {
    'MN 135': 'mn135-tieu-kinh-nghiep-phan-biet.md',
    'MN 136': 'mn136-dai-kinh-nghiep-phan-biet.md',
    'MN 142': 'mn142-kinh-phan-biet-cung-duong.md',
    'AN 3.99': 'an03-099-kinh-hat-muoi.md',
    'AN 6.63': 'an06-063-mot-phap-mon-quyet-trach.md',
}

for title, pali, sid, url, body, extra, _ in jobs:
    out = os.path.join(OUT, names[sid])
    open(out, 'w', encoding='utf-8').write(fm(title, pali, sid, url, extra) + body + '\n')
    print(names[sid], len(body), 'chars')
