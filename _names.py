import os
with open("_names.txt", "w", encoding="utf-8") as w:
    for f in os.listdir("."):
        if f.lower().endswith(".pdf"):
            w.write(f + "\n")
print("done")
