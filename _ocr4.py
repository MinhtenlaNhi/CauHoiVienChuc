import os, subprocess, shutil
import fitz

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
WORK = r"C:\ocrwork"
TDATA = os.path.join(WORK, "tessdata")
os.makedirs(TDATA, exist_ok=True)
src = os.path.abspath("tessdata/vie.traineddata")
dst = os.path.join(TDATA, "vie.traineddata")
if not os.path.exists(dst):
    shutil.copyfile(src, dst)
os.makedirs("_txt", exist_ok=True)

targets = [
    (r"d:\Downloads\3. Luật viên chức số 129-2025.pdf", "OCR_LVC129.txt"),
    (r"d:\Downloads\4. Luật nhà giáo số 73-2025.pdf", "OCR_LNG73.txt"),
]

for f, outname in targets:
    print("START", outname, flush=True)
    doc = fitz.open(f)
    all_text = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
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
        print("page", i+1, "/", doc.page_count, "chars", len(txt), flush=True)
    doc.close()
    with open(os.path.join("_txt", outname), "w", encoding="utf-8") as w:
        w.write("".join(all_text))
    print("DONE", outname, flush=True)
print("ALL DONE")
