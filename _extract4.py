import os
import fitz

os.makedirs("_txt", exist_ok=True)
targets = [
    r"d:\Downloads\3. Luật viên chức số 129-2025.pdf",
    r"d:\Downloads\4. Luật nhà giáo số 73-2025.pdf",
    r"d:\Downloads\Mục 8-ĐLTTHCS-THPT.pdf",
    r"d:\Downloads\Mục 7-Thông-tư-31-mã số -2026-TT-BGDĐT.pdf",
]
for f in targets:
    if not os.path.exists(f):
        print("MISSING", f)
        continue
    doc = fitz.open(f)
    parts = []
    total = 0
    for i, page in enumerate(doc):
        t = page.get_text()
        total += len(t.strip())
        parts.append(f"\n----- PAGE {i+1}/{doc.page_count} -----\n{t}")
    name = os.path.basename(f)
    safe = "".join(c if (c.isalnum() or c in " -_.") else "_" for c in name)
    out = os.path.join("_txt", safe + ".txt")
    with open(out, "w", encoding="utf-8") as w:
        w.write("".join(parts))
    print("OK", name, "pages", doc.page_count, "chars", total, "->", out)
    doc.close()
print("done")
