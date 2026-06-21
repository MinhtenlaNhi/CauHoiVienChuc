import os
import fitz  # PyMuPDF

os.makedirs("_txt", exist_ok=True)
targets = [
    "Mục 6-Thông-tư-30-chuẩn nghề nghiêp-2026-TT-BGDĐT.pdf",
]
for f in targets:
    if not os.path.exists(f):
        print("MISSING", repr(f)); continue
    doc = fitz.open(f)
    parts = []
    total = 0
    for i, page in enumerate(doc):
        t = page.get_text()
        total += len(t.strip())
        parts.append(f"\n----- PAGE {i+1}/{doc.page_count} -----\n{t}")
    safe = "".join(c if (c.isalnum() or c in " -_.") else "_" for c in f)
    with open(os.path.join("_txt", safe + ".txt"), "w", encoding="utf-8") as w:
        w.write("".join(parts))
    print("TEXT", repr(f), "pages", doc.page_count, "chars", total)
    doc.close()
print("done")
