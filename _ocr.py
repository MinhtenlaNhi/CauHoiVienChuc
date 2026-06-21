import os, subprocess, shutil
import fitz

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
WORK = r"C:\ocrwork"
TDATA = os.path.join(WORK, "tessdata")
os.makedirs(TDATA, exist_ok=True)
shutil.copyfile(os.path.abspath("tessdata/vie.traineddata"),
                os.path.join(TDATA, "vie.traineddata"))
os.makedirs("_txt", exist_ok=True)

targets = [
    "Mục 10- TT20-bgddt.pdf",
    "Mục 10-TT13.pdf",
    "Mục 12-45 KHcthd.pdf",
    "Mục 2- Nghi-quyet-57.pdf",
    "Mục 5- NQ 281-cp.signed.pdf",
]

for f in targets:
    if not os.path.exists(f):
        print("MISSING", f); continue
    doc = fitz.open(f)
    all_text = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img_path = os.path.join(WORK, "page.png")
        pix.save(img_path)
        out_base = os.path.join(WORK, "out")
        if os.path.exists(out_base + ".txt"):
            os.remove(out_base + ".txt")
        subprocess.run(
            [TESS, img_path, out_base, "-l", "vie",
             "--tessdata-dir", TDATA, "--psm", "6"],
            capture_output=True, text=True, cwd=WORK
        )
        txt = ""
        if os.path.exists(out_base + ".txt"):
            with open(out_base + ".txt", encoding="utf-8") as r:
                txt = r.read()
        all_text.append(f"\n----- PAGE {i+1}/{doc.page_count} -----\n{txt}")
    doc.close()
    safe = "".join(c if (c.isalnum() or c in " -_.") else "_" for c in f)
    with open(os.path.join("_txt", "OCR_" + safe + ".txt"), "w", encoding="utf-8") as w:
        w.write("".join(all_text))
    print("DONE", f, sum(len(t) for t in all_text))
print("ALL DONE")
