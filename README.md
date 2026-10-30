
# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis kinerja penjualan dan ulasan pelanggan pada platform E-Commerce Olist selama Januari hingga Desember 2017.

Analisis dilakukan melalui tahapan Data Wrangling, Exploratory Data Analysis (EDA), Visualization & Explanatory Analysis, serta penyusunan kesimpulan dan rekomendasi tindakan.

Hasil analisis disajikan menggunakan dashboard interaktif berbasis Streamlit.

## Pertanyaan Bisnis

1. Selama Januari–Desember 2017, bagaimana perubahan bulanan nilai penjualan produk (GMV, tidak termasuk ongkos kirim) dan jumlah pesanan berstatus delivered, serta bulan mana yang perlu diprioritaskan untuk perencanaan stok dan promosi?

2. Selama Januari–Desember 2017, apa lima kategori produk dengan kontribusi GMV terbesar pada pesanan delivered, berapa persentase kontribusinya, dan bagaimana skor ulasan rata-ratanya untuk menentukan prioritas promosi serta perbaikan pengalaman pelanggan?

## Struktur Direktori

    submission/
    ├── dashboard/
    │   ├── dashboard.py
    │   └── main_data.csv
    ├── data/
    │   ├── orders_dataset.csv
    │   ├── order_items_dataset.csv
    │   ├── products_dataset.csv
    │   ├── order_reviews_dataset.csv
    │   └── product_category_name_translation.csv
    ├── notebook.ipynb
    ├── README.md
    ├── requirements.txt
    └── url.txt

Keterangan:

- dashboard/dashboard.py: kode utama aplikasi Streamlit.
- dashboard/main_data.csv: dataset hasil cleaning yang digunakan oleh dashboard.
- data/: lima dataset sumber untuk analisis.
- notebook.ipynb: dokumentasi seluruh proses analisis data.
- requirements.txt: daftar library Python yang diperlukan.
- url.txt: tautan dashboard yang sudah di-deploy ke Streamlit Cloud.

## Setup Environment

### Prasyarat

Pastikan perangkat sudah memiliki:

- Python versi 3.10 atau lebih baru (disarankan Python 3.11).
- pip untuk instalasi library.
- Terminal, Command Prompt, PowerShell, atau Visual Studio Code.
- Seluruh file proyek telah diunduh dan diekstrak.

### Setup Environment - Windows PowerShell

1. Buka terminal pada folder `submission`.

2. Buat virtual environment:

    py -m venv .venv

3. Aktifkan virtual environment:

    .\.venv\Scripts\Activate.ps1

4. Instal seluruh library dari requirements.txt:

    python -m pip install -r requirements.txt

Jika aktivasi PowerShell diblokir, jalankan instalasi tanpa mengaktifkan virtual environment:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

### Setup Environment - Command Prompt (Windows)

1. Buka Command Prompt pada folder `submission`.

2. Buat virtual environment:

    py -m venv .venv

3. Aktifkan virtual environment:

    .venv\Scripts\activate.bat

4. Instal library:

    python -m pip install -r requirements.txt

### Setup Environment - Linux / macOS

1. Buka terminal pada folder `submission`.

2. Buat virtual environment:

    python3 -m venv .venv

3. Aktifkan environment:

    source .venv/bin/activate

4. Instal library:

    python -m pip install -r requirements.txt

## Menjalankan Dashboard Secara Lokal

Pastikan file `main_data.csv` berada di dalam folder `dashboard/`.

Jalankan perintah berikut dari direktori utama `submission`:

    streamlit run dashboard/dashboard.py

Alternatif jika perintah streamlit tidak dikenali:

    python -m streamlit run dashboard/dashboard.py

Apabila menggunakan PowerShell tanpa aktivasi virtual environment:

    .\.venv\Scripts\python.exe -m streamlit run dashboard/dashboard.py

Setelah berhasil, Streamlit biasanya membuka browser secara otomatis dengan alamat:

http://localhost:8501

Apabila browser tidak terbuka otomatis, salin alamat tersebut ke browser.

Untuk menghentikan dashboard, tekan Ctrl + C pada terminal.

## Menjalankan Notebook Analisis

