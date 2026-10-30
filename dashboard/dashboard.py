
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

DATA_PATH = Path(__file__).resolve().parent / "main_data.csv"

if not DATA_PATH.exists():
    st.error(
        "File main_data.csv tidak ditemukan. "
        "Pastikan file berada dalam folder dashboard."
    )
    st.stop()


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)

    required = [
        "order_id",
        "order_item_id",
        "month",
        "category",
        "price",
        "review_score"
    ]

    missing = [col for col in required if col not in data.columns]

    if missing:
        raise ValueError(f"Kolom tidak tersedia: {missing}")

    data["month"] = data["month"].astype(str)
    data["category"] = data["category"].fillna("Unknown")
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["review_score"] = pd.to_numeric(
        data["review_score"], errors="coerce"
    )

    return data


try:
    df = load_data(DATA_PATH)
except (ValueError, pd.errors.ParserError) as error:
    st.error(f"Gagal memuat dataset: {error}")
    st.stop()


# ===================================================
# FILTER DATA
# ===================================================

with st.sidebar:
    st.header("Filter Dashboard")

    months = sorted(df["month"].dropna().unique())

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

    st.caption(
        "Seluruh KPI, tabel, dan grafik mengikuti "
        "filter bulan dan kategori yang dipilih."
    )


filtered_df = df[df["month"].isin(selected_months)].copy()

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]

filtered_df = filtered_df.dropna(subset=["price"])

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
# VISUALISASI 1: TREN GMV BULANAN
# ===================================================

st.divider()
st.header("Pertanyaan Bisnis 1")

st.write(
    "Bagaimana perubahan bulanan nilai penjualan produk "
    "(GMV) dan jumlah pesanan delivered sepanjang tahun 2017, "
    "serta bulan mana yang perlu diprioritaskan untuk "
    "perencanaan stok dan promosi?"
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

# Hanya satu grafik untuk pertanyaan bisnis pertama
fig_gmv = px.line(
    monthly,
    x="month",
    y="gmv",
    markers=True,
    title="Tren GMV E-Commerce Olist 2017",
    labels={
        "month": "Bulan",
        "gmv": "GMV (BRL)"
    }
)

fig_gmv.update_traces(
    line=dict(color="#4C78A8", width=3),
    marker=dict(size=8)
)

fig_gmv.update_layout(
    xaxis_tickangle=-45,
    hovermode="x unified",
    height=450
)

st.plotly_chart(fig_gmv, use_container_width=True)

# Insight pertanyaan bisnis 1
peak = monthly.loc[monthly["gmv"].idxmax()]
lowest = monthly.loc[monthly["gmv"].idxmin()]

st.subheader("Insight Pertanyaan Bisnis 1")

st.markdown(
    f"""
1. Nilai GMV tertinggi pada data terfilter terjadi pada
   **{peak['month']}**, sebesar **{peak['gmv']:,.2f} BRL**,
   dengan **{int(peak['orders']):,} pesanan**.

2. Nilai GMV terendah terjadi pada **{lowest['month']}**,
   sebesar **{lowest['gmv']:,.2f} BRL**. Perbedaan ini
   dapat dijadikan pertimbangan dalam perencanaan stok
   dan strategi promosi.
"""
)

st.subheader("Data Penjualan Bulanan")

st.dataframe(
    monthly,
    use_container_width=True,
    hide_index=True
)


# ===================================================
# PERTANYAAN BISNIS 2
# VISUALISASI 2: KATEGORI DAN SKOR ULASAN
# ===================================================

st.divider()
st.header("Pertanyaan Bisnis 2")

st.write(
    "Apa lima kategori produk dengan kontribusi GMV terbesar "
    "pada pesanan delivered sepanjang tahun 2017, "
    "berapa persentase kontribusinya, dan bagaimana "
    "rata-rata skor ulasan pelanggannya?"
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

# Satu pesanan dihitung sekali dalam setiap kategori
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

# Hanya 5 kategori teratas
top_categories = category_summary.head(5).copy()

top_categories["review_label"] = top_categories[
    "avg_review"
].apply(
    lambda x: f"{x:.2f}/5" if pd.notna(x) else "N/A"
)

top_categories["chart_label"] = top_categories.apply(
    lambda row: (
        f"{row['share_pct']:.2f}% | "
        f"Ulasan: {row['review_label']}"
    ),
    axis=1
)

# Hanya satu grafik untuk pertanyaan bisnis kedua
fig_category = px.bar(
    top_categories.sort_values("gmv"),
    x="gmv",
    y="category",
    orientation="h",
    text="chart_label",
    custom_data=[
        "share_pct",
        "avg_review",
        "orders"
    ],
    title="5 Kategori Produk dengan GMV Tertinggi dan Skor Ulasan",
    labels={
        "gmv": "GMV (BRL)",
        "category": "Kategori Produk"
    }
)

fig_category.update_traces(
    marker_color="#4C78A8",
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "GMV: BRL %{x:,.2f}<br>"
        "Kontribusi: %{customdata[0]:.2f}%<br>"
        "Skor Ulasan: %{customdata[1]:.2f}/5<br>"
        "Jumlah Pesanan: %{customdata[2]:,}"
        "<extra></extra>"
    )
)

fig_category.update_layout(
    height=500,
    margin=dict(l=140, r=220, t=80, b=60),
    xaxis_range=[
        0,
        top_categories["gmv"].max() * 1.60
    ],
    showlegend=False
)

st.plotly_chart(fig_category, use_container_width=True)

# Insight pertanyaan bisnis 2
highest = top_categories.iloc[0]
valid_reviews = top_categories.dropna(subset=["avg_review"])

st.subheader("Insight Pertanyaan Bisnis 2")

st.markdown(
    f"""
1. Kategori **{highest['category']}** memiliki
   GMV terbesar, yaitu **{highest['gmv']:,.2f} BRL**
   dengan kontribusi **{highest['share_pct']:.2f}%**
   terhadap total GMV pada data terfilter.
"""
)

if not valid_reviews.empty:
    lowest_review = valid_reviews.loc[
        valid_reviews["avg_review"].idxmin()
    ]

    st.markdown(
        f"""
2. Di antara lima kategori dengan GMV terbesar,
   **{lowest_review['category']}** memiliki
   skor ulasan terendah sebesar
   **{lowest_review['avg_review']:.2f}/5**.
   Kategori ini dapat diprioritaskan untuk evaluasi
   pengalaman pelanggan.
"""
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

- GMV sepanjang tahun 2017 mencapai sekitar
  **5.962.902,01 BRL** dari **43.428 pesanan**.
- November merupakan bulan dengan GMV tertinggi,
  yaitu **987.765,37 BRL**, meningkat **52,37%**
  dibandingkan Oktober.

### Kesimpulan Pertanyaan Bisnis 2

- Lima kategori teratas menyumbang sekitar
  **38,03%** dari total GMV.
- Kategori **bed_bath_table** memiliki GMV terbesar,
  dengan kontribusi **8,23%** dan skor ulasan
  rata-rata sekitar **4,01/5**.

### Recommendation & Action Items

1. Mengoptimalkan persediaan menjelang periode
   penjualan tinggi berdasarkan pola historis.
2. Memprioritaskan promosi pada kategori
   dengan kontribusi GMV terbesar.
3. Mengevaluasi pengalaman pelanggan pada
   kategori bed_bath_table.
4. Memantau GMV, jumlah pesanan, dan skor ulasan
   secara berkala.
""")
else:
    st.markdown("""
### Kesimpulan Berdasarkan Filter

Hasil analisis mengikuti bulan dan kategori yang dipilih.
Lihat insight pada masing-masing visualisasi untuk
mengetahui nilai tertinggi, terendah, dan kategori prioritas.

### Recommendation

Evaluasi kategori dengan kontribusi GMV tinggi
dan skor ulasan relatif rendah pada periode terpilih.
""")
