from flask import Flask, request, send_file, jsonify
from flask import render_template
from flask_cors import CORS
import pyvips
import os
import tempfile
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

HARD_LIMIT_KB = 800
MIN_TARGET_KB = 30

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


def compress_tight_range(
    input_path,
    output_path,
    target_kb,
    tolerance_kb=2,
    q_min=40,
    q_max=95,
    max_width=2000
):
    image = pyvips.Image.new_from_file(input_path, access="sequential")

    if image.width > max_width:
        image = image.resize(max_width / image.width)

    max_bytes = target_kb * 1024
    min_bytes = max((target_kb - tolerance_kb) * 1024, 1)

    best_under = None
    best_under_size = 0

    for q in range(q_max, q_min - 1, -1):
        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg",
            dir=OUTPUT_DIR
        )
        tmp.close()

        image.jpegsave(
            tmp.name,
            Q=q,
            optimize_coding=True,
            strip=True
        )

        size = os.path.getsize(tmp.name)

        if size > max_bytes:
            os.remove(tmp.name)
            continue

        if min_bytes <= size <= max_bytes:
            os.replace(tmp.name, output_path)
            return True, size

        if size > best_under_size:
            if best_under:
                os.remove(best_under)
            best_under = tmp.name
            best_under_size = size
        else:
            os.remove(tmp.name)

    if best_under:
        os.replace(best_under, output_path)
        return True, best_under_size

    return False, None


@app.route("/compress", methods=["POST"])
def compress():
    try:
        if "image" not in request.files:
            return jsonify({"error": "image missing"}), 400

        file = request.files["image"]

        if not file.filename.lower().endswith((".jpg", ".jpeg")):
            return jsonify({"error": "Only JPG/JPEG supported"}), 400

        target_kb = int(request.form.get("target_kb", 100))
        target_kb = min(max(target_kb, MIN_TARGET_KB), HARD_LIMIT_KB)

        uid = uuid.uuid4().hex
        input_path = os.path.join(UPLOAD_DIR, f"{uid}_{file.filename}")
        output_path = os.path.join(OUTPUT_DIR, f"{uid}_compressed.jpg")

        file.save(input_path)

        ok, size = compress_tight_range(
            input_path=input_path,
            output_path=output_path,
            target_kb=target_kb
        )

        if not ok or not os.path.exists(output_path):
            return jsonify({"error": "compression failed"}), 500

        response = send_file(
            output_path,
            as_attachment=True,
            download_name=f"compressed_{size // 1024}KB.jpg"
        )

        @response.call_on_close
        def cleanup():
            for p in (input_path, output_path):
                if os.path.exists(p):
                    os.remove(p)

        return response

    except Exception as e:
        print("COMPRESS ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
