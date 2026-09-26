# Ôn thi Tuyển Giáo viên - Web trắc nghiệm

Ứng dụng web ôn tập trắc nghiệm theo các văn bản tuyển dụng giáo viên, dữ liệu câu hỏi lưu trên **MongoDB Atlas**.

## Tính năng
- **1.139 câu hỏi** trong 17 mục: mỗi mục có bộ câu ghép kiến thức và các câu hỏi được trích từ phần hỏi - đáp trong PDF nguồn khi tài liệu có phần này.
- **Ôn theo từng văn bản**; các câu hỏi PDF giữ nguyên nội dung câu hỏi và đáp án tham khảo, sau đó được chuyển thành 4 lựa chọn để làm quiz.
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
| `questions.js` | Ngân hàng câu hỏi, câu ghép thử thách và câu hỏi trích từ PDF |
| `extract_pdf_questions.py` | Trích câu hỏi/đáp án từ PDF và OCR các PDF dạng scan |
