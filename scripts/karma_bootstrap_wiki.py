# -*- coding: utf-8 -*-
"""karma_bootstrap_wiki.py — Bootstrap P0.2 Karma Engine.

Sinh wiki/concepts/karma-*.md (Template C + C-R) từ dataset curated bên dưới.
Dataset đối chiếu tay với nguyên văn trong raw/karma/ (fetch 2026-06-12):
  - MN 135 (mn135-tieu-kinh-nghiep-phan-biet.md) — 14 cặp nhân-quả
  - MN 136 (mn136-dai-kinh-nghiep-phan-biet.md) — 10 bất thiện → cõi dữ / 10 thiện → thiện thú
  - MN 142, AN 3.99, AN 6.63 — rules (đã seed karma_rules, không sinh edge ở đây)
  - T 600 (t0600-kinh-thap-thien-nghiep-dao.md) — 10 thiện nghiệp + lợi ích

Chạy 1 LẦN để bootstrap. Sau đó wiki .md là SSOT — sửa tay, KHÔNG chạy đè
(script sẽ từ chối ghi đè file đã tồn tại trừ khi --force).

Usage:  PYTHONUTF8=1 python scripts/karma_bootstrap_wiki.py [--force]
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT_DIR = os.path.join(ROOT, 'wiki', 'concepts')

# ============================================================
# DATASET — curated 2026-06-12
# ============================================================

SUTTAS = [
    # (slug, name, pali/han, description, raw_source_file)
    ('mn135', 'Tiểu kinh Nghiệp phân biệt', 'Cūḷakammavibhaṅga Sutta',
     'Đức Thế Tôn khai thị cho thanh niên Subha Todeyyaputta về 14 cặp nhân-quả: vì sao giữa loài người có kẻ liệt người ưu — "các loài hữu tình là chủ nhân của nghiệp, là thừa tự của nghiệp".',
     'mn135-tieu-kinh-nghiep-phan-biet.md'),
    ('mn136', 'Đại kinh Nghiệp phân biệt', 'Mahākammavibhaṅga Sutta',
     'Đức Thế Tôn phân tích bốn hạng người (làm ác sinh cõi dữ, làm ác sinh thiện thú, làm thiện sinh thiện thú, làm thiện sinh cõi dữ) — logic nghiệp phức hợp, nền tảng tham số thái độ sau (tư hậu) và tà kiến.',
     'mn136-dai-kinh-nghiep-phan-biet.md'),
    ('mn142', 'Kinh Phân biệt cúng dường', 'Dakkhiṇāvibhaṅga Sutta',
     'Đức Thế Tôn giảng cho Tôn giả Ānanda 14 bậc cúng dường phân theo hạng người (bàng sanh ×100 → Như Lai vô lượng), 7 loại cúng dường Tăng chúng và 4 sự thanh tịnh của cúng dường — thang số thiện nghiệp nguyên văn trong kinh.',
     'mn142-kinh-phan-biet-cung-duong.md'),
    ('an3_99', 'Kinh Hạt Muối', 'Loṇakapalla Sutta (AN 3.99; SuttaCentral: AN 3.100)',
     'Cùng một nghiệp nhỏ, người không tu thân-giới-tâm-tuệ phải cảm thọ địa ngục, người có tu chỉ cảm thọ nhẹ ngay hiện tại — như nắm muối trong chén nước nhỏ với nắm muối trong sông Hằng. Nền kinh điển của tham số nền người tạo và cơ chế giảm thọ.',
     'an03-099-kinh-hat-muoi.md'),
    ('an6_63', 'Kinh Một Pháp Môn Quyết Trạch', 'Nibbedhika Sutta (AN 6.63)',
     'Đức Thế Tôn tuyên thuyết "Ta nói tác ý là nghiệp (cetanā)" — sau khi tác ý mới tạo nghiệp về thân, khẩu, ý. Nền tảng của tham số tác ý trong công thức trọng số.',
     'an06-063-mot-phap-mon-quyet-trach.md'),
    ('t600', 'Kinh Thập Thiện Nghiệp Đạo', '十善業道經 (Taishō T 600)',
     'Đức Phật thuyết tại cung điện Long vương Ta-kiệt-la: mười nghiệp thiện (thân 3, khẩu 4, ý 3) là mặt đất cho tất cả pháp lành của trời, người, Thanh văn, Độc giác, Bồ-tát; mỗi thiện nghiệp kèm danh sách lợi ích cụ thể.',
     't0600-kinh-thap-thien-nghiep-dao.md'),
    ('an5_129', 'Kinh Ngũ Nghịch', 'Parikuppa Sutta (AN 5.129)',
     'Đức Thế Tôn dạy: năm nghịch tội (đoạt mạng mẹ, đoạt mạng cha, đoạt mạng vị A-la-hán, với ác tâm làm Như Lai chảy máu, phá hòa hợp Tăng) đưa đến đọa xứ, đưa đến địa ngục, không có thể chữa trị.',
     'an05-129-kinh-ngu-nghich.md'),
    ('t1484_k20', 'Kinh Phạm Võng Bồ Tát Giới — Giới khinh thứ 20', '梵網經 不行放救戒 (T 1484)',
     'Giới không phóng sanh: "vì tâm từ bi mà làm việc phóng sanh... chúng sanh trong lục đạo đều là cha mẹ ta... cho nên phải thường làm việc phóng sanh và khuyên bảo người làm; thấy người đời sát sanh, nên tìm cách cứu hộ cho chúng được thoát khỏi nạn khổ" — nguồn kinh điển trực tiếp của pháp phóng sinh.',
     't1484-pham-vong-gioi-khinh-20-phong-sinh.md'),
]

# (slug, name, pali, category, description, [(fruit_slug, edge_type, weight, sutta_ref)], [source_files], metadata)
ACTIONS = [
    # ---------- 10 ác Thập Thiện + 5 ác MN 135 ----------
    ('sat-sinh', 'Sát sinh', 'Pāṇātipāta', 'than_ac',
     'Giết hại sinh mạng — "tàn nhẫn, tay lấm máu, tâm chuyên sát hại đả thương, tâm không từ bi đối với các loại chúng sanh" (MN 135).',
     [('doan-tho', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135; MN 136')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('trom-cap', 'Trộm cắp', 'Adinnādāna', 'than_ac',
     'Lấy của không cho (MN 136; T 600 gọi là trộm cắp).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ta-hanh', 'Tà hạnh trong các dục', 'Kāmesumicchācāra', 'than_ac',
     'Sống tà hạnh trong các dục (MN 136; T 600 gọi là tà hạnh).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('vong-ngu', 'Vọng ngữ', 'Musāvāda', 'khau_ac',
     'Nói dối, nói láo (MN 136; T 600 gọi là nói dối).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('luong-thiet', 'Nói hai lưỡi', 'Pisuṇā vācā', 'khau_ac',
     'Nói lời ly gián, nói hai lưỡi khiến chia rẽ (MN 136; T 600 gọi là nói hai chiều).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ac-khau', 'Ác khẩu', 'Pharusā vācā', 'khau_ac',
     'Nói lời thô ác, mắng nhiếc (MN 136; T 600 gọi là nói lời thô ác).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('y-ngu', 'Ỷ ngữ', 'Samphappalāpa', 'khau_ac',
     'Nói lời phù phiếm, thêu dệt vô nghĩa (MN 136; T 600 gọi là nói lời thêu dệt).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('tham-duc', 'Tham dục', 'Abhijjhā', 'y_ac',
     'Tâm tham muốn, ham đắm tài vật của người (MN 136; T 600 gọi là tham dục).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('san-han', 'Sân hận, phẫn nộ', 'Byāpāda / Kodha', 'y_ac',
     'Phẫn nộ, nhiều phật ý, "bị nói đến một chút thời bất bình, phẫn nộ, sân hận, chống đối" (MN 135); sân tâm (MN 136); giận dữ (T 600).',
     [('xau-sac', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135; MN 136')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ta-kien', 'Tà kiến', 'Micchādiṭṭhi', 'y_ac',
     'Thấy biết điên đảo về nhân quả, rơi vào đoạn kiến hay thường kiến (MN 136; T 600).',
     [('doa-coi-du', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('nao-hai-chung-sinh', 'Não hại chúng sinh', 'Vihiṃsā', 'than_ac',
     '"Tánh hay não hại các loài hữu tình, với tay, hay với cục đất, hay với cây gậy, hay với cây đao" (MN 135).',
     [('nhieu-benh', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('tat-do', 'Tật đố', 'Issā', 'y_ac',
     'Ganh ghét khi người khác được quyền lợi, tôn trọng, cung kính, cúng dường (MN 135).',
     [('quyen-the-nho', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('khong-bo-thi', 'Xan tham, không bố thí', 'Macchariya', 'y_ac',
     'Không bố thí cho Sa-môn hay Bà-la-môn đồ ăn uống, y phục, ngọa cụ, đèn đuốc (MN 135).',
     [('tai-san-nho', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('ngao-man', 'Ngạo mạn', 'Atimāna', 'y_ac',
     'Ngạo nghễ kiêu mạn, không đảnh lễ người đáng đảnh lễ, không cung kính người đáng cung kính (MN 135).',
     [('gia-dinh-ha-liet', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('khong-hoc-hoi', 'Không thân cận học hỏi Chánh pháp', None, 'y_ac',
     'Không đi đến bậc trí để hỏi: thế nào là thiện, thế nào là bất thiện, làm gì để được lợi ích an lạc lâu dài (MN 135).',
     [('tri-tue-yeu-kem', 'dan_den', 1.0, 'MN 135'), ('doa-coi-du', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    # ---------- 10 thiện Thập Thiện + 5 thiện MN 135 ----------
    ('ly-sat-sinh', 'Từ bỏ sát sinh', 'Pāṇātipātā veramaṇī', 'than_thien',
     '"Bỏ trượng, bỏ kiếm, biết tàm quý, có lòng từ, sống thương xót đến hạnh phúc tất cả chúng sanh" (MN 135); T 600: được mười pháp xa lìa phiền não.',
     [('truong-tho', 'dan_den', 1.0, 'MN 135; T 600'), ('it-benh', 'dan_den', 1.0, 'T 600'),
      ('tam-an-vui-khong-mong-ac', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135; MN 136; T 600')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-trom-cap', 'Từ bỏ trộm cắp', 'Adinnādānā veramaṇī', 'than_thien',
     'Xa lìa trộm cắp — T 600: được mười pháp đáng tin cậy, tài sản dồn đầy không thể hủy hoại.',
     [('tai-san-khong-bi-xam-doat', 'dan_den', 1.0, 'T 600'), ('duoc-nguoi-thuong-men', 'dan_den', 1.0, 'T 600'),
      ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136; T 600')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-ta-hanh', 'Từ bỏ tà hạnh trong các dục', 'Kāmesumicchācārā veramaṇī', 'than_thien',
     'Xa lìa hạnh tà — T 600: đạt bốn pháp được người trí khen ngợi.',
     [('cac-can-dieu-hoa', 'dan_den', 1.0, 'T 600'), ('gia-dinh-trinh-thuan', 'dan_den', 1.0, 'T 600'),
      ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-vong-ngu', 'Từ bỏ vọng ngữ', 'Musāvādā veramaṇī', 'khau_thien',
     'Xa lìa lời nói dối — T 600: đạt tám pháp được chư Thiên khen ngợi.',
     [('loi-noi-duoc-tin-phuc', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-luong-thiet', 'Từ bỏ nói hai lưỡi', 'Pisuṇāya vācāya veramaṇī', 'khau_thien',
     'Xa lìa lời nói ly gián — T 600: được năm pháp chẳng thể hư hoại, quyến thuộc bất hoại.',
     [('quyen-thuoc-hoa-thuan', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-ac-khau', 'Từ bỏ ác khẩu', 'Pharusāya vācāya veramaṇī', 'khau_thien',
     'Xa lìa lời nói thô ác — T 600: thành tựu tám việc làm trong sáng, lời nói được tin theo.',
     [('loi-noi-duoc-ua-thich', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-y-ngu', 'Từ bỏ ỷ ngữ', 'Samphappalāpā veramaṇī', 'khau_thien',
     'Xa lìa lời nói thêu dệt — T 600: thành tựu ba pháp chắc chắn, được bậc trí thương mến.',
     [('duoc-bac-tri-thuong-men', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('ly-tham-duc', 'Từ bỏ tham dục', 'Anabhijjhā', 'y_thien',
     'Xa lìa tham dục — T 600: thành tựu năm pháp tự tại, của cải hơn cả năm lần mong ước.',
     [('cua-cai-y-nguyen-vien-man', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('tu-tam-khong-san', 'Từ tâm, không sân hận', 'Abyāpāda / Mettā', 'y_thien',
     'Không phẫn nộ dầu bị nói đến nhiều (MN 135); T 600: xa lìa giận dữ được tám pháp vui vẻ nơi tâm.',
     [('dep-sac', 'dan_den', 1.0, 'MN 135'), ('tam-hoan-hy-nhu-hoa', 'dan_den', 1.0, 'T 600'),
      ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135; MN 136')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('chanh-kien', 'Chánh kiến', 'Sammādiṭṭhi', 'y_thien',
     'Xa lìa tà kiến — T 600: thành tựu mười pháp công đức, tin sâu nhân quả, thà chết không làm ác.',
     [('sinh-nha-chanh-kien', 'dan_den', 1.0, 'T 600'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 136; T 600')],
     ['mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md'], None),
    ('khong-nao-hai', 'Không não hại chúng sinh', 'Avihiṃsā', 'than_thien',
     'Tánh không não hại các loài hữu tình với tay, cục đất, cây gậy, cây đao (MN 135).',
     [('it-benh', 'dan_den', 1.0, 'MN 135'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('tuy-hy-khong-tat-do', 'Không tật đố, tùy hỷ', 'Anissā / Muditā', 'y_thien',
     'Không ganh ghét khi người khác được quyền lợi, tôn trọng, cúng dường (MN 135).',
     [('quyen-the-lon', 'dan_den', 1.0, 'MN 135'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('bo-thi', 'Bố thí', 'Dāna', 'than_thien',
     'Bố thí cho Sa-môn, Bà-la-môn đồ ăn uống, y phục, ngọa cụ, đèn đuốc (MN 135); thang công đức theo đối tượng xem MN 142.',
     [('tai-san-lon', 'dan_den', 1.0, 'MN 135'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn142-kinh-phan-biet-cung-duong.md'], None),
    ('khiem-cung', 'Khiêm cung, cung kính', 'Nivātavutti', 'than_thien',
     'Không ngạo mạn — đảnh lễ người đáng đảnh lễ, nhường chỗ người đáng nhường, cúng dường người đáng cúng dường (MN 135).',
     [('gia-dinh-cao-quy', 'dan_den', 1.0, 'MN 135'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    ('hoc-hoi-chanh-phap', 'Thân cận học hỏi Chánh pháp', None, 'y_thien',
     'Đi đến bậc trí để hỏi: thế nào là thiện, thế nào là bất thiện, làm gì để được lợi ích an lạc lâu dài (MN 135).',
     [('day-du-tri-tue', 'dan_den', 1.0, 'MN 135'), ('sinh-thien-thu', 'dan_den', 1.0, 'MN 135')],
     ['mn135-tieu-kinh-nghiep-phan-biet.md'], None),
    # ---------- Ngũ vô gián nghiệp (trọng nghiệp categorical — AN 5.129) ----------
    ('giet-me', 'Giết mẹ (đoạt mạng mẹ)', 'Mātughāta', 'than_ac',
     'Ngũ nghịch tội thứ nhất — "đưa đến đọa xứ, đưa đến địa ngục, không có thể chữa trị" (AN 5.129). Trọng nghiệp categorical, override mọi điểm số (§20.1).',
     [('doa-coi-du', 'dan_den', 2.0, 'AN 5.129')],
     ['an05-129-kinh-ngu-nghich.md'], {'garuka': True}),
    ('giet-cha', 'Giết cha (đoạt mạng cha)', 'Pitughāta', 'than_ac',
     'Ngũ nghịch tội — "đưa đến đọa xứ, đưa đến địa ngục, không có thể chữa trị" (AN 5.129). Trọng nghiệp categorical.',
     [('doa-coi-du', 'dan_den', 2.0, 'AN 5.129')],
     ['an05-129-kinh-ngu-nghich.md'], {'garuka': True}),
    ('giet-a-la-han', 'Giết bậc A-la-hán (đoạt mạng vị A-la-hán)', 'Arahantaghāta', 'than_ac',
     'Ngũ nghịch tội — "đưa đến đọa xứ, đưa đến địa ngục, không có thể chữa trị" (AN 5.129). Trọng nghiệp categorical.',
     [('doa-coi-du', 'dan_den', 2.0, 'AN 5.129')],
     ['an05-129-kinh-ngu-nghich.md'], {'garuka': True}),
    ('lam-phat-than-chay-mau', 'Với ác tâm làm Như Lai chảy máu', 'Lohituppāda', 'than_ac',
     'Ngũ nghịch tội — "đưa đến đọa xứ, đưa đến địa ngục, không có thể chữa trị" (AN 5.129). Trọng nghiệp categorical.',
     [('doa-coi-du', 'dan_den', 2.0, 'AN 5.129')],
     ['an05-129-kinh-ngu-nghich.md'], {'garuka': True}),
    ('pha-hoa-hop-tang', 'Phá hòa hợp Tăng', 'Saṅghabheda', 'than_ac',
     'Ngũ nghịch tội — "đưa đến đọa xứ, đưa đến địa ngục, không có thể chữa trị" (AN 5.129). Trọng nghiệp categorical, nặng nhất trong năm tội.',
     [('doa-coi-du', 'dan_den', 2.0, 'AN 5.129')],
     ['an05-129-kinh-ngu-nghich.md'], {'garuka': True}),
]

# (slug, name, pali, description, [source_files])
FRUITS = [
    # ---------- 14 quả MN 135 ----------
    ('doan-tho', 'Đoản thọ (yểu mệnh)', None, 'Mạng sống ngắn ngủi — quả của sát sinh (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('truong-tho', 'Trường thọ', None, 'Mạng sống lâu dài — quả của từ bỏ sát sinh (MN 135; T 600 mục 5 của mười pháp).', ['mn135-tieu-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md']),
    ('nhieu-benh', 'Nhiều bệnh hoạn', None, 'Thân nhiều bệnh tật — quả của não hại chúng sinh (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('it-benh', 'Ít bệnh hoạn', None, 'Thân ít bệnh — quả của không não hại chúng sinh (MN 135); T 600: "thân thể thường không bệnh tật".', ['mn135-tieu-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md']),
    ('xau-sac', 'Xấu sắc', None, 'Dung mạo xấu xí — quả của phẫn nộ sân hận (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('dep-sac', 'Đẹp sắc', 'Pāsādika', 'Dung mạo đoan chính khả ái — quả của không phẫn nộ (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('quyen-the-nho', 'Quyền thế nhỏ', None, 'Uy quyền kém — quả của tật đố (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('quyen-the-lon', 'Quyền thế lớn', None, 'Uy quyền lớn — quả của không tật đố (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('tai-san-nho', 'Tài sản nhỏ', None, 'Nghèo khó — quả của xan tham không bố thí (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('tai-san-lon', 'Tài sản lớn', None, 'Giàu sang nhiều tài sản — quả của bố thí (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('gia-dinh-ha-liet', 'Gia đình hạ liệt', None, 'Sinh vào gia đình thấp kém — quả của ngạo mạn (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('gia-dinh-cao-quy', 'Gia đình cao quý', None, 'Sinh vào gia đình cao quý — quả của khiêm cung (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('tri-tue-yeu-kem', 'Trí tuệ yếu kém', None, 'Thiếu trí — quả của không thân cận học hỏi Chánh pháp (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    ('day-du-tri-tue', 'Đầy đủ trí tuệ', None, 'Trí tuệ đầy đủ — quả của thân cận học hỏi Chánh pháp (MN 135).', ['mn135-tieu-kinh-nghiep-phan-biet.md']),
    # ---------- 2 cõi tái sinh ----------
    ('doa-coi-du', 'Đọa cõi dữ, ác thú, đọa xứ, địa ngục', 'Apāya duggati', 'Sau khi thân hoại mạng chung sinh vào cõi dữ — quả chung của mười bất thiện nghiệp (MN 135; MN 136).', ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn136-dai-kinh-nghiep-phan-biet.md']),
    ('sinh-thien-thu', 'Sinh thiện thú, Thiên giới', 'Sugati sagga loka', 'Sau khi thân hoại mạng chung sinh vào thiện thú, Thiên giới — quả chung của mười thiện nghiệp (MN 135; MN 136; T 600).', ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn136-dai-kinh-nghiep-phan-biet.md', 't0600-kinh-thap-thien-nghiep-dao.md']),
    # ---------- 12 quả đặc thù T 600 ----------
    ('tam-an-vui-khong-mong-ac', 'Tâm an vui, không mộng ác', None, 'T 600 (ly sát sinh, mục 7): "thường không có mộng ác, ngủ hay thức đều yên vui".', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('tai-san-khong-bi-xam-doat', 'Tài sản không bị xâm đoạt', None, 'T 600 (ly trộm cắp, mục 1): "tài sản dồn đầy, vua, giặc, nước, lửa, con hư không thể hủy hoại".', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('duoc-nguoi-thuong-men', 'Được nhiều người thương mến, không ai lừa gạt', None, 'T 600 (ly trộm cắp, mục 2-3).', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('cac-can-dieu-hoa', 'Các căn điều hòa', None, 'T 600 (ly tà hạnh, mục 1-2): các căn điều hòa, dứt hẳn loạn động.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('gia-dinh-trinh-thuan', 'Gia đình trinh thuận', None, 'T 600 (ly tà hạnh, mục 4 + đoạn bố thí trang nghiêm): vợ không thể bị xâm phạm, gia đình trinh thuận.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('loi-noi-duoc-tin-phuc', 'Lời nói được tin phục', None, 'T 600 (ly vọng ngữ, mục 2-3): được người đời tin phục, lời nói ra luôn có chứng cứ.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('quyen-thuoc-hoa-thuan', 'Quyến thuộc hòa thuận, bất hoại', None, 'T 600 (ly nói hai chiều, mục 2 + đoạn bố thí): quyến thuộc bất hoại, hòa thuận cùng chí hướng.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('loi-noi-duoc-ua-thich', 'Lời nói được ưa thích, tiếp nhận', None, 'T 600 (ly ác khẩu, mục 5-8): nói ra người khéo tiếp nhận, lời nói luôn được tin theo.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('duoc-bac-tri-thuong-men', 'Được bậc trí thương mến', None, 'T 600 (ly ỷ ngữ, mục 1-2): được bậc trí thương mến, dùng trí tuệ giải đáp đúng sự thật.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('cua-cai-y-nguyen-vien-man', 'Của cải tự tại, ý nguyện viên mãn', None, 'T 600 (ly tham dục, mục 2-5): của cải tự tại không bị oán tặc chiếm đoạt, được hơn cả năm lần mong ước.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('tam-hoan-hy-nhu-hoa', 'Tâm hoan hỷ, nhu hòa', None, 'T 600 (ly giận dữ, mục 1-5): tâm không phiền não, nhu hòa ngay thẳng, đạt tâm Từ của bậc Thánh.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('sinh-nha-chanh-kien', 'Sinh vào nhà chánh kiến, gặp Phật pháp', None, 'T 600 (ly tà kiến + đoạn bố thí): sinh vào nhà chánh kiến chánh tín, gặp Phật, nghe pháp, cúng dường chúng Tăng.', ['t0600-kinh-thap-thien-nghiep-dao.md']),
]

# (slug, name, pali, group_label, description)
KARMA_CLASSES = [
    ('sanh-nghiep', 'Sanh nghiệp', 'Janaka-kamma', 'theo chức năng', 'Nghiệp tạo ra tái sinh và danh-sắc lúc thụ thai — một trong bốn loại nghiệp phân theo chức năng.'),
    ('tri-nghiep', 'Trì nghiệp', 'Upatthambhaka-kamma', 'theo chức năng', 'Nghiệp nâng đỡ, duy trì quả của sanh nghiệp đã trổ.'),
    ('chuong-nghiep', 'Chướng nghiệp', 'Upapīḷaka-kamma', 'theo chức năng', 'Nghiệp áp chế, làm suy yếu quả của nghiệp khác.'),
    ('doan-nghiep', 'Đoạn nghiệp', 'Upaghātaka-kamma', 'theo chức năng', 'Nghiệp cắt đứt quả của nghiệp khác và thay bằng quả của chính nó.'),
    ('trong-nghiep', 'Trọng nghiệp', 'Garuka-kamma', 'theo thứ tự trổ quả', 'Nghiệp cực nặng (ngũ vô gián về phía ác, thiền chứng về phía thiện) — chắc chắn trổ quả trước mọi nghiệp khác, không gì ngăn được.'),
    ('can-tu-nghiep', 'Cận tử nghiệp', 'Āsanna-kamma', 'theo thứ tự trổ quả', 'Nghiệp tạo hoặc nhớ lại lúc lâm chung — quyết định cảnh giới tái sinh khi không có trọng nghiệp.'),
    ('tap-quan-nghiep', 'Tập quán nghiệp', 'Āciṇṇa-kamma', 'theo thứ tự trổ quả', 'Nghiệp làm thường xuyên thành thói quen — cơ sở kinh điển của tham số tần suất trong calculator.'),
    ('khinh-tac-nghiep', 'Khinh tác nghiệp', 'Kaṭattā-kamma', 'theo thứ tự trổ quả', 'Nghiệp vụn vặt không chủ tâm mạnh — chỉ trổ khi ba loại trên vắng mặt.'),
    ('hien-bao-nghiep', 'Hiện báo nghiệp', 'Diṭṭhadhammavedanīya-kamma', 'theo thời gian trổ quả', 'Nghiệp trổ quả ngay trong kiếp hiện tại.'),
    ('sinh-bao-nghiep', 'Sinh báo nghiệp', 'Upapajjavedanīya-kamma', 'theo thời gian trổ quả', 'Nghiệp trổ quả ở kiếp kế tiếp.'),
    ('hau-bao-nghiep', 'Hậu báo nghiệp', 'Aparāpariyavedanīya-kamma', 'theo thời gian trổ quả', 'Nghiệp trổ quả từ kiếp thứ hai trở đi, bất cứ khi nào hội đủ duyên.'),
    ('vo-hieu-nghiep', 'Vô hiệu nghiệp', 'Ahosi-kamma', 'theo thời gian trổ quả', 'Nghiệp đã qua thời trổ quả, không còn cơ hội cho quả.'),
]
KARMA_CLASS_SOURCE = 'Abhidhamma — Thắng Pháp Tập Yếu Luận (taxonomy mức phân loại, P0; chi tiết sâu ingest ở P3)'

# Template C-R remedies — (slug, name, han, mechanism, target_state, strength_reduction,
#   effort, dosage, timing_rule, counters[(node_slug_or_type, edge_type, strength)],
#   cautions, requires_foundation, source_layer, source_ref, description, sources)
REMEDIES = [
    ('tho-tri-thap-thien', 'Thọ trì mười nghiệp thiện', '受持十善', 'tieu_nhan', 'agami',
     0.3, 3, {'cadence': 'hang_ngay', 'min_duration_months': 6}, None,
     [('action:sat-sinh', 'hoa_giai_boi', 0.8), ('action:trom-cap', 'hoa_giai_boi', 0.8),
      ('action:ta-hanh', 'hoa_giai_boi', 0.8), ('action:vong-ngu', 'hoa_giai_boi', 0.8),
      ('action:luong-thiet', 'hoa_giai_boi', 0.8), ('action:ac-khau', 'hoa_giai_boi', 0.8),
      ('action:y-ngu', 'hoa_giai_boi', 0.8), ('action:tham-duc', 'hoa_giai_boi', 0.8),
      ('action:san-han', 'hoa_giai_boi', 0.8), ('action:ta-kien', 'hoa_giai_boi', 0.8)],
     ['Thọ trì hình thức mà tâm vẫn nuôi ác niệm thì chưa thành tựu — kinh dạy "suốt ngày đêm thường nhớ nghĩ, tư duy quán xét pháp lành, chẳng cho chút nghiệp ác nào xen vào" (T 600)'],
     None, 'kinh_dien', 'T 600 — "Bồ-tát có một pháp để có thể cắt đứt sự khổ trong tất cả các đường ác... Pháp này chính là mười nghiệp thiện"',
     'Giữ gìn trọn vẹn mười thiện nghiệp đạo — Đức Phật dạy đây là một pháp cắt đứt khổ trong tất cả đường ác, là mặt đất cho mọi pháp lành của trời, người và ba thừa.',
     ['t0600-kinh-thap-thien-nghiep-dao.md']),
    ('tu-tap-than-gioi-tam-tue', 'Tu tập về thân, giới, tâm, tuệ', '修身戒心慧', 'giam_tho', 'prarabdha',
     0.2, 4, {'cadence': 'hang_ngay', 'min_duration_months': 6}, None,
     [('fruit:doa-coi-du', 'giam_nhe', 0.7)],
     ['Đây là chuyển hóa nền tâm thức lâu dài, không phải nghi thức một lần — dưới ngưỡng tinh tấn đều đặn thì "người chứa" chưa rộng ra (AN 3.99)'],
     None, 'kinh_dien', 'AN 3.99 — nắm muối trong chén nước với nắm muối trong sông Hằng: người tu tập thân-giới-tâm-tuệ, nghiệp nhỏ chỉ cảm thọ ngay hiện tại, không rơi địa ngục',
     'Mở rộng "người chứa" theo Kinh Hạt Muối: cùng một nghiệp ác nhỏ, người có tu tập về thân, về giới, về tâm, về tuệ chỉ cảm thọ nhẹ ngay hiện tại thay vì cảm thọ nơi địa ngục.',
     ['an03-099-kinh-hat-muoi.md']),
    ('bo-thi-cung-duong', 'Bố thí, cúng dường', '布施供養', 'giam_tho', 'prarabdha',
     0.2, 2, {'cadence': 'hang_thang', 'min_duration_months': 6}, None,
     [('action:khong-bo-thi', 'hoa_giai_boi', 0.8), ('fruit:tai-san-nho', 'giam_nhe', 0.5)],
     ['Cúng dường chỉ thanh tịnh trọn vẹn khi cả người cho lẫn người nhận giữ giới theo thiện pháp — vật thí đúng pháp, tâm khéo hoan hỷ, lòng tin vững vàng (MN 142, bốn sự thanh tịnh)'],
     None, 'kinh_dien', 'MN 135 (bố thí → tài sản lớn) + MN 142 (thang 14 bậc đối tượng, 7 loại cúng dường Tăng chúng, 4 sự thanh tịnh)',
     'Đối trị xan tham và quả nghèo khó; công đức tùy bậc đối tượng nhận và sự thanh tịnh của hai bên theo Kinh Phân biệt cúng dường.',
     ['mn135-tieu-kinh-nghiep-phan-biet.md', 'mn142-kinh-phan-biet-cung-duong.md']),
    ('phong-sinh', 'Phóng sinh', '放生', 'giam_tho', 'prarabdha',
     0.2, 2, {'cadence': 'hang_thang', 'min_duration_months': 6}, None,
     [('action:sat-sinh', 'hoa_giai_boi', 0.8), ('fruit:doan-tho', 'giam_nhe', 0.5),
      ('fruit:nhieu-benh', 'giam_nhe', 0.5)],
     ['Phóng sinh sai cách (mua chim bị bắt lại, thả loài ngoại lai sai môi trường) nuôi cầu sát nghiệp thay vì cứu hộ — chọn loài bản địa, thả đúng môi trường, ưu tiên cứu vật sắp bị giết thật',
      'Tinh thần kinh là CỨU HỘ khi thấy chúng sinh lâm nạn ("thấy người đời sát sanh, nên tìm cách cứu hộ") — không phải nghi thức mua-thả định kỳ'],
     None, 'kinh_dien', 'Phạm Võng Bồ Tát Giới — giới khinh thứ 20 (T 1484): "phải thường làm việc phóng sanh và khuyên bảo người làm"; T 600 (ly sát sinh, mục 1: ban cho sự không sợ hãi — thí vô úy)',
     'Cứu mạng chúng sinh sắp bị giết — đối trị trực tiếp sát nghiệp; Kinh Phạm Võng dạy chúng sanh trong lục đạo đều là cha mẹ ta nên phải thường hành phóng sinh và cứu hộ.',
     ['t1484-pham-vong-gioi-khinh-20-phong-sinh.md', 't0600-kinh-thap-thien-nghiep-dao.md']),
]

# ============================================================
# GENERATOR
# ============================================================

def node_id(node_type, idx, slug):
    if node_type == 'sutta':
        return f'karma_sutta_{slug}'
    return f'karma_{node_type}_{idx:03d}_{slug}'

def fname(node_type, slug):
    return f'karma-{node_type.replace("_", "-")}-{slug}.md'

# build id maps
ACTION_IDS = {a[0]: node_id('action', i + 1, a[0]) for i, a in enumerate(ACTIONS)}
FRUIT_IDS = {f[0]: node_id('fruit', i + 1, f[0]) for i, f in enumerate(FRUITS)}
CLASS_IDS = {c[0]: node_id('class', i + 1, c[0]) for i, c in enumerate(KARMA_CLASSES)}
REMEDY_IDS = {r[0]: node_id('remedy', i + 1, r[0]) for i, r in enumerate(REMEDIES)}
SUTTA_IDS = {s[0]: node_id('sutta', 0, s[0]) for s in SUTTAS}

ALL_FILES = {}  # id -> filename (cho [[link]])

def reg(nid, node_type, slug):
    ALL_FILES[nid] = fname(node_type, slug).replace('.md', '')

for i, a in enumerate(ACTIONS):
    reg(ACTION_IDS[a[0]], 'action', a[0])
for i, f in enumerate(FRUITS):
    reg(FRUIT_IDS[f[0]], 'fruit', f[0])
for i, c in enumerate(KARMA_CLASSES):
    reg(CLASS_IDS[c[0]], 'class', c[0])
for i, r in enumerate(REMEDIES):
    reg(REMEDY_IDS[r[0]], 'remedy', r[0])
for s in SUTTAS:
    reg(SUTTA_IDS[s[0]], 'sutta', s[0])


def yaml_str(v):
    return '"' + str(v).replace('"', '\\"') + '"'


def write_file(path, content, force):
    if os.path.exists(path) and not force:
        print('SKIP (exists):', os.path.basename(path))
        return False
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(content)
    print('WROTE:', os.path.basename(path))
    return True


def gen_sutta(s):
    slug, name, pali, desc, src = s
    nid = SUTTA_IDS[slug]
    lines = ['---', f'id: {nid}', 'type: karma', 'node_type: sutta',
             f'name: {yaml_str(name)}', f'name_pali: {yaml_str(pali)}',
             f'description: {yaml_str(desc)}', 'status: published', f'sources: [{src}]', '---', '']
    lines += [f'# {name}', '', desc, '',
              f'> Nguyên văn bản dịch: `raw/karma/{src}`', '']
    return fname('sutta', slug), '\n'.join(lines)


def gen_action(a, idx):
    slug, name, pali, cat, desc, rels, srcs, meta = a
    nid = ACTION_IDS[slug]
    lines = ['---', f'id: {nid}', 'type: karma', 'node_type: action',
             f'name: {yaml_str(name)}']
    if pali:
        lines.append(f'name_pali: {yaml_str(pali)}')
    lines.append(f'category: {cat}')
    if meta:
        lines.append('metadata:')
        for k, v in meta.items():
            lines.append(f'  {k}: {str(v).lower() if isinstance(v, bool) else v}')
    if rels:
        lines.append('karma_relations:')
        for fruit_slug, etype, w, ref in rels:
            lines += [f'  - target: {FRUIT_IDS[fruit_slug]}',
                      f'    type: {etype}',
                      f'    base_weight: {w}',
                      f'    sutta_ref: {yaml_str(ref)}']
    lines += ['status: published',
              'sources: [' + ', '.join(srcs) + ']' if srcs else 'sources: []',
              '---', '', f'# {name}', '', desc, '']
    if rels:
        lines += ['## Liên kết', '']
        for fruit_slug, etype, w, ref in rels:
            lines.append(f'- {etype} → [[{ALL_FILES[FRUIT_IDS[fruit_slug]]}]] ({ref})')
        lines.append('')
    return fname('action', slug), '\n'.join(lines)


def gen_fruit(f, idx):
    slug, name, pali, desc, srcs = f
    nid = FRUIT_IDS[slug]
    lines = ['---', f'id: {nid}', 'type: karma', 'node_type: fruit',
             f'name: {yaml_str(name)}']
    if pali:
        lines.append(f'name_pali: {yaml_str(pali)}')
    lines += ['status: published', 'sources: [' + ', '.join(srcs) + ']',
              '---', '', f'# {name}', '', desc, '']
    return fname('fruit', slug), '\n'.join(lines)


def gen_class(c, idx):
    slug, name, pali, group, desc = c
    nid = CLASS_IDS[slug]
    lines = ['---', f'id: {nid}', 'type: karma', 'node_type: karma_class',
             f'name: {yaml_str(name)}', f'name_pali: {yaml_str(pali)}',
             f'category: {yaml_str("12 loại nghiệp — " + group)}',
             f'description: {yaml_str(desc)}',
             f'source_ref: {yaml_str(KARMA_CLASS_SOURCE)}',
             'status: published', 'sources: []', '---', '',
             f'# {name} ({pali})', '', desc, '',
             f'> Thuộc nhóm phân loại **{group}** trong 12 loại nghiệp Abhidhamma.', '']
    return fname('class', slug), '\n'.join(lines)


def gen_remedy(r, idx):
    (slug, name, han, mech, state, sred, effort, dosage, timing,
     counters, cautions, req_found, layer, sref, desc, srcs) = r
    nid = REMEDY_IDS[slug]
    lines = ['---', f'id: {nid}', 'type: karma', 'node_type: remedy',
             f'name: {yaml_str(name)}', f'name_han: {yaml_str(han)}',
             f'remedy_mechanism: {mech}', f'target_karma_state: {state}',
             f'strength_reduction: {sred}', f'effort: {effort}', 'dosage:',
             f'  cadence: {dosage["cadence"]}',
             f'  min_duration_months: {dosage["min_duration_months"]}']
    if timing:
        lines.append(f'timing_rule: {timing}')
    lines.append('counters:')
    for tgt, etype, strength in counters:
        ttype, tslug = tgt.split(':')
        tid = ACTION_IDS[tslug] if ttype == 'action' else FRUIT_IDS[tslug]
        lines += [f'  - target: {tid}', f'    type: {etype}', f'    strength: {strength}']
    lines.append('cautions:')
    for c in cautions:
        lines.append(f'  - {yaml_str(c)}')
    lines += [f'requires_foundation: {req_found if req_found else "null"}',
              f'source_layer: {layer}', f'source_ref: {yaml_str(sref)}',
              'status: published', 'confidence: high',
              'sources: [' + ', '.join(srcs) + ']', '---', '',
              f'# {name}', '', desc, '', '## Liên kết', '']
    for tgt, etype, strength in counters:
        ttype, tslug = tgt.split(':')
        tid = ACTION_IDS[tslug] if ttype == 'action' else FRUIT_IDS[tslug]
        lines.append(f'- {etype} ← [[{ALL_FILES[tid]}]]')
    lines.append('')
    return fname('remedy', slug), '\n'.join(lines)


def main():
    force = '--force' in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    written = 0
    for s in SUTTAS:
        fn, content = gen_sutta(s)
        written += write_file(os.path.join(OUT_DIR, fn), content, force)
    for i, a in enumerate(ACTIONS):
        fn, content = gen_action(a, i)
        written += write_file(os.path.join(OUT_DIR, fn), content, force)
    for i, f in enumerate(FRUITS):
        fn, content = gen_fruit(f, i)
        written += write_file(os.path.join(OUT_DIR, fn), content, force)
    for i, c in enumerate(KARMA_CLASSES):
        fn, content = gen_class(c, i)
        written += write_file(os.path.join(OUT_DIR, fn), content, force)
    for i, r in enumerate(REMEDIES):
        fn, content = gen_remedy(r, i)
        written += write_file(os.path.join(OUT_DIR, fn), content, force)
    total = len(SUTTAS) + len(ACTIONS) + len(FRUITS) + len(KARMA_CLASSES) + len(REMEDIES)
    print(f'\nDone: {written}/{total} files written to {OUT_DIR}')
    print(f'  suttas={len(SUTTAS)} actions={len(ACTIONS)} fruits={len(FRUITS)} '
          f'classes={len(KARMA_CLASSES)} remedies={len(REMEDIES)}')


if __name__ == '__main__':
    main()
