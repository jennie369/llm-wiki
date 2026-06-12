# Karma Engine MCP — hướng dẫn dùng (agent)

> Server `karma` (stdio) — wrapper mỏng gọi Supabase Edge Functions. Logic + dữ liệu DUY NHẤT ở
> `karma_nodes/edges/rules/passages` (project `pgfkbcnzqozzkohwbgbk`).
> Plan kiến trúc: `crypto-pattern-scanner/docs/design_and_architecture/KARMA_ENGINE_ARCHITECTURE_PLAN.md`.
> Nguyên tắc vàng: mọi kết quả truy ngược được về Kinh tham chiếu — KHÔNG tự suy diễn quy luật nhân-quả ngoài citations trả về.

## Tools (P1+P2+P4+P5 — đủ bộ)

### `karma__diagnose` — ĐIỂM VÀO MẶC ĐỊNH (router đa chiều)
Khi user mô tả TỰ DO (không biết mình cần track nào) → dùng tool này TRƯỚC. Input `{text}`. Engine detect: `van_de` (mô tả khổ/vận hạn) → suy ngược quả→nhân từ KG + remedies có citation; `hanh_dong` → trả action_id + tham số để gọi tiếp karma__calculate; `giao_ly` → tự forward RAG; `ngoai_pham_vi` → từ chối. LLM chỉ phân loại — nhân-quả 100% từ KG. Trình bày: nhấn mạnh "một quả nhiều nhân — đây là các nhân KHẢ DĨ theo Kinh, không phán định".

### `karma__simulate` (P5 — What-if)
Mô phỏng remedy lên findings của `karma__chartRead`. Input `{findings, remedy_ids[], van_windows?}`. 4 cơ chế trung thực giáo lý: `tieu_nhan` KHÔNG đổi Prārabdha (chỉ phòng hộ tương lai) · `giam_tho` giảm ~1 band, floor 0.15 KHÔNG về 0 · `chan_duyen` đóng cửa sổ duyên = HOÃN không tiêu · `phong_ngua` chặn tích lũy. Output: comparison trước/sau + `leverage_ranking` + verdict mỗi quả (KHÔNG đổi/HOÃN/GIẢM — nói thẳng, không vẽ hy vọng giả). Workflow chuẩn: `tuvi__getChartVN` → (`tuvi__getHoroscope`) → `karma__chartRead` → `karma__simulate`.

### `karma__chartRead` (P4 — Track C)
Suy ngược lá số Tử Vi (quả đã trổ) → nhân nghiệp + remedy. **Workflow bắt buộc**: `tuvi__getChartVN` trước → đưa NGUYÊN output JSON vào `{chart}`. Matcher luận theo CỤM (cách cục > trường cung > tổ hợp bản cung — sao đơn chỉ làm modifier giải/phá/tăng) trên `karma_chart_mappings` đã duyệt. Output: `karma_findings[]` (fruit + `combined_score` noisy-OR + patterns matched + `inferred_causes` truy về Kinh + remedies) + `citations_by_layer`. **Trình bày**: lớp mapping sao→nghiệp là DIỄN GIẢI HUYỀN HỌC (tin cậy thấp hơn Kinh điển 1 bậc) — chỉ nói "khuynh hướng", PHẢI tách lớp nguồn khi dẫn. `include_unapproved=true` CHỈ để test pipeline.

### `karma__ask` (P2)
Hỏi đáp RAG tiếng Việt trên nền Kinh tạng. Input `{question}`. Output `answer` (mọi nhận định kèm [nguồn]) + `citations[]` + `refused` (true = ngoài phạm vi, hệ TỪ CHỐI thay vì suy diễn — golden set eval đảm bảo hành vi này). Nhãn nguồn hợp lệ: MN 135 · MN 136 · MN 142 · AN 3.99 · AN 5.129 · AN 6.63 · T 600 · Phạm Võng giới 20.

### `karma__searchPassages` (P2)
Tra cứu NGUYÊN VĂN đoạn kinh theo ngữ nghĩa (pgvector, KHÔNG LLM). Input `{question, match_count?}`. Output top-k passages (label + similarity + content) + structured facts từ KG. Dùng khi cần trích dẫn nguyên văn.

### `karma__listActions`
Tra taxonomy hành động để lấy `action_id` đúng. Filter optional `category`: `than_ac|khau_ac|y_ac|than_thien|khau_thien|y_thien`.

### `karma__calculate`
Tính nghiệp deterministic (KHÔNG LLM).

**Hành động ÁC** — 4 tham số BẮT BUỘC + 5 optional:

```json
{
  "action_id": "karma_action_001_sat-sinh",
  "intent": "co_y",                  // vo_tinh | nua_vo_tinh | co_y | co_y_lap_ke_hoach  [AN 6.63]
  "target_relation": "chung_sinh_thuong", // ... | an_nhan | cha_me | bac_tu_hanh | tang_doan
  "frequency": "thoi_quen",          // mot_lan | vai_lan | thoi_quen | nghe_nghiep
  "attitude_after": "da_dung_sam_hoi", // hoan_hy_khoe | khong | nhan_thuc | da_dung | da_dung_sam_hoi [MN 136]
  "completion": "hoan_thanh", "role": "tu_lam", "target_scale": "mot",
  "ditthi": false, "doer_foundation": "co_gioi"   // optional [AN 3.99]
}
```

**Hành động THIỆN** (category `*_thien`) — track punna riêng theo MN 142:

```json
{ "action_id": "karma_action_028_bo-thi", "punna_target": "pham_phu_giu_gioi", "punna_purity": "ca_hai_tinh" }
```

**Output**: `karma_score` + `severity_band` (`nhe|trung_binh|nang|trong_nghiep`) hoặc `punna` (track thiện), `fruits[]` (kèm `sutta_ref`), `remedies[]` (kèm `mechanism`: tieu_nhan/chan_duyen/giam_tho/phong_ngua + `cautions`), `applied_rules[]` (từng multiplier + căn cứ kinh), `citations[]`, `disclaimer`.

## Quy tắc trình bày cho agent
1. LUÔN dẫn citations dạng [MN 135], [AN 5.129]... khi nêu nhân-quả.
2. KHÔNG tiên đoán tuyệt đối ("chắc chắn sẽ...") — dùng "theo Kinh..., hành nghiệp này dẫn đến khuynh hướng...".
3. Kết thúc bằng hướng chuyển nghiệp (remedies trong output) — nêu rõ cơ chế và cautions.
4. Trọng nghiệp (`trong_nghiep`): nói thẳng theo AN 5.129 "không thể chữa trị" nhưng vẫn dẫn hướng tu tập (AN 3.99 giảm thọ) — không gieo sợ hãi cực đoan.
5. Multiplier hiện là bản DRAFT (`karma_rules.approved=false`) — nếu user hỏi về độ tin cậy con số, nói rõ trọng số đang chờ duyệt, căn cứ kinh ở cột `sutta_ref`.

## Vận hành
- Sửa wrapper → restart MCP server (stdio không hot-reload — Gotcha #7 bazi).
- Secret đọc từ `crypto-pattern-scanner/.env.local` (SUPABASE_URL + SERVICE_ROLE) — không nằm trong mcp.json.
