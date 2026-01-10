const dropArea = document.getElementById("dropArea");
const input = document.getElementById("imageFile");
const preview = document.getElementById("preview");
const uploadText = document.getElementById("uploadText");
const customSize = document.getElementById("customSize");

/* =========================
   CLICK TO UPLOAD
========================= */
dropArea.addEventListener("click", () => input.click());

/* =========================
   DRAG & DROP
========================= */
dropArea.addEventListener("dragover", e => {
  e.preventDefault();
  dropArea.classList.add("active");
});

dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
});

dropArea.addEventListener("drop", e => {
  e.preventDefault();
  dropArea.classList.remove("active");

  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    input.files = e.dataTransfer.files;
    showPreview(file);
  }
});

/* =========================
   FILE SELECT
========================= */
input.addEventListener("change", () => {
  if (input.files.length) {
    showPreview(input.files[0]);
  }
});

/* =========================
   PREVIEW
========================= */
function showPreview(file) {
  const reader = new FileReader();
  reader.onload = () => {
    preview.src = reader.result;
    preview.style.display = "block";
    uploadText.style.display = "none";
    dropArea.classList.add("has-image");
  };
  reader.readAsDataURL(file);
}

/* =========================
   AUTO SIZE
========================= */
function autoCompress(size) {
  if (!input.files[0]) {
    alert("Please upload image first");
    return;
  }
  compressAndDownload(size);
}

/* =========================
   CUSTOM SIZE
========================= */
function customCompress() {
  if (!input.files[0]) {
    alert("Please upload image first");
    return;
  }

  let size = parseInt(customSize.value, 10);
  size = Math.min(800, Math.max(10, size));
  customSize.value = size;

  compressAndDownload(size);
}

/* =========================
   BACKEND INTEGRATION ✅
========================= */
async function compressAndDownload(size) {
  const fd = new FormData();

  // ✅ MATCH BACKEND
  fd.append("image", input.files[0]);
  fd.append("target_kb", size);

const API_URL = "/compress";

const res = await fetch(API_URL, {
  method: "POST",
  body: fd
});


  if (!res.ok) {
    alert("Compression failed");
    return;
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `compressed_${size}KB.webp`;
  document.body.appendChild(a);
  a.click();
  a.remove();

  URL.revokeObjectURL(url);
}
