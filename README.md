# Ôn thi Tuyển Giáo viên - Web trắc nghiệm

Ứng dụng web ôn tập trắc nghiệm theo các văn bản tuyển dụng giáo viên, dữ liệu câu hỏi lưu trên **MongoDB Atlas**.

## Tính năng
- **520 câu hỏi** (40 câu/đề × 13 văn bản): Luật Giáo dục, Luật Viên chức, CTGDPT (TT32), TT13, TT17, TT20, TT30 (chuẩn nghề nghiệp GV), Quy tắc ứng xử (TT06), NQ57, NQ71, NQ281, KH45 (UBND Hà Nội), CT 05-CTr/TU.
- **Ôn theo từng văn bản** (40 câu/đề).
- **Làm đề tổng hợp**: lấy ngẫu nhiên 30/40/60/90/120 câu từ tất cả văn bản (MongoDB `$sample`).
- Chấm điểm, xem lại bài làm kèm giải thích, trộn câu hỏi.

## Công nghệ
- Backend: Node.js + Express + MongoDB driver
- Frontend: HTML/CSS/JS thuần (fetch API)
- Lưu trữ: MongoDB Atlas

## Cài đặt & chạy
```bash
npm install
```

Tạo file `.env` (KHÔNG commit file này):
```
MONGODB_URI=<connection string MongoDB Atlas của bạn>
DB_NAME=on_thi_giao_vien
PORT=3000
```

Nạp dữ liệu câu hỏi lên MongoDB:
```bash
npm run seed
```

Chạy server:
```bash
npm start
```
Mở trình duyệt tại http://localhost:3000

## Cấu trúc
| File | Vai trò |
|------|---------|
| `index.html` | Giao diện web, lấy dữ liệu qua API |
| `server.js` | Express server + API (`/api/topics`, `/api/topics/:index/questions`, `/api/exam?n=`) |
| `seed.js` | Nạp `questions.js` lên MongoDB |
| `questions.js` | Ngân hàng 520 câu hỏi (nguồn dữ liệu) |
