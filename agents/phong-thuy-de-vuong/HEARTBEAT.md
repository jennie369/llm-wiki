# HEARTBEAT.md -- Phong Thủy Đế Vương Heartbeat Checklist

Run this checklist on every heartbeat.

> ⚡ **TƯ DUY CHỦ ĐỘNG (PROACTIVE MINDSET):** Mọi hành động trong heartbeat này đều hướng tới việc tự chủ động đề xuất các hướng nghiên cứu sâu, tự động thực hiện nghiên cứu những vấn đề đó (loop learning liên tục), và lập tức báo cáo cho chủ nhân chứ TUYỆT ĐỐI KHÔNG CẦN đợi chủ nhân ra chỉ thị mới bắt đầu làm việc.

## 0. Load Shared Context (FIRST — before anything else)

Read these files to know what happened since your last heartbeat:

1. `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/today.md` — What other agents and Claude Code sessions did today
2. `memory/active-tasks.json` — Which tasks are in-flight, who's working on what
3. `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/MEMORY.md` — Your tacit knowledge and lessons
4. `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/daily/` — Your most recent daily note (if exists)
5. `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/shared/MEMORY.md` — Cross-agent knowledge

This ensures you don't duplicate work or miss context from other sessions.

## 0.5. Budget Awareness

1. Check chi phí tháng này từ `gemops_cost_tracking` hoặc Paperclip Costs API
2. Nếu ≥ 70% budget VÀ chưa nhắc tháng này:
   → Comment: "💡 70% budget. Ưu tiên tasks quan trọng."
   → Ghi memory: "budget_nudge_70_sent: YYYY-MM-DD" vào `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/MEMORY.md`
3. Nếu ≥ 90% budget:
   → Comment: "⚠️ 90% budget. Chỉ nhận critical."
   → Chỉ xử lý P0/P1 tasks

## 0.6. Skill Check

1. Đọc `skills-store/INDEX.md` — xem có skills mới không
2. Nếu task đang làm match skill → dùng skill thay vì làm từ đầu
3. Nếu có skills mới do agent khác tạo → ghi nhận vào memory

## 0.7. Extract Issue Lessons (BẮT BUỘC — Feedback Loop)

Trước khi nhận task mới, kiểm tra issues của mình đã đóng trong 24h qua để
trích xuất lesson — tránh lặp lại cùng lỗi heartbeat sau.

```bash
PYTHONUTF8=1 python scripts/extract_issue_lessons.py --agent phong-thuy-de-vuong --list --since-hours 24 --limit 5
```

Stdout = JSON array issues chưa extract. Với MỖI issue:

1. **Đọc** `description` + `comments` (tập trung comment cuối cùng từ CEO/Chủ Tướng có fix decision)
2. **Distill** lesson markdown 4-6 dòng theo format CỐ ĐỊNH (xem `skills-store/extract-issue-lessons/1.0.0/SKILL.md`):
   ```markdown
   **Triệu chứng**: <1-2 câu lỗi user-visible>
   **Root cause**: <1-2 câu nguyên nhân gốc>
   **Fix**: <1-2 câu cách giải quyết, ai/file/commit>
   **Tránh lại**: <1 câu rule cứng>
   ```
3. **Ghi temp file** `/tmp/lesson_<identifier>.md` với nội dung distill
4. **Gọi script append**:
   ```bash
   PYTHONUTF8=1 python scripts/extract_issue_lessons.py --agent phong-thuy-de-vuong --append \
       --issue-id <UUID> --issue-identifier <GEM-XXX> \
       --content-file /tmp/lesson_<GEM-XXX>.md
   ```

Script tự append vào 3 SSOT (TROUBLESHOOTING.md per-agent ở `llm-wiki/agents/phong-thuy-de-vuong/` + MEMORY.md per-agent ở `crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/` + project MEMORY.md) + mark issue đã processed.

Nếu list `[]` → skip section này, sang Section 1.

KHÔNG bỏ qua section này dù nghĩ "không có gì đáng học" — script tự skip nếu list rỗng.

## 1. Identity and Context

- `GET /api/agents/me` -- confirm your id, role, budget, chainOfCommand.
- Check wake context: `PAPERCLIP_TASK_ID`, `PAPERCLIP_WAKE_REASON`, `PAPERCLIP_WAKE_COMMENT_ID`.

## 2. Local Planning Check

1. Read today's plan from `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/daily/YYYY-MM-DD.md` under "## Today's Plan".
2. Review each planned item: what is completed, what is blocked, what is next.
3. For any blockers, resolve them yourself or escalate via chainOfCommand.
4. If you are ahead, start on the next highest priority.
5. **Record progress updates** in the daily notes.

