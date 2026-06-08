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
## Dataset
Kalau dihitung berdasarkan asumsi dataset harian dari **1 Januari 2021 sampai 31 Mei 2026**:

### Jumlah Hari Observasi

```text
2021 = 365 hari
2022 = 365 hari
2023 = 365 hari
2024 = 366 hari (tahun kabisat)
2025 = 365 hari
Jan–Mei 2026 = 151 hari
----------------------
Total = 1.977 hari
```

---

## Google Trends

Cakupan:

* 10 provinsi Sumatera
* Frekuensi harian
* 1 indeks pencarian bantuan sosial

Maka ukuran data mentah:

[
1.977 \times 10 = 19.770
]

≈ **19.770 observasi**

---

## PIHPS

Cakupan:

* 10 provinsi Sumatera
* Frekuensi harian
* 20 komoditas spesifik

Contoh:

```text
Beras Premium
Beras Medium
Bawang Merah
Bawang Putih
Cabai Merah
Cabai Rawit
Minyak Goreng Curah
Minyak Goreng Kemasan
Gula Pasir
Telur Ayam Ras
...
```

Maka ukuran data mentah:

[
1.977 \times 10 \times 20
=========================

395.400
]

≈ **395.400 observasi**

---

## Setelah Agregasi ke 10 Komoditas Utama

Misalnya:

| Komoditas Utama | Komoditas Spesifik        |
| --------------- | ------------------------- |
| Beras           | Beras Kualitas I, II, III |
| Cabai           | Cabai Merah, Cabai Rawit  |
| Minyak Goreng   | Curah, Kemasan            |
| Daging Ayam     | Ras, Kampung              |
| dll             | ...                       |

Maka ukuran data menjadi:

[
1.977 \times 10 \times 10
=========================

197.700
]

≈ **197.700 observasi**

Angka ini sangat dekat dengan hasil Gold Layer milikmu:

```text
197.500 baris
```

Selisih sekitar 200 baris sangat wajar karena ada:

* tanggal yang hilang,
* data kosong,
* hasil join yang tidak lengkap,
* atau proses filtering saat ETL.

---

Untuk README, saya akan menulis:

> Dataset mentah terdiri atas sekitar **19.770 observasi Google Trends** dan **395.400 observasi harga pangan PIHPS** yang mencakup 10 provinsi di Sumatera selama periode Januari 2021–Mei 2026. Data harga pangan mencakup 20 komoditas spesifik yang kemudian dikelompokkan menjadi 10 komoditas utama untuk proses analisis. Setelah integrasi dan transformasi menggunakan Apache Spark, dihasilkan dataset analitik (Gold Layer) berisi sekitar **197 ribu observasi** yang digunakan dalam proses analisis hubungan shock harga pangan dan pencarian bantuan sosial.

Dataset yang digunakan berasal dari dua sumber utama:

### 1. PIHPS (Pusat Informasi Harga Pangan Strategis Nasional)

- Periode: 2021–2026
- Cakupan wilayah: 10 provinsi di Sumatera
- Frekuensi: Harian
- Komoditas: 10 komoditas pangan strategis
- Format: XLSX

### 2. Google Trends

- Periode: 2021–2026
- Cakupan wilayah: 10 provinsi di Sumatera
- Frekuensi: Harian
- Variabel: Indeks pencarian terkait bantuan sosial
- Format: CSV
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

