import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { MongoClient } from 'mongodb';

const URI = process.env.MONGODB_URI;
const DB_NAME = process.env.DB_NAME || 'on_thi_giao_vien';

if (!URI) {
  console.error('Thiếu MONGODB_URI trong .env');
  process.exit(1);
}

// Nạp dữ liệu gốc + dữ liệu bổ sung
const DATA = [];
const sources = ['./questions.js'];

for (const source of sources) {
  try {
    const code = readFileSync(new URL(source, import.meta.url), 'utf8');
    const win = {};
    new Function('window', code)(win);

    const list = win.QUIZ_DATA || win.QUIZ_EXTRA_DATA || [];
    if (Array.isArray(list) && list.length) {
      DATA.push(...list);
    }
  } catch (err) {
    // Nếu file bổ sung chưa tồn tại, bỏ qua an toàn.
    if (source.endsWith('questions.js')) {
      console.error(`Không đọc được dữ liệu từ ${source}:`, err.message);
      process.exit(1);
    }
  }
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

  if (docs.length) {
    const res = await col.insertMany(docs);
    console.log(`Đã nạp ${res.insertedCount} câu hỏi (${DATA.length} đề).`);
  } else {
    console.log('Không có câu hỏi mới; collection đã được làm trống.');
  }

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
