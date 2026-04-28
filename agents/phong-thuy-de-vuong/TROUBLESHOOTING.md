# TROUBLESHOOTING.md — Agent

> **Đọc file này ĐẦU MỖI HEARTBEAT** trước khi bắt đầu làm việc.
> Ghi thêm entry mỗi khi gặp và fix lỗi mới. Không xóa entry cũ — chỉ thêm.

---

## Cách ghi entry mới

```markdown
## YYYY-MM-DD — [Mô tả lỗi ngắn]

**Triệu chứng**: [Agent thấy gì / lỗi nào]
**Nguyên nhân gốc**: [Root cause]
**Fix**: [Cách fix]
**Tránh lại**: [Rule để không lặp lại]
```

---

<!-- Thêm entries mới bên dưới, mới nhất lên đầu -->

## 2026-04-24 — Quy tắc về File Báo cáo

**Vấn đề**: Các file báo cáo (`report*.md`) được tạo ra ở thư mục gốc, gây bừa bộn và khó quản lý.
**Giải pháp**: Tất cả các file báo cáo, đặc biệt là các báo cáo nghiên cứu tự chủ hoặc theo nhiệm vụ, phải được lưu trữ trong thư mục `C:/Users/Jennie Chu/Desktop/Projects/crypto-pattern-scanner/memory/agents/phong-thuy-de-vuong/daily/`.
**Quy tắc đặt tên**: `YYYY-MM-DD-topic-name-task-id.md`.
    - `YYYY-MM-DD`: Ngày tạo báo cáo.
    - `topic-name`: Chủ đề chính của báo cáo, viết liền không dấu, các từ nối bằng gạch ngang.
    - `task-id`: Mã số task Paperclip (nếu có) hoặc `tu-chu-XX` cho các báo cáo tự nghiên cứu.
**Hành động**: Đã di chuyển tất cả các file báo cáo cũ vào đúng thư mục theo quy tắc mới.

## 2026-04-22 — Lỗi write_todos và execute_sql

**Triệu chứng 1**: Khi gọi tool `write_todos`, bị văng lỗi: `Invalid parameters: Only one task can be "in_progress" at a time.`
**Nguyên nhân gốc 1**: Agent đã truyền vào danh sách todos có tận 2 task mang trạng thái `"in_progress"` cùng lúc.
**Fix 1**: Khi dùng lệnh `write_todos`, BẮT BUỘC chỉ được phép có **tối đa một (1)** todo mang trạng thái `"in_progress"`. Các todo còn lại phải là `"completed"`, `"pending"`, hoặc `"cancelled"`.

**Triệu chứng 2**: Lỗi `Error executing tool mcp_supabase_execute_sql: Error: MCP tool 'execute_sql' reported an error.`
**Nguyên nhân gốc 2**: Tool SQL của Supabase rất nhạy cảm với cú pháp. Thường do Agent viết sai tên bảng, thiếu cột bắt buộc, hoặc truyền string SQL bị sai escape quotes, hoặc thiếu tham số `project_id`.
**Fix 2**: Trước khi chạy `execute_sql`, hãy chạy `list_tables` hoặc check kỹ schema. Đảm bảo truyền đủ `project_id`. Đừng gửi các câu query phức tạp nếu không nắm chắc schema. Mọi câu query SQL cần bọc kỹ string, tránh dùng ký tự lạ gây vỡ JSON.

## 2026-04-22 — Lỗi khi gửi Báo Cáo / Bình Luận (Conflict giữa Comment và Document)

**Triệu chứng**: Agent gửi báo cáo dài vào Endpoint Comment bị cắt xén, hoặc dùng sai field (nhồi vào `body` khi dùng `PATCH`, nhồi sai Endpoint).
**Nguyên nhân gốc**: Agent bị nhầm lẫn giữa các endpoint của Paperclip API khi cần tương tác cập nhật task so với khi cần nộp báo cáo nghiên cứu sâu.

**Tránh lại & Fix cứng (QUY TẮC BẮT BUỘC):**
Để gửi dữ liệu về Paperclip Issue, bạn BẮT BUỘC phân loại độ dài/mục đích của dữ liệu và gọi ĐÚNG endpoint theo quy định trong `SKILL.md`:

1. **COMMENT NGẮN / TRẠNG THÁI TASK (Short Check-in):**
   - Dùng: `POST /api/issues/{issueId}/comments` với payload `{"body": "Nội dung ngắn..."}`
   - Hoặc cập nhật issue kèm comment: `PATCH /api/issues/{issueId}` với payload `{"status": "done", "comment": "Nội dung ngắn..."}`.
   
2. **BÁO CÁO NGHIÊN CỨU DÀI / PHỨC TẠP (Long Report):**
   - TUYỆT ĐỐI KHÔNG dùng Comment. Comment sẽ làm vỡ định dạng và rút gọn nội dung quý giá từ Sequential Thinking.
   - BẮT BUỘC dùng: `PUT /api/issues/{issueId}/documents/report`
   - Payload: `{"title": "Báo Cáo Nghiên Cứu", "format": "markdown", "body": "BÊ NGUYÊN VĂN NỘI DUNG TỪ THOUGHT VÀO ĐÂY", "baseRevisionId": null}`.

**Tuyệt đối tuân thủ** định dạng dữ liệu (field `comment` cho `PATCH`, field `body` cho `POST comment` hoặc `PUT document`) để API không quăng lỗi `405 Method Not Allowed` hoặc bỏ qua dữ liệu.
