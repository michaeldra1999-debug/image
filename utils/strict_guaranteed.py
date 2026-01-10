
from PIL import Image
import tempfile, os

def compress_image_strict_guaranteed(file, target_kb):
    limit = max(target_kb - 1, 1)
    img = Image.open(file).convert("RGB")

    for scale in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]:
        w, h = img.size
        resized = img.resize((int(w * scale), int(h * scale)))
        for quality in range(95, 0, -1):
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            resized.save(tmp.name, "JPEG", quality=quality, optimize=True, progressive=True)
            if os.path.getsize(tmp.name) / 1024 <= limit:
                return tmp.name

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    resized.save(tmp.name, "JPEG", quality=5, optimize=True)
    return tmp.name
