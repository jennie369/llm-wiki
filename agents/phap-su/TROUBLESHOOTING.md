# TROUBLESHOOTING.md — Pháp Sư

## Lỗi thường gặp + cách xử lý

### 1. `mcp_sequential-thinking_sequentialthinking` "MCP tool reported an error"

**Triệu chứng:** Tool crash khi gọi sequentialthinking.

**Root cause:** Sai kiểu dữ liệu (Gemini hay nhầm).

**Fix:**
- `thoughtNumber` + `totalThoughts` = Integer (`1`, `2`), KHÔNG String (`"1"`, `"2"`)
- `nextThoughtNeeded` = Boolean (`true`/`false`), KHÔNG String
- `thought` = String

**Sample đúng:**
```json
{
  "thought": "Đầu tiên ta phân tích...",
  "thoughtNumber": 1,
  "totalThoughts": 5,
  "nextThoughtNeeded": true
}
```

---

### 2. `mcp_deep-research_tavily` empty result hoặc timeout

**Triệu chứng:** Trả về `[]` hoặc timeout sau 30s.

**Root cause:**
- Query quá narrow / quá lạ (vd query Phạn ngữ raw)
- TAVILY_API_KEY hết quota
- Network blip

**Fix:**
- Retry với query rộng hơn (vd thêm 1-2 alternative keywords cùng nghĩa)
- Thử `mcp_deep-research_deep_research` thay vì `tavily` (multi-source synthesis bền hơn)
- Fallback: `mcp_web-fetch_fetch` URL cụ thể nếu biết source primary
- KHÔNG được skip Bước 2 vì lỗi tool — báo cáo sẽ FAIL

---

### 3. `mcp_bazi_*` tool not found

**Triệu chứng:** Gemini báo "tool not available".

**Root cause:** Naming convention. Gemini = single underscore, Claude = double.

**Fix:**
- Gemini: `mcp_bazi_getBaziDetail`, `mcp_bazi_getChineseCalendar`, `mcp_bazi_getSolarTimes`
- Claude: `mcp__bazi__getBaziDetail`, ...
- Verify mcp.json `bazi` block có command `node` + path `bazi_wrapper.mjs` đúng

---

### 4. Báo cáo bị trả về với "RÚT GỌN" warning

**Triệu chứng:** Chủ Tướng feedback "báo cáo nông cạn" hoặc "rác rưởi".

**Root cause:**
- Skip Bước 2 (deep research external)
- Cite nguồn vu vơ ("một số tài liệu cho rằng...") không tên kinh cụ thể
- Bullet rời rạc thay vì đoạn 10-15 câu liên kết logic
- Khẩu quyết viết phiên âm bừa, không có chữ Hán gốc

**Fix:**
- ĐỌC LẠI HEARTBEAT.md mục Bước 7 Audit ngôn ngữ
- Re-run Bước 2 với query Hán-Việt cụ thể
- Cite tên kinh + chương + dòng (vd "Đạo Tạng quyển 17 mục Linh Bảo Phẩm trang 234")
- Compose lại đoạn theo phú ngẫu ngôn từ — hình tượng hóa siêu hình

---

### 5. PersonaHash không invalidate sau khi sửa SOUL.md

**Triệu chứng:** Sửa SOUL.md nhưng heartbeat tick tiếp theo vẫn dùng SOUL cũ.

**Root cause:** BUG-052 đã fix commit `bc94cb84` (codec whitelist). Nếu vẫn xảy ra:
- Server có thể cache personaHash > 1 tick
- Hoặc adapter codec không strip personaHash đúng

**Fix:**
- Restart Paperclip server: `pm2 restart paperclip-server`
- Hoặc đợi 2-3 tick để pickup
- Verify `agent_task_sessions.session_params_json->>'personaHash'` có thay đổi (qua mcp_supabase_execute_sql)

---

### 6. `pc.py` báo "issue not found" hoặc "401 unauthorized"

**Triệu chứng:** `python scripts/pc.py read` fail.

**Root cause:**
- `$PAPERCLIP_ISSUE_IDENTIFIER` không inject (heartbeat scheduled không có issue context)
- `$PAPERCLIP_API_KEY` expire (rare)

