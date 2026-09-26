# Ôn thi Tuyển Giáo viên - Web trắc nghiệm

Ứng dụng web ôn tập trắc nghiệm theo các văn bản tuyển dụng giáo viên, dữ liệu câu hỏi lưu trên **MongoDB Atlas**.

## Tính năng
- **1.020 câu hỏi** (60 câu/đề × 17 mục hiện có): mỗi đề gồm 40 câu ghép kiến thức và 20 câu ghép bổ sung được biên soạn từ các dữ kiện trong mục.
- **Ôn theo từng văn bản** (60 câu/đề). Mục 7 và 8 có tài liệu nguồn nhưng không có sẵn bộ câu hỏi; các câu quiz ở đó được biên soạn từ nội dung/ngân hàng hiện có.
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
| `questions.js` | Ngân hàng câu hỏi nguồn và bộ ghép câu hỏi thử thách |
