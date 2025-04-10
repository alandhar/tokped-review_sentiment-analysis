# Tokopedia Product Review Sentiment Analysis

Proyek ini bertujuan untuk membangun sistem **analisis sentimen otomatis** terhadap **ulasan produk Tokopedia**. Sistem terdiri dari dua tahap utama:

1. **Web Scraping Review Produk Tokopedia**
2. **Fine-tuning Model Deep Learning untuk Klasifikasi Sentimen**

---

## Tujuan Proyek

- Mengumpulkan data ulasan produk dari Tokopedia secara otomatis.
- Melabeli sentimen secara otomatis berdasarkan konteks kalimat.
- Membangun sistem klasifikasi sentimen berbasis **transformer** untuk Bahasa Indonesia.
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

## Labeling Sentimen Berbasis BERT

Sistem ini melakukan **analisis konteks teks review** untuk memberikan label sentimen yang lebih kontekstual dan akurat.

### Model yang Digunakan:
- `w11wo/indonesian-roberta-base-sentiment-classifier` dari Huggingface
- Pretrained untuk Bahasa Indonesia, mendukung output: `positive`, `neutral`, `negative`

---

## Modeling (IndoBERT Fine-tuning)

- Model: `indobenchmark/indobert-base-p1`
- Framework: Huggingface Transformers + PyTorch
- Teknik:
  - Oversampling untuk mengatasi data imbalance
  - Tokenisasi & encoding teks
  - Fine-tuning dengan `Trainer API`
- Hasil:
  - Akurasi: > 93%
  - F1-score: > 93%

---

## Prediksi Review Baru

Model dapat memprediksi sentimen dari review baru secara otomatis menggunakan pipeline prediksi.

Contoh:
```python
"Packing bagus, produk sesuai. Recommended banget!"
Sentimen: Positif
```