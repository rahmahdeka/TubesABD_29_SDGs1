from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("CommodityCorrelation")
    .getOrCreate()
)

# =====================================================
# Load Gold 1
# =====================================================

df = spark.read.parquet(
    "/workspace/output/gold/gold_dataset.parquet"
)

print("Total rows:", df.count())

# =====================================================
# Daftar Provinsi
# =====================================================

provinces = [
    row["provinsi"]
    for row in df.select("provinsi").distinct().collect()
]

commodities = [
    row["komoditas"]
    for row in df.select("komoditas").distinct().collect()
]

results = []

# =====================================================
# Correlation per Provinsi x Komoditas
# =====================================================

for prov in provinces:

    print(f"Processing province: {prov}")

    for commodity in commodities:

        subset = (
            df
            .filter(col("provinsi") == prov)
            .filter(col("komoditas") == commodity)
        )

        corr_value = subset.stat.corr(
            "shock_harga",
            "bansos_normalized"
        )

        if corr_value is None:
            corr_value = 0.0

        results.append(
            (
                prov,
                commodity,
                float(corr_value)
            )
        )

# =====================================================
# Save Result
# =====================================================

result_df = spark.createDataFrame(
    results,
    [
        "provinsi",
        "komoditas",
        "korelasi"
    ]
)

result_df.write \
    .mode("overwrite") \
    .parquet(
        "/tmp/output/analytics/province_commodity_correlation.parquet"
    )

print("=================================")
print("Commodity Correlation Selesai")
print("=================================")

result_df.orderBy(
    col("korelasi").desc()
).show(
    20,
    truncate=False
)

spark.stop()
