from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lead, row_number
from pyspark.sql.window import Window

spark = (
    SparkSession.builder
    .appName("LagAnalysis")
    .getOrCreate()
)

# =====================================================
# Load Gold 2
# =====================================================

df = spark.read.parquet(
    "/tmp/output/gold/province_daily_series.parquet"
)

df.cache()

print("Total rows:", df.count())

# =====================================================
# Daftar Provinsi
# =====================================================

provinces = [
    row["provinsi"]
    for row in df.select("provinsi").distinct().collect()
]

print("Provinsi:", provinces)

results = []

# =====================================================
# Hitung Korelasi Lag 0-30 Hari
# =====================================================

for prov in provinces:

    print(f"Processing {prov} ...")

    province_df = (
        df
        .filter(col("provinsi") == prov)
        .orderBy("tanggal")
    )

    window_spec = Window.orderBy("tanggal")

    for lag_day in range(31):

        lagged_df = (
            province_df
            .withColumn(
                "bansos_shifted",
                lead(
                    "bansos_normalized",
                    lag_day
                ).over(window_spec)
            )
        )

        corr_value = lagged_df.stat.corr(
            "food_shock",
            "bansos_shifted"
        )

        if corr_value is None:
            corr_value = 0.0

        results.append(
            (
                prov,
                lag_day,
                float(corr_value)
            )
        )

# =====================================================
# Simpan Semua Lag
# =====================================================

lag_df = spark.createDataFrame(
    results,
    [
        "provinsi",
        "lag_hari",
        "korelasi"
    ]
)

lag_df.write \
    .mode("overwrite") \
    .parquet(
        "/tmp/output/analytics/province_lag_analysis.parquet"
    )

print("Lag analysis saved")

# =====================================================
# Ambil Lag Terbaik Tiap Provinsi
# =====================================================

window_best = (
    Window
    .partitionBy("provinsi")
    .orderBy(
        col("korelasi").desc()
    )
)

optimal_df = (
    lag_df
    .withColumn(
        "rank",
        row_number().over(window_best)
    )
    .filter(
        col("rank") == 1
    )
    .drop("rank")
)

optimal_df.write \
    .mode("overwrite") \
    .parquet(
        "/tmp/output/analytics/province_lag_optimal.parquet"
    )

print("Optimal lag saved")

optimal_df.show(
    20,
    truncate=False
)

print("=================================")
print("Lag Analysis Selesai")
print("=================================")

spark.stop()