Notebook dapat dijalankan menggunakan Google Colab atau Jupyter Notebook.

Langkah menjalankan melalui Google Colab:

1. Buka Google Colab.
2. Upload file `notebook.ipynb`.
3. Pastikan lima dataset sumber tersedia sesuai lokasi yang digunakan pada notebook.
4. Jalankan seluruh cell melalui menu Runtime > Run all.
5. Periksa hasil Data Wrangling, EDA, Visualization, dan Conclusion.
6. Simpan notebook setelah seluruh output berhasil ditampilkan.

## Fitur Dashboard

Dashboard memiliki fitur:

1. Filter periode berdasarkan bulan.
2. Filter berdasarkan kategori produk.
3. Ringkasan total GMV, jumlah pesanan, jumlah item, dan GMV per pesanan.
4. Grafik tren GMV bulanan.
5. Grafik jumlah pesanan bulanan.
6. Grafik kategori produk dengan kontribusi GMV terbesar.
7. Grafik rata-rata skor ulasan kategori produk.
8. Tabel ringkasan penjualan.
9. Fitur unduh ringkasan kategori dalam format CSV.

Filter yang dipilih akan memengaruhi KPI, grafik, dan tabel pada dashboard.

## Hasil Analisis

### Pertanyaan Bisnis 1

Hasil analisis menunjukkan bahwa total GMV produk dari pesanan delivered sepanjang 2017 mencapai sekitar 5.962.902,01 BRL dengan 43.428 pesanan.

November merupakan bulan dengan GMV tertinggi, yaitu sekitar 987.765,37 BRL, meningkat 52,37% dibandingkan Oktober.

### Pertanyaan Bisnis 2

Lima kategori dengan kontribusi GMV tertinggi adalah:

1. bed_bath_table
2. watches_gifts
3. health_beauty
4. sports_leisure
5. computers_accessories

Kelima kategori tersebut memberikan kontribusi gabungan sekitar 38,03% dari total GMV.

Kategori bed_bath_table memiliki kontribusi GMV terbesar, tetapi skor ulasan rata-ratanya sekitar 4,01 dari skala 5, relatif lebih rendah dibandingkan kategori unggulan lainnya.

## Recommendation & Action Items

1. Melakukan evaluasi kesiapan persediaan menjelang periode penjualan tinggi berdasarkan pola historis.
2. Memprioritaskan kategori produk dengan kontribusi GMV terbesar dalam perencanaan pemasaran.
3. Mengevaluasi kualitas produk dan pengalaman pelanggan pada kategori bed_bath_table.
4. Memantau tren GMV, jumlah pesanan, dan skor ulasan secara berkala.
5. Meningkatkan kelengkapan informasi kategori produk untuk mendukung akurasi analisis.

## Deployment Dashboard

Dashboard dapat di-deploy melalui Streamlit Community Cloud dengan menghubungkan repository GitHub.

Konfigurasi deployment:

- Repository: itsnummy/analisis-ecommerce-olist-2017
- Branch: main
- Main file path: dashboard/dashboard.py

Alamat dashboard yang berhasil di-deploy dicantumkan pada file `url.txt`.

## Troubleshooting

### File main_data.csv tidak ditemukan

Pastikan struktur direktori berikut tersedia:

    dashboard/
    ├── dashboard.py
    └── main_data.csv

### ModuleNotFoundError

Instal ulang seluruh library:

    python -m pip install -r requirements.txt

### Perintah streamlit tidak dikenali

Gunakan:

    python -m streamlit run dashboard/dashboard.py

### Dashboard tidak menampilkan grafik

Pastikan main_data.csv memiliki kolom:

- order_id
- order_item_id
- purchase_datetime
- month
- category
- price
- freight_value
- review_score

Pastikan juga filter bulan dan kategori tidak menghasilkan dataset kosong.

## Catatan

Dataset yang digunakan merupakan data historis Olist, bukan data transaksi real-time.

GMV dihitung berdasarkan harga produk dan tidak termasuk ongkos kirim.

Skor ulasan diperoleh pada tingkat pesanan dan digunakan untuk analisis deskriptif kategori produk.
