# Tokopedia Product Review Sentiment Analysis

Proyek ini bertujuan untuk membangun sistem **analisis sentimen otomatis** terhadap **ulasan produk Tokopedia**. Sistem terdiri dari dua tahap utama:

1. **Web Scraping Review Produk Tokopedia**
2. **Fine-tuning Model Deep Learning untuk Klasifikasi Sentimen**

---

## Tujuan Proyek

- Mengumpulkan data ulasan produk dari Tokopedia secara otomatis.
- Melabeli sentimen secara otomatis berdasarkan rating.
- Melatih model berbasis **IndoBERT** untuk mengklasifikasikan sentimen review menjadi:
  - `positif`
  - `netral`
  - `negatif`

---

## Web Scraping Tokopedia

Scraping dilakukan dalam dua tahap:

### a. `product_scraper.py`
- Input: list keyword
- Output: link produk Tokopedia
- Metode: Selenium + scroll dinamis

### b. `review_scraper.py`
- Input: file `tokopedia_products.csv`
- Output: file `tokopedia_reviews.csv`
- Scraping review berdasarkan rating (1–5) dengan batas tertentu
- Include timestamp, rating, dan isi review

---

## Modeling (IndoBERT Fine-tuning)

- Model: `indobenchmark/indobert-base-p1`
- Framework: Huggingface Transformers + PyTorch
- Teknik:
  - Oversampling untuk mengatasi data imbalance
  - Tokenisasi & encoding teks
  - Fine-tuning dengan `Trainer API`
- Hasil:
  - Akurasi: > 91%
  - F1-score: > 91%

---

## Prediksi Review Baru

Model dapat memprediksi sentimen dari review baru secara otomatis menggunakan pipeline prediksi.

Contoh:
```python
"Packing bagus, produk sesuai. Recommended banget!"
Sentimen: Positif
```