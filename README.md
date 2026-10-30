# Proyek Analisis Data E-Commerce 2017

## Deskripsi
Proyek ini bertujuan untuk menganalisis kinerja penjualan dan ulasan pelanggan pada dataset E-Commerce sepanjang tahun 2017

## Pertanyaan Bisnis
1. Bagaimana perubahan bulanan nilai penjualan produk (GMV) dan jumlah pesanan delivered sepanjang 2017?
2. Kategori produk apa yang memberikan kontribusi GMV terbesar dan bagaimana rata-rata skor ulasannya?

## Struktur Folder
```text
submission/
│
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│
├── data/
│   ├── data_1.csv
│   └── data_2.csv
│
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Menjalankan Dashboard
Masuk ke folder `submission`, lalu jalankan:

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Jika perintah `streamlit` tidak dikenali, gunakan:

```bash
python -m streamlit run dashboard/dashboard.py
```

## Insight Utama
- Penjualan tertinggi terjadi pada November 2017.
- Lima kategori produk teratas memberikan kontribusi besar terhadap total GMV.
- Kategori `bed_bath_table` memiliki GMV tertinggi, tetapi skor ulasannya relatif paling rendah di antara lima kategori utama.

## Recommendation
1. Optimalkan stok menjelang periode penjualan tinggi.
2. Fokuskan promosi pada kategori dengan kontribusi GMV besar.
3. Evaluasi kualitas layanan dan pengalaman pelanggan pada kategori `bed_bath_table`.