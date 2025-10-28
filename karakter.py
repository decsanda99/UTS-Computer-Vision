import cv2
import numpy as np
import os

# --- Konfigurasi Awal ---
OUTPUT_DIR = "output"
IMG_DIR = "img"
CANVAS_SIZE = (400, 400, 3)  # Tinggi, Lebar, Channel

# Warna (BGR)
WARNA_PUTIH = (255, 255, 255)
WARNA_HITAM = (0, 0, 0)
WARNA_MERAH = (0, 0, 255)
WARNA_ABU = (192, 192, 192)
WARNA_KUNING = (0, 255, 255)
WARNA_BIRU_MUDA = (255, 204, 102)
WARNA_HIJAU = (0, 150, 0)

# Pastikan folder output dan img ada
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

def buat_karakter():
    """
    Langkah 1: Membuat karakter robot sederhana di kanvas putih.
    """
    kanvas = np.full(CANVAS_SIZE, WARNA_PUTIH, dtype=np.uint8)

    # Kepala (abu-abu)
    cv2.rectangle(kanvas, (150, 50), (250, 150), WARNA_ABU, -1)
    cv2.rectangle(kanvas, (150, 50), (250, 150), WARNA_HITAM, 2)

    # Mata (kuning)
    cv2.circle(kanvas, (180, 100), 15, WARNA_KUNING, -1)
    cv2.circle(kanvas, (220, 100), 15, WARNA_KUNING, -1)
    cv2.circle(kanvas, (180, 100), 15, WARNA_HITAM, 2)
    cv2.circle(kanvas, (220, 100), 15, WARNA_HITAM, 2)

    # Mulut
    cv2.line(kanvas, (170, 130), (230, 130), WARNA_HITAM, 3)

    # Badan (merah)
    cv2.rectangle(kanvas, (125, 150), (275, 280), WARNA_MERAH, -1)
    cv2.rectangle(kanvas, (125, 150), (275, 280), WARNA_HITAM, 2)

    # Panel Dada (biru muda)
    cv2.rectangle(kanvas, (160, 170), (240, 210), WARNA_BIRU_MUDA, -1)
    cv2.rectangle(kanvas, (160, 170), (240, 210), WARNA_HITAM, 2)

    # Kaki (hitam)
    cv2.rectangle(kanvas, (140, 280), (180, 350), WARNA_HITAM, -1)
    cv2.rectangle(kanvas, (220, 280), (260, 350), WARNA_HITAM, -1)

    # Tangan (garis merah tebal)
    cv2.line(kanvas, (125, 190), (75, 250), WARNA_MERAH, 20)
    cv2.line(kanvas, (275, 190), (325, 250), WARNA_MERAH, 20)

    # Simpan hasil
    path_karakter = os.path.join(OUTPUT_DIR, "karakter.png")
    cv2.imwrite(path_karakter, kanvas)
    print(f"Gambar karakter disimpan di: {path_karakter}")

    return kanvas

def terapkan_transformasi(img):
    """
    Langkah 2: Menerapkan beberapa transformasi pada gambar karakter.
    """
    (h, w) = img.shape[:2]

    # Translasi
    M_translate = np.float32([[1, 0, 50], [0, 1, 30]])
    translasi = cv2.warpAffine(img, M_translate, (w, h), borderValue=WARNA_PUTIH)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "translasi.png"), translasi)
    print("Hasil translasi disimpan di: output/translasi.png")

    # Rotasi
    pusat = (w // 2, h // 2)
    M_rotate = cv2.getRotationMatrix2D(pusat, 45, 1.0)
    rotasi = cv2.warpAffine(img, M_rotate, (w, h), borderValue=WARNA_PUTIH)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "rotate.png"), rotasi)
    print("Hasil rotasi disimpan di: output/rotate.png")

    # Resize
    resize = cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "resize.png"), resize)
    print("Hasil resize disimpan di: output/resize.png")

    # Crop
    crop = img[50:220, 125:275]
    cv2.imwrite(os.path.join(OUTPUT_DIR, "crop.png"), crop)
    print("Hasil crop disimpan di: output/crop.png")

def terapkan_operasi(img_karakter):
    """
    Langkah 3: Menerapkan operasi bitwise/arithmetic.
    """
    (h, w) = img_karakter.shape[:2]

    # Buat background
    background = np.full(CANVAS_SIZE, (255, 200, 100), dtype=np.uint8)
    cv2.rectangle(background, (0, 250), (w, h), WARNA_HIJAU, -1)
    path_bg = os.path.join(IMG_DIR, "background.jpg")
    cv2.imwrite(path_bg, background)
    print(f"Gambar background disimpan di: {path_bg}")

    # Buat mask
    img_gray = cv2.cvtColor(img_karakter, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img_gray, 254, 255, cv2.THRESH_BINARY_INV)
    path_mask = os.path.join(OUTPUT_DIR, "bitwise.png")
    cv2.imwrite(path_mask, mask)
    print(f"Hasil mask disimpan di: {path_mask}")

    # Inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Lubangi background
    bg_terlubangi = cv2.bitwise_and(background, background, mask=mask_inv)

    # Isolasi karakter
    karakter_terisolasi = cv2.bitwise_and(img_karakter, img_karakter, mask=mask)

    # Gabungkan
    final = cv2.add(bg_terlubangi, karakter_terisolasi)
    path_final = os.path.join(OUTPUT_DIR, "final.png")
    cv2.imwrite(path_final, final)
    print(f"Hasil akhir disimpan di: {path_final}")

def main():
    print("Memulai proses pembuatan gambar...")
    karakter = buat_karakter()
    terapkan_transformasi(karakter)
    terapkan_operasi(karakter)
    print("...Proses selesai! Semua file ada di folder 'output/' dan 'img/'.")

# ✅ Perbaikan utama di sini:
if _name_ == "_main_":
    main()