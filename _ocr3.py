import os, subprocess, shutil
import fitz

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
WORK = r"C:\ocrwork"
TDATA = os.path.join(WORK, "tessdata")
os.makedirs(TDATA, exist_ok=True)
if not os.path.exists(os.path.join(TDATA, "vie.traineddata")):
    shutil.copyfile(os.path.abspath("tessdata/vie.traineddata"),
                    os.path.join(TDATA, "vie.traineddata"))
os.makedirs("_txt", exist_ok=True)

f = "Mục 11- CT 05ctrtu_20120267.pdf"
doc = fitz.open(f)
all_text = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    img_path = os.path.join(WORK, "ct05.png")
    pix.save(img_path)
    out_base = os.path.join(WORK, "ct05out")
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
    print("page", i+1, "done", len(txt), flush=True)
doc.close()
with open(os.path.join("_txt", "OCR_CT05.txt"), "w", encoding="utf-8") as w:
    w.write("".join(all_text))
print("ALL DONE")
