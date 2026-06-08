# Analisis Hubungan Shock Harga Pangan dan Pencarian Bantuan Sosial untuk Mendukung SDGs 1 di Sumatera

## Deskripsi Proyek

Proyek ini bertujuan menganalisis hubungan antara gejolak harga pangan (*food price shock*) dan pencarian bantuan sosial menggunakan data harga pangan dari PIHPS dan data pencarian Google Trends pada 10 provinsi di Sumatera selama periode 2021–2026.

Analisis dilakukan menggunakan Apache Spark dengan pendekatan Medallion Architecture (Bronze, Silver, dan Gold Layer) untuk menghasilkan insight yang mendukung pencapaian **SDGs 1 (No Poverty)**.

---

## Tujuan

* Mengukur intensitas shock harga pangan pada setiap provinsi.
* Menganalisis hubungan antara shock harga pangan dan pencarian bantuan sosial.
* Mengidentifikasi lag respons masyarakat terhadap shock harga pangan.
* Menentukan komoditas yang paling berkaitan dengan peningkatan pencarian bantuan sosial.
* Menyajikan hasil analisis dalam bentuk dashboard interaktif.

---

## Teknologi yang Digunakan

* Python
* Apache Spark
* Pandas
* PostgreSQL
* Apache Superset
* Docker
* MinIO

---

## Arsitektur Pipeline

```text
Raw Data (PIHPS + Google Trends)
        ↓
Silver Layer
├── pihps_silver.parquet
└── google_trends_silver.parquet
        ↓
Gold Layer
├── gold_dataset.parquet
└── province_daily_series.parquet
        ↓
Analytics Layer
├── province_lag_analysis.parquet
├── province_lag_optimal.parquet
├── province_commodity_correlation.parquet
└── province_shock_summary.parquet
        ↓
PostgreSQL
        ↓
Apache Superset Dashboard
```

---

## Struktur Repository

```text
Tugas-Besar-Analisis-Big-Data/
│
├── data/
│   ├── pihps/
│   └── google_trends/
│
├──  jobs

│   ├── analytics

│   │   ├── 05_lag_analysis_spark.py

│   │   ├── 06_commodity_correlation_spark.py

│   │   └── 07_shock_summary_spark.py

│   ├── gold

│   │   ├── build_province_daily_series.py

│   │   └── spark_build_gold.py

│   └── silver

│       ├── 01_pihps_to_silver.py

│       └── 02_google_trends_to_silver.py
│
├── output/
│   ├── silver/
│   ├── gold/
│   ├── analytics/
│   └── dashboard/
│
├── docs/
├── jars/
├── minio/
├── superset/
│
├── docker-compose.spark.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Konfigurasi Lingkungan

### 1. Clone Repository

```bash
git clone <repository-url>
cd Tugas-Besar-Analisis-Big-Data
```

### 2. Menjalankan Apache Spark

```bash
docker compose -f docker-compose.spark.yml up -d
```

### 3. Menjalankan MinIO

```bash
docker compose -f minio/docker-compose.minio.yml up -d
```

### 4. Menjalankan Apache Superset

```bash
docker compose -f superset/docker-compose.superset.yml up -d
```

### 5. Dependensi Python

```bash
pip install -r requirements.txt
```

---

## Analisis yang Dilakukan

### Food Price Shock

Mengukur perubahan harga harian menggunakan:

[
Shock_t=\frac{Harga_t-Harga_{t-1}}{Harga_{t-1}}
]

### Lag Analysis

Mengidentifikasi jeda waktu antara shock harga pangan dan peningkatan pencarian bantuan sosial.

### Commodity Correlation

Mengukur hubungan antara shock harga setiap komoditas dan pencarian bantuan sosial.

### Shock Summary

Merangkum tingkat kerentanan harga pangan pada masing-masing provinsi.

---

## Dashboard

Dashboard terdiri atas empat visualisasi utama:

1. Korelasi Shock Harga dan Bantuan Sosial
2. Lag Respons Bantuan Sosial
3. Korelasi Berdasarkan Komoditas
4. Intensitas Shock Harga Pangan

---

## Pembagian Peran Tim

| Nama                            | NIM           | Peran                           | Tanggung Jawab                                                                                            |
| ------------------------------- | ------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Rahmah Gustriana Deka | 123450102     | Data Analyst (Ketua)            | Analisis shock harga, lag analysis, korelasi komoditas, interpretasi hasil, dan penyusunan insight SDGs 1 |
| Gusti Putu Ferazka D.                  | 123450046 | ETL Engineer                    | Implementasi pipeline Bronze, Silver, dan Gold Layer menggunakan Apache Spark                             |
| Hafsa Fazila Arradhi                  | 123450079 | Data Collection Engineer        | Akuisisi, validasi, dan pengelolaan data PIHPS serta Google Trends                                        |
| Eka Fidiya Putri                  | 122450045 | Dashboard & Deployment Engineer | PostgreSQL, Apache Superset, Docker, deployment, dan visualisasi dashboard                                |

---

## SDGs yang Didukung

### SDG 1 – No Poverty (Tanpa Kemiskinan)

Proyek ini memanfaatkan data harga pangan dan perilaku pencarian bantuan sosial untuk mengidentifikasi indikasi kerentanan ekonomi masyarakat akibat gejolak harga pangan serta mendukung pengambilan keputusan berbasis data.

