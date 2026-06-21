import 'dotenv/config';
import express from 'express';
import { MongoClient } from 'mongodb';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const URI = process.env.MONGODB_URI;
const DB_NAME = process.env.DB_NAME || 'on_thi_giao_vien';
const PORT = process.env.PORT || 3000;

const client = new MongoClient(URI);
let col;

async function connect() {
  await client.connect();
  col = client.db(DB_NAME).collection('questions');
  console.log('Đã kết nối MongoDB Atlas.');
}

const app = express();
app.use(express.json());
app.use(express.static(__dirname));

// Danh sách đề + số câu
app.get('/api/topics', async (req, res) => {
  try {
    const topics = await col.aggregate([
      {
        $group: {
          _id: '$topicIndex',
          code: { $first: '$topicCode' },
          title: { $first: '$topicTitle' },
          desc: { $first: '$topicDesc' },
          count: { $sum: 1 },
        },
      },
      { $sort: { _id: 1 } },
    ]).toArray();
    res.json(topics.map(t => ({
      index: t._id, code: t.code, title: t.title, desc: t.desc, count: t.count,
    })));
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Câu hỏi của 1 đề
app.get('/api/topics/:index/questions', async (req, res) => {
  try {
    const index = Number(req.params.index);
    const qs = await col.find({ topicIndex: index })
      .sort({ qIndex: 1 })
      .project({ _id: 0, q: 1, options: 1, answer: 1, explain: 1 })
      .toArray();
    res.json(qs);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Đề tổng hợp: lấy ngẫu nhiên n câu (mặc định 60) từ TẤT CẢ các file
app.get('/api/exam', async (req, res) => {
  try {
    let n = Number(req.query.n) || 60;
    n = Math.max(1, Math.min(n, 200));
    const qs = await col.aggregate([
      { $sample: { size: n } },
      { $project: { _id: 0, q: 1, options: 1, answer: 1, explain: 1, topicCode: 1 } },
    ]).toArray();
    res.json(qs);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

connect()
  .then(() => app.listen(PORT, () => console.log(`Server chạy tại http://localhost:${PORT}`)))
  .catch(e => { console.error('Không kết nối được MongoDB:', e.message); process.exit(1); });
