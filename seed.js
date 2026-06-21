import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { MongoClient } from 'mongodb';

const URI = process.env.MONGODB_URI;
const DB_NAME = process.env.DB_NAME || 'on_thi_giao_vien';

if (!URI) {
  console.error('Thiếu MONGODB_URI trong .env');
  process.exit(1);
}

// Nạp questions.js (file dùng window.QUIZ_DATA = [...])
const code = readFileSync(new URL('./questions.js', import.meta.url), 'utf8');
const win = {};
new Function('window', code)(win);
const DATA = win.QUIZ_DATA || [];

if (!DATA.length) {
  console.error('Không đọc được dữ liệu từ questions.js');
  process.exit(1);
}

// Làm phẳng thành các document câu hỏi
const docs = [];
DATA.forEach((topic, ti) => {
  topic.questions.forEach((q, qi) => {
    docs.push({
      topicIndex: ti,
      topicCode: topic.code || `Đề ${ti + 1}`,
      topicTitle: topic.title || `Đề ${ti + 1}`,
      topicDesc: topic.desc || '',
      qIndex: qi,
      q: q.q,
      options: q.options,
      answer: q.answer,
      explain: q.explain || '',
    });
  });
});

const client = new MongoClient(URI);

try {
  await client.connect();
  console.log('Đã kết nối MongoDB Atlas.');
  const db = client.db(DB_NAME);
  const col = db.collection('questions');

  await col.deleteMany({});
  console.log('Đã xóa dữ liệu cũ trong collection "questions".');

  const res = await col.insertMany(docs);
  console.log(`Đã nạp ${res.insertedCount} câu hỏi (${DATA.length} đề).`);

  // Index hỗ trợ truy vấn theo đề
  await col.createIndex({ topicIndex: 1, qIndex: 1 });
  console.log('Đã tạo index.');

  // Thống kê
  const stats = await col.aggregate([
    { $group: { _id: '$topicCode', title: { $first: '$topicTitle' }, n: { $sum: 1 } } },
    { $sort: { _id: 1 } },
  ]).toArray();
  console.log('--- Thống kê theo đề ---');
  stats.forEach(s => console.log(`${s._id}: ${s.n} câu`));
} catch (e) {
  console.error('LỖI:', e.message);
  process.exit(1);
} finally {
  await client.close();
}