**Fix:**
- Verify env: `echo $PAPERCLIP_ISSUE_IDENTIFIER` + `echo $PAPERCLIP_API_KEY` (in heartbeat shell)
- Nếu không có issue context → heartbeat đang chạy theo `wakeOnDemand` không phải comment_wake
  → Pháp Sư TỰ TẠO research issue theo Bước 5 (Tự Giác Sinh Việc) thay vì wait
- Read `.paperclip-spawn-context.json` để debug

---

### 7. File output bị block `.tmp/` permission

**Triệu chứng:** Write tool báo "permission denied" cho `.tmp/<file>.md`.

**Root cause:** Safety system block .tmp/ ngoài UI grant.

**Fix:**
- Default fallback: `memory/reports/YYYY-MM-DD-{slug}.md` (canonical path per AGENTS.md)
- KHÔNG cố ghi `.tmp/` — dùng path approved
- Reference: `agents/phap-su/AGENTS.md` mục File Output Convention

---

### 8. Cross-reference với PTĐV bị conflict

**Triệu chứng:** PTĐV đã viết research về cùng pháp môn, Pháp Sư duplicate.

**Root cause:** Không check shared MEMORY trước khi research.

**Fix:**
- Trước khi nhận task, **đọc `memory/agents/shared/MEMORY.md`** xem PTĐV đã cover chưa
- Nếu PTĐV đã cover → Pháp Sư chỉ ADD góc nhìn pháp thuật (lịch sử pháp môn / cross-civilization), KHÔNG lặp tử vi cá nhân
- Comment trên issue tag `@phong-thuy-de-vuong` để align nếu có overlap
- Save coordination outcome vào `memory/agents/shared/MEMORY.md`

---

### 9. Query Trung văn raw không cho kết quả

**Triệu chứng:** Search "茅山道术" trả về 0 results trên Tavily.

**Root cause:** Tavily index thiên về Anh ngữ.

**Fix:**
- Thử `mcp_web-fetch_fetch` trực tiếp các URL chữ Hán đã biết:
  - https://ctext.org/wiki.pl?if=gb (Chinese Text Project)
  - https://kanripo.org/text/<id> (Kanripo Buddhist canon)
  - https://baike.baidu.com/item/<term>
- Thử query Pinyin: "Mao Shan dao shu" thay raw Hán
- Thử query Hán-Việt: "Mao Sơn đạo thuật"
- Cuối cùng: query song ngữ Trung-Anh "茅山 Mao Shan exorcism techniques"

---

### 10. Khuyến nghị pháp hắc ám bị Chủ Tướng phản ứng

**Triệu chứng:** Pháp Sư recommend dùng Cổ Độc / Kumanthong / Voodoo.

**Root cause:** Vi phạm SOUL.md mục Quỷ Đạo (chỉ liệt kê có cảnh báo, KHÔNG khuyến nghị).

**Fix:**
- TUYỆT ĐỐI không recommend pháp hắc ám
- Chỉ list để Chủ Tướng biết tồn tại + warning rõ ràng
- Nếu Chủ Tướng cần phòng vệ trước hắc ám → recommend pháp môn TRỪ, không phải LUYỆN
- Lesson: re-read SOUL.md Lăng kính 1 mục 7 Action Plan

---

## Cảnh báo Vận Hành

### Khi nào escalate cho Chủ Tướng (Telegram)

- Phát hiện pháp môn Chủ Tướng đang dùng có giới luật vi phạm = phản phệ sắp xảy ra
- Mâu thuẫn cực lớn giữa nguồn cổ và biến tướng hiện đại có khả năng gây hại
- Khám phá kết nối siêu hình bất ngờ với lá số / Đại Vận / Long Mạch của Chủ Tướng
- Pháp môn không kịp research deep trong heartbeat → cần extend time

### Khi nào KHÔNG escalate (tự xử lý)

- Tool error có thể fix qua troubleshooting (mục 1-9 trên)
- Research subtopic minor (defer cho heartbeat sau)
- Conflict với PTĐV về scope (giải qua coordination shared MEMORY)