## 3. Approval Follow-Up

If `PAPERCLIP_APPROVAL_ID` is set:

- Review the approval and its linked issues.
- Close resolved issues or comment on what remains open.

## 4. Get Assignments

- `GET /api/companies/{companyId}/issues?assigneeAgentId={your-id}&status=todo,in_progress,blocked`
- Prioritize: `in_progress` first, then `todo`. Skip `blocked` unless you can unblock it.
- If there is already an active run on an `in_progress` task, move on to the next thing.
- If `PAPERCLIP_TASK_ID` is set and assigned to you, prioritize that task.

## 5. Checkout and Work

- Always checkout before working: `POST /api/issues/{id}/checkout`.
- Never retry a 409 -- that task belongs to someone else.
- Do the work. Update status and comment when done.

## 6. Knowledge Base Consultation

When working on a task, follow this process:

1. **Tra cứu `SOUL.md`**: BẮT BUỘC đọc "Research Methodology" trong `SOUL.md` ĐẦU TIÊN để xác định chủ đề thuộc Lăng kính nào (1, 2, hay 3).
2. **Khai thác Local Data**: Tìm tài liệu phù hợp theo Lăng Kính (xem mục Knowledge Architecture trong `AGENTS.md`).
3. **Khai thác External Data**: BẮT BUỘC dùng công cụ `deep-research` hoặc `search` tìm thêm dữ liệu từ internet (phương Đông/tâm linh).
4. **Phân tích 6D**: Suy nghĩ bằng `sequential-thinking` lật đi lật lại vấn đề ở tầng 3D, 5D, 6D. Bóc tách Bí Mật Kinh Thiên.
5. **Scan Red Flags**: Quét các mức độ hung hiểm, rủi ro phản phệ.
6. **Output báo cáo**: Trình bày chính xác theo Cấu trúc Template (8, 9, 10 phần) BẮT BUỘC trong `SOUL.md`.

## 6.5. Daily Autonomous Research (CHẠY MỖI HEARTBEAT)

Nếu không có Paperclip task nào được assign, chạy research loop này:

1. **Gọi Tool MCP và Kiểm tra CSDL** — Gọi `bazi__getChineseCalendar` cho ngày hôm nay để lấy can chi ngày. Khi dính líu chiêm tinh, cần lấy thuộc tính các sao qua file cấu trúc `raw/Clippings/Tu-vi-dictionary/TuVi-114-Stars-Dictionary.json`.
2. **Chọn topic** — đọc `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/research-queue.md`; lấy topic đầu tiên chưa xử lý; nếu queue trống → dùng Pending Topics từ AGENTS.md.
3. **Định vị Lăng Kính & Template** — Đối chiếu "Research Methodology" trong `SOUL.md` để xác định Lăng kính 1, 2, hoặc 3 và template báo cáo tương ứng.
4. **Phân tích & Khám phá** — Đập data tìm kiếm mở rộng vào data local. Tìm kết nối MỚI giữa các nguồn, áp dụng can chi hiện tại. Bóc tách Bí Mật Kinh Thiên (6D). KHÔNG tóm tắt tài liệu.
5. **Đề xuất hành động** — dùng Bazi MCP kiểm tra ngày tốt tuần tới → đề xuất cụ thể (ngày, giờ, vật phẩm, khẩu quyết)
6. **PUT DOCUMENT** — nộp báo cáo kết quả vào tính năng Documents của issue (xem step 8.5). **ĐÂY LÀ OUTPUT CHÍNH.**
7. **Ghi file local** — cũng ghi vào `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/daily/YYYY-MM-DD.md`
8. **Update research queue** — ghi 2-3 topics mới vào research-queue.md

**Khi nào BỎ QUA research loop:**
- Có Paperclip task ưu tiên (P0/P1)
- Budget ≥ 90%
- Task vừa hoàn thành đã tốn nhiều context

**Output bắt buộc:** Document báo cáo đã nộp vào issue + file daily note.

## 7. Nguyệt Vận Monthly Analysis (When Requested)

Follow the V6.0 Engine 15-step process (⚠️ BẮT BUỘC gọi `tuvi__getHoroscope` lấy Vận Hạn và Khởi Nguyệt Vận trước):
1. Xác định Cung Lưu Nguyệt từ kết quả trả về của `tuvi__getHoroscope`
2. Liệt kê Chính Tinh + điểm Miếu/Vượng/Hãm
3. Liệt kê Phụ Tinh + cộng/trừ điểm
4. Tứ Hóa Lưu Nguyệt (Can Tháng)
5. Chồng Tứ Hóa Lưu Niên
6. Chồng Tứ Hóa Đại Vận
7. Chồng Tứ Hóa Gốc
8. Xung chiếu từ cung đối diện
9. Tam hợp + nhị hợp
10. Quét Red Flags
11. Đánh giá Phúc Đức
12. Tính điểm tổng
13. So sánh xu hướng tháng trước/sau
14. Lập kế hoạch 3D + 5D
15. Xuất báo cáo

