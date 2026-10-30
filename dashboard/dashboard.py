
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ===================================================
# KONFIGURASI DASHBOARD
# ===================================================

st.set_page_config(
    page_title="Analisis E-Commerce Olist 2017",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Dashboard Analisis E-Commerce Olist 2017")

st.caption(
    "Analisis transaksi delivered Januari–Desember 2017 | "
    "GMV merupakan total harga produk tanpa ongkos kirim."
)


# ===================================================
# LOAD DATA
# ===================================================

DATA_PATH = (
    Path(__file__).resolve().parent / "main_data.csv"
)

if not DATA_PATH.exists():
    st.error(
        "File main_data.csv tidak ditemukan. "
        "Pastikan file berada dalam folder dashboard."
    )
    st.stop()


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(
        file_path,
        parse_dates=["purchase_datetime"]
    )

    data["month"] = data["month"].astype(str)
    data["category"] = data["category"].fillna("Unknown")

    return data


df = load_data(DATA_PATH)


# ===================================================
# FILTER DATA
# ===================================================

with st.sidebar:
    st.header("Filter Dashboard")

    months = sorted(df["month"].unique())

    selected_months = st.multiselect(
        "Pilih Bulan",
        options=months,
        default=months
    )

    categories = sorted(df["category"].unique())

    selected_categories = st.multiselect(
        "Pilih Kategori Produk",
        options=categories,
        default=[],
        help="Kosongkan untuk menampilkan semua kategori."
    )

    top_n = st.slider(
        "Jumlah Kategori Teratas",
        min_value=5,
        max_value=20,
        value=10
    )

    st.caption(
        "Seluruh KPI, tabel, dan grafik mengikuti "
        "filter bulan dan kategori yang dipilih."
    )


filtered_df = df[
    df["month"].isin(selected_months)
].copy()

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]

if filtered_df.empty:
    st.warning("Tidak ada data berdasarkan filter yang dipilih.")
    st.stop()


# ===================================================
# KEY PERFORMANCE INDICATORS (KPI)
# ===================================================

gmv = filtered_df["price"].sum()
total_orders = filtered_df["order_id"].nunique()
total_items = len(filtered_df)

avg_order_value = (
    gmv / total_orders if total_orders > 0 else 0
)

st.subheader("Ringkasan Kinerja Penjualan")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total GMV", f"BRL {gmv:,.2f}")
col2.metric("Total Pesanan", f"{total_orders:,}")
col3.metric("Total Item", f"{total_items:,}")
col4.metric("GMV per Pesanan", f"BRL {avg_order_value:,.2f}")


# ===================================================
# PERTANYAAN BISNIS 1
# TREN PENJUALAN BULANAN
# ===================================================

st.divider()
st.header("Pertanyaan Bisnis 1")

st.write(
    "Bagaimana perubahan bulanan GMV dan jumlah "
    "pesanan delivered sepanjang tahun 2017?"
)

