from PIL import Image
from pathlib import Path

DIRS = ["pics", "static/img"]
QUALITY = 80
MAX_PX = 1920  # max width or height

for d in DIRS:
    for p in Path(d).glob("*"):
        if p.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        before = p.stat().st_size
        img = Image.open(p)
        if img.mode in ("RGBA", "P") and p.suffix.lower() in (".jpg", ".jpeg"):
            img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > MAX_PX:
            scale = MAX_PX / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        save_args = {"quality": QUALITY, "optimize": True}
        if p.suffix.lower() == ".png":
            save_args = {"optimize": True, "compress_level": 9}
        img.save(p, **save_args)
        after = p.stat().st_size
        print(f"{p.name}: {before//1024}KB → {after//1024}KB")
