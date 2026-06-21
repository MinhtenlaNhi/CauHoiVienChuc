import os, sys
import fitz  # PyMuPDF

os.makedirs("_txt", exist_ok=True)
files = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]
summary = []
for f in files:
    try:
        doc = fitz.open(f)
        parts = []
        total_chars = 0
        for i, page in enumerate(doc):
            t = page.get_text()
            total_chars += len(t.strip())
            parts.append(f"\n----- PAGE {i+1}/{doc.page_count} -----\n{t}")
        out = "".join(parts)
        safe = "".join(c if (c.isalnum() or c in " -_.") else "_" for c in f)
        with open(os.path.join("_txt", safe + ".txt"), "w", encoding="utf-8") as w:
            w.write(out)
        summary.append((f, doc.page_count, total_chars))
        doc.close()
    except Exception as e:
        summary.append((f, -1, "ERR:" + str(e)))

with open("_summary.txt", "w", encoding="utf-8") as w:
    for s in summary:
        w.write(f"{s[2]}\tchars\t{s[1]}\tpages\t{s[0]}\n")
print("done")