monthly = (
    filtered_df
    .groupby("month", as_index=False)
    .agg(
        gmv=("price", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values("month")
)

col_left, col_right = st.columns(2)

with col_left:
    fig_gmv = px.line(
        monthly,
        x="month",
        y="gmv",
        markers=True,
        title="Tren GMV Bulanan",
        labels={
            "month": "Bulan",
            "gmv": "GMV (BRL)"
        }
    )

    fig_gmv.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_gmv,
        use_container_width=True
    )

with col_right:
    fig_orders = px.bar(
        monthly,
        x="month",
        y="orders",
        title="Jumlah Pesanan Bulanan",
        labels={
            "month": "Bulan",
            "orders": "Jumlah Pesanan"
        }
    )

    st.plotly_chart(
        fig_orders,
        use_container_width=True
    )

st.subheader("Data Penjualan Bulanan")
st.dataframe(
    monthly,
    use_container_width=True,
    hide_index=True
)

peak = monthly.loc[monthly["gmv"].idxmax()]

st.info(
    f"Insight: Bulan dengan GMV tertinggi pada "
    f"data terfilter adalah {peak['month']} "
    f"dengan GMV sebesar BRL {peak['gmv']:,.2f}."
)


# ===================================================
# PERTANYAAN BISNIS 2
# KATEGORI PRODUK DAN ULASAN
# ===================================================

st.divider()
st.header("Pertanyaan Bisnis 2")

st.write(
    "Kategori produk apa yang memiliki kontribusi "
    "GMV terbesar dan bagaimana skor ulasan pelanggan?"
)

category_summary = (
    filtered_df
    .groupby("category", as_index=False)
    .agg(
        gmv=("price", "sum"),
        items=("order_item_id", "size"),
        orders=("order_id", "nunique")
    )
    .sort_values("gmv", ascending=False)
)

category_summary["share_pct"] = (
    category_summary["gmv"]
    / category_summary["gmv"].sum() * 100
)

reviews = (
    filtered_df[
        ["order_id", "category", "review_score"]
    ]
    .drop_duplicates(["order_id", "category"])
    .groupby("category", as_index=False)
    .agg(
        avg_review=("review_score", "mean"),
        reviewed_orders=("review_score", "count")
    )
)

category_summary = category_summary.merge(
    reviews,
    on="category",
    how="left"
)

top_categories = category_summary.head(top_n)

col_left, col_right = st.columns(2)

with col_left:
    fig_category = px.bar(
        top_categories.sort_values("gmv"),
        x="gmv",
        y="category",
        orientation="h",
        title="Kategori dengan GMV Tertinggi",
        labels={
            "gmv": "GMV (BRL)",
            "category": "Kategori Produk"
        }
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col_right:
    fig_review = px.bar(
        top_categories.sort_values("avg_review"),
        x="avg_review",
        y="category",
        orientation="h",
        range_x=[0, 5],
        title="Rata-rata Skor Ulasan",
        labels={
            "avg_review": "Skor Ulasan (1–5)",
            "category": "Kategori Produk"
        }
    )

    st.plotly_chart(
        fig_review,
        use_container_width=True
    )

st.subheader("Ringkasan Kategori Produk")

st.dataframe(
    category_summary,
    use_container_width=True,
    hide_index=True
)


# ===================================================
# DOWNLOAD DATA
# ===================================================

st.download_button(
    label="Unduh Ringkasan Kategori (CSV)",
    data=category_summary.to_csv(
        index=False
    ).encode("utf-8"),
    file_name="ringkasan_kategori_2017.csv",
    mime="text/csv"
)


# ===================================================
# KESIMPULAN DAN REKOMENDASI
# ===================================================

st.divider()
st.header("Conclusion & Recommendation")

is_full_data = (
    set(selected_months) == set(months)
    and not selected_categories
)

if is_full_data:
    st.markdown("""
### Kesimpulan Pertanyaan Bisnis 1

- GMV tahun 2017 mencapai sekitar **5.962.902,01 BRL**.
- November merupakan bulan dengan GMV tertinggi.
- GMV November mencapai **987.765,37 BRL**,
  meningkat **52,37%** dibandingkan Oktober.

### Kesimpulan Pertanyaan Bisnis 2

- Lima kategori teratas menyumbang sekitar
  **38,03%** dari total GMV.
- Kategori **bed_bath_table** memiliki GMV terbesar.
- Skor ulasan kategori bed_bath_table sekitar
  **4,01 dari skala 5**.

### Recommendation & Action Items

1. Mengoptimalkan persediaan menjelang periode
   penjualan tinggi.
2. Memprioritaskan promosi kategori dengan
   kontribusi GMV terbesar.
3. Mengevaluasi pengalaman pelanggan pada
   kategori bed_bath_table.
4. Memantau GMV, jumlah pesanan, dan skor ulasan
   secara berkala.
""")
else:
    st.markdown("""
### Insight Berdasarkan Filter

Grafik dan tabel di atas menunjukkan hasil analisis
berdasarkan bulan serta kategori yang dipilih.

### Recommendation

Evaluasi kategori dengan kontribusi GMV terbesar
dan skor ulasan yang relatif rendah dalam periode
yang sedang dianalisis.
""")

st.caption(
    "Data bersifat historis dan digunakan untuk "
    "analisis deskriptif, bukan prediksi penjualan."
)