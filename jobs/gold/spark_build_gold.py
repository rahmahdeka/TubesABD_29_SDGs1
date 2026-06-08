from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, lag

# =====================================
# Spark Session
# =====================================
spark = (
    SparkSession.builder
    .appName("BuildGoldDataset")
    .getOrCreate()
)

print("Reading silver datasets...")

# =====================================
# Read Silver
# =====================================
pihps = spark.read.parquet(
    "/workspace/output/silver/pihps_silver.parquet"
)

trends = spark.read.parquet(
    "/workspace/output/silver/google_trends_silver.parquet"
)

print("PIHPS rows:", pihps.count())
print("Trends rows:", trends.count())

# =====================================
# Shock Harga
# =====================================
window_spec = (
    Window
    .partitionBy("provinsi", "komoditas")
    .orderBy("tanggal")
)

pihps = pihps.withColumn(
    "harga_lag",
    lag("harga").over(window_spec)
)

pihps = pihps.withColumn(
    "shock_harga",
    (
        col("harga") - col("harga_lag")
    ) / col("harga_lag")
)

# =====================================
# Join Trends
# =====================================
gold = pihps.join(
    trends.select(
        "tanggal",
        "provinsi",
        "bansos_normalized"
    ),
    on=["tanggal", "provinsi"],
    how="left"
)

gold = gold.drop("harga_lag")

print("Gold rows:", gold.count())

gold.printSchema()

# =====================================
# Save Gold
# =====================================
output_path = "/workspace/output/gold/gold_dataset.parquet"

gold.write.mode("overwrite").parquet(
    output_path
)

print("Saved to:", output_path)

spark.stop()
