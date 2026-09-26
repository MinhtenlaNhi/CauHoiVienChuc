import json
import os
import re
import subprocess
from pathlib import Path

import fitz


ROOT = Path(__file__).parent
OCR_ROOT = ROOT / ".ocrdata"
TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TOPIC_CODES = {
    "Mục 1- NQ71.pdf": "Mục 1 - NQ71",
    "Mục 10-CTGDPT.pdf": "Mục 10 - CTGDPT",
    "Mục 10- TT20-bgddt.pdf": "Mục 10 - TT20",
    "Mục 10-TT13.pdf": "Mục 10 - TT13",
    "Mục 10-TT17-bgddt.pdf": "Mục 10 - TT17",
    "Mục 11- CT 05ctrtu_20120267.pdf": "Mục 11 - CT 05",
    "Mục 12-45 KHcthd.pdf": "Mục 12 - KH 45",
    "Mục 2- Nghi-quyet-57.pdf": "Mục 2 - NQ57",
    "Mục 3-LVC.pdf": "Mục 3 - LVC",
    "Mục 4-LGD.pdf": "Mục 4 - LGD",
    "Mục 5- NQ 281-cp.signed.pdf": "Mục 5 - NQ281",
    "Mục 6-Thông-tư-30-chuẩn nghề nghiêp-2026-TT-BGDĐT.pdf": "Mục 6 - TT30",
    "Mục 9-QTƯX.pdf": "Mục 9 - QTƯX",
}


def extract_text(pdf_path):
    return "\n".join(page.get_text() for page in fitz.open(pdf_path))


def ocr_text(pdf_path):
    if not Path(TESSERACT).exists():
        return ""
    output = []
    document = fitz.open(pdf_path)
    target_dir = OCR_ROOT / pdf_path.stem
    target_dir.mkdir(parents=True, exist_ok=True)
    for page_index, page in enumerate(document):
        image_path = target_dir / f"page_{page_index + 1:02d}.png"
        text_path = target_dir / f"page_{page_index + 1:02d}.txt"
        if text_path.exists():
            output.append(text_path.read_text(encoding="utf-8"))
            continue
        page.get_pixmap(dpi=200).save(image_path)
        subprocess.run(
            [TESSERACT, str(image_path), str(target_dir / f"page_{page_index + 1:02d}"), "-l", "vie", "--psm", "6"],
            capture_output=True,
            check=False,
        )
        generated = target_dir / f"page_{page_index + 1:02d}.txt"
        output.append(generated.read_text(encoding="utf-8") if generated.exists() else "")
    return "\n".join(output)


def parse_questions(text):
    matches = list(re.finditer(r"(?mi)^\s*Câu\s+(\d+)\s*:", text))
    questions = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = re.sub(r"\s+", " ", text[match.end():end]).strip()
        question_end = block.find("?")
        if question_end < 0:
            continue
        question = block[: question_end + 1].strip()
        answer = block[question_end + 1 :].strip(" -:;")
        if len(question) < 20 or len(answer) < 20:
            continue
        questions.append((int(match.group(1)), question, answer))
    return questions


def summarize_answer(answer, limit=260):
    answer = re.sub(r"\s+", " ", answer).strip(" -:;")
    answer = re.sub(r"(?:\*\s*)?(?:Mục tiêu giáo dục|Tính chất, nguyên lý giáo dục)\s*", "", answer)
    parts = [part.strip(" -;,.:") for part in re.split(r"\s+-\s+|;\s+", answer) if part.strip()]
    summary = "; ".join(parts[:3])
    if len(summary) <= limit:
        return summary
    shortened = summary[:limit].rsplit(" ", 1)[0].rstrip(";,.:")
    return shortened + "..."


def make_options(answer, pool):
    answer = summarize_answer(answer)
    distractors = [item for item in pool if item != answer]
    options = [answer, *[summarize_answer(item) for item in distractors[:3]]]
    while len(options) < 4:
        options.append("Nội dung này không được quy định trong văn bản.")
    return options


def js_string(value):
    return json.dumps(value, ensure_ascii=False)


def main():
    topics = {}
    for file_name, topic_code in TOPIC_CODES.items():
        pdf_path = ROOT / file_name
        if not pdf_path.exists():
            continue
        text = extract_text(pdf_path)
        questions = parse_questions(text)
        if not questions:
            questions = parse_questions(ocr_text(pdf_path))
        if not questions:
            continue
        answers = [summarize_answer(answer) for _, _, answer in questions]
        imported = []
        for number, question, answer in questions:
            options = make_options(summarize_answer(answer), answers)
            imported.append({
                "q": question,
                "options": options,
                "answer": 0,
                "explain": f"Đáp án tham khảo được trích từ phần Câu {number} trong tài liệu PDF.",
            })
        topics[topic_code] = imported
        print(f"{topic_code}: {len(imported)} câu")

    marker = "\n// BEGIN PDF SOURCE QUESTIONS\n"
    end_marker = "\n// END PDF SOURCE QUESTIONS\n"
    questions_path = ROOT / "questions.js"
    source = questions_path.read_text(encoding="utf-8")
    if marker in source:
        source = source[: source.index(marker)] + "\n"
    payload = json.dumps(topics, ensure_ascii=False, indent=2)
    addition = f"{marker}const PDF_SOURCE_QUESTIONS = {payload};\n"
    addition += "window.QUIZ_DATA.forEach(topic => {\n"
    addition += "  const imported = PDF_SOURCE_QUESTIONS[topic.code] || [];\n"
    addition += "  topic.questions.push(...imported);\n"
    addition += "});\n"
    addition += "// END PDF SOURCE QUESTIONS\n"
    questions_path.write_text(source.rstrip() + addition, encoding="utf-8")
    print("TOTAL", sum(len(items) for items in topics.values()))


if __name__ == "__main__":
    main()