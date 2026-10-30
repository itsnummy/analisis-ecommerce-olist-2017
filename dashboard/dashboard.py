from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Dashboard Analisis E-Commerce 2017")
st.caption(
    "Analisis pesanan delivered Januari–Desember 2017 "
    "| GMV = total harga produk tanpa ongkos kirim"
)

# =========================
# LOAD DATA
# =========================
DATA_FILE = Path(__file__).resolve().parent / "main_data.csv"

if not DATA_FILE.exists():
    st.error("File main_data.csv tidak ditemukan di folder dashboard.")
    st.stop()

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["purchase_datetime"])
    df["month"] = df["month"].astype(str)
    df["category"] = df["category"].fillna("Unknown")
    return df

df = load_data(DATA_FILE)

# =========================
# SIDEBAR FILTER
# =========================
with st.sidebar:
    st.header("Filter")

    month_options = sorted(df["month"].unique())
    selected_months = st.multiselect(
        "Pilih Bulan",
        options=month_options,
        default=month_options
    )

    category_options = sorted(df["category"].unique())
    selected_categories = st.multiselect(
        "Pilih Kategori",
        options=category_options,
        default=[]
    )

    top_n = st.slider(
        "Jumlah Kategori Teratas",
        min_value=5,
        max_value=20,
        value=10
    )

filtered_df = df[df["month"].isin(selected_months)].copy()

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]

if filtered_df.empty:
    st.warning("Tidak ada data berdasarkan filter yang dipilih.")
    st.stop()

# =========================
# KPI
# =========================
gmv = filtered_df["price"].sum()
total_orders = filtered_df["order_id"].nunique()
total_items = filtered_df.shape[0]
avg_order_value = gmv / total_orders if total_orders else 0

st.subheader("Ringkasan Kinerja")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total GMV", f"BRL {gmv:,.2f}")
col2.metric("Total Pesanan", f"{total_orders:,}")
col3.metric("Total Item", f"{total_items:,}")
col4.metric("GMV per Pesanan", f"BRL {avg_order_value:,.2f}")

# =========================
# BUSINESS QUESTION 1
# =========================
st.divider()
st.header("Pertanyaan Bisnis 1")
st.write(
    "Bagaimana perubahan bulanan nilai penjualan produk "
    "(GMV) dan jumlah pesanan delivered sepanjang tahun 2017?"
)

monthly = (
    filtered_df.groupby("month", as_index=False)
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
        labels={"month": "Bulan", "gmv": "GMV (BRL)"}
    )
    fig_gmv.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_gmv, use_container_width=True)

with col_right:
    fig_orders = px.bar(
        monthly,
        x="month",
        y="orders",
        title="Jumlah Pesanan Bulanan",
        labels={"month": "Bulan", "orders": "Jumlah Pesanan"}
    )
    fig_orders.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_orders, use_container_width=True)

st.dataframe(monthly, use_container_width=True, hide_index=True)

# =========================
# BUSINESS QUESTION 2
# =========================
st.divider()
st.header("Pertanyaan Bisnis 2")
st.write(
    "Kategori produk apa yang memberikan kontribusi GMV terbesar "
    "dan bagaimana rata-rata skor ulasannya?"
)

category_summary = (
    filtered_df.groupby("category", as_index=False)
    .agg(
        gmv=("price", "sum"),
        items=("order_item_id", "size"),
        orders=("order_id", "nunique")
    )
    .sort_values("gmv", ascending=False)
)

category_summary["share_pct"] = (
    category_summary["gmv"] / category_summary["gmv"].sum() * 100
)

reviews = (
    filtered_df[["order_id", "category", "review_score"]]
    .drop_duplicates(["order_id", "category"])
    .groupby("category", as_index=False)
    .agg(avg_review=("review_score", "mean"))
)

category_summary = category_summary.merge(
    reviews,
    on="category",
    how="left"
)

top_categories = category_summary.head(top_n)

col_left, col_right = st.columns(2)

with col_left:
    fig_cat = px.bar(
        top_categories.sort_values("gmv"),
        x="gmv",
        y="category",
        orientation="h",
        title="Kategori dengan GMV Tertinggi",
        labels={"gmv": "GMV (BRL)", "category": "Kategori"}
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_right:
    fig_review = px.bar(
        top_categories.sort_values("avg_review"),
        x="avg_review",
        y="category",
        orientation="h",
        title="Rata-rata Skor Ulasan",
        labels={"avg_review": "Skor Ulasan", "category": "Kategori"},
        range_x=[0, 5]
    )
    st.plotly_chart(fig_review, use_container_width=True)

st.dataframe(category_summary, use_container_width=True, hide_index=True)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    label="Unduh Ringkasan Kategori",
    data=category_summary.to_csv(index=False).encode("utf-8"),
    file_name="ringkasan_kategori.csv",
    mime="text/csv"
)

# =========================
# CONCLUSION
# =========================
st.divider()
st.header("Conclusion & Recommendation")

st.markdown("""
### Kesimpulan
- Penjualan cenderung meningkat sepanjang 2017 dan mencapai puncak pada November.
- Kategori dengan GMV tertinggi adalah **bed_bath_table**.
- Kategori **bed_bath_table** memiliki kontribusi penjualan besar, tetapi skor ulasannya relatif lebih rendah dibanding kategori unggulan lainnya.

### Action Items
1. Menyiapkan stok dan promosi menjelang periode penjualan tinggi.
2. Memprioritaskan kategori dengan kontribusi GMV terbesar.
3. Mengevaluasi pengalaman pelanggan pada kategori bed_bath_table.
4. Melakukan monitoring rutin terhadap GMV, pesanan, dan skor ulasan.
""")