from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    max,
    col,
    sum as spark_sum,
    when
)

spark = (
    SparkSession.builder
    .appName("ShockSummary")
    .getOrCreate()
)

# =====================================================
# Load Gold 2
# =====================================================

df = spark.read.parquet(
    "/tmp/output/gold/province_daily_series.parquet"
)

print("Rows:", df.count())

# =====================================================
# Threshold Nasional
# =====================================================

threshold = (
    df
    .select(avg("food_shock"))
    .collect()[0][0]
)

print("National mean shock:", threshold)

# =====================================================
# Summary per Provinsi
# =====================================================

summary = (
    df
    .groupBy("provinsi")
    .agg(
        avg("food_shock").alias(
            "mean_abs_shock"
        ),

        max("food_shock").alias(
            "max_shock"
        ),

        spark_sum(
            when(
                col("food_shock") > threshold,
                1
            ).otherwise(0)
        ).alias(
            "shock_days"
        )
    )
)

summary.write \
    .mode("overwrite") \
    .parquet(
        "/tmp/output/analytics/province_shock_summary.parquet"
    )

summary.orderBy(
    col("mean_abs_shock").desc()
).show(
    20,
    truncate=False
)

print("Shock Summary Selesai")

spark.stop()