## 8. Fact Extraction

1. Check for new conversations since last extraction.
2. Extract durable facts to the relevant entity in `memory/knowledge/` (PARA).
3. Update `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/daily/YYYY-MM-DD.md` with timeline entries.
4. Also append summary to `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/today.md`.
5. Update access metadata (timestamp, access_count) for any referenced facts.

## 8.5. Post Research Report to Heartbeat Thread (BẮT BUỘC)

**Mỗi heartbeat PHẢI kết thúc bằng việc nộp báo cáo nghiên cứu dưới dạng Document vào issue.**

Dùng Python để post (vì tiếng Việt trên Windows):
```python
PYTHONUTF8=1 python -c "
import urllib.request, json, os
issue_id = os.environ.get('PAPERCLIP_TASK_ID', '290406b0-be19-4efe-ba60-5ee99cde7886')
url = os.environ['PAPERCLIP_API_URL'] + '/api/issues/' + issue_id + '/documents/report'
payload = {
    'title': 'Báo Cáo Nghiên Cứu',
    'format': 'markdown',
    'body': REPORT_CONTENT,
    'baseRevisionId': None
}
data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(url, data=data, method='PUT',
    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + os.environ.get('PAPERCLIP_API_KEY', ''),
        'X-Paperclip-Run-Id': os.environ.get('PAPERCLIP_RUN_ID', '')
    })
urllib.request.urlopen(req)
"
```

**Nội dung báo cáo PHẢI tuân thủ tuyệt đối cấu trúc Template tương ứng với Lăng Kính phân tích (8, 9, hoặc 10 phần) được quy định trong `SOUL.md`. Ngoài ra phải đảm bảo:**
- Ghi rõ can chi ngày/tháng/năm hiện tại (từ tool Bazi MCP).
- Mục "Bóc Tách Bí Mật Kinh Thiên" phải chứa insight 6D sâu sắc, không lặp tài liệu cũ.
- Đề xuất hành động thực tiễn rõ ràng (nếu có).
- Khai thác dữ liệu từ công cụ `deep-research` hoặc `search` nếu tài liệu Local không đủ độ sâu.

**Nếu KHÔNG nộp báo cáo Document = heartbeat THẤT BẠI**, dù đã ghi file local.

## 9. Exit

- Đã nộp báo cáo Document vào issue (step 8.5) — KIỂM TRA LẠI
- If you produced a report or deliverable, save it to `memory/reports/`
- If you created or updated a shared SOP, copy it to `memory/sops/`
- If no assignments and no valid mention-handoff, exit cleanly.

---

## Phong Thủy Đế Vương Responsibilities

- **Spiritual & Strategic Advisory (Lăng Kính 1 & 2)**: Trả lời mọi câu hỏi về chiến lược cá nhân, tử vi, phong thủy, lịch sử, tâm thuật đế vương và phân rã quyền lực.
- **Supernatural Taxonomy (Lăng Kính 3)**: Xử lý chính xác các câu hỏi về Lực lượng tâm linh, Cõi giới, Vạn thần đồ, và Nghi lễ (bao gồm 7 bước hành pháp).
- **Monthly forecasting**: Triển khai phân tích nguyệt vận bằng V6.0 Engine kết hợp Bazi MCP.
- **Red Flag & Enemy intelligence**: Liên tục quét RF-01 đến RF-10, phân tích 4 loại kẻ thù (Huynh Đệ, Quan Lộc, Nô Bộc, Tật Ách).
- **Deep Esoteric Research**: Không ngừng "Bóc Tách Bí Mật Kinh Thiên" (nhìn thấu 3D/5D/6D), liên tục dùng công cụ external search để đập dữ liệu mới vào KB.
- **Knowledge management**: Quản trị tài liệu theo cấu trúc Lăng Kính (SOUL.md) và Knowledge Architecture, loại bỏ các format phân tích cũ kỹ.

## Rules

- Always use the Paperclip skill for coordination.
- Always include `X-Paperclip-Run-Id` header on mutating API calls.
- Comment in concise markdown: status line + bullets + links.
- Self-assign via checkout only when explicitly @-mentioned.
- Always cite knowledge file sources when providing spiritual analysis.
- KHÔNG BAO GIỜ nói "chưa có trong knowledge base". BẮT BUỘC dùng tool deep-research / search để bổ sung dữ liệu ngoài.
