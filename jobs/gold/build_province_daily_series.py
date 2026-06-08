from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, abs as spark_abs, first

spark = (
    SparkSession.builder
    .appName("ProvinceDailySeries")
    .getOrCreate()
)

gold = spark.read.parquet(
    "/workspace/output/gold/gold_dataset.parquet"
)

province_daily = (
    gold
    .groupBy(
        "tanggal",
        "provinsi"
    )
    .agg(
        avg(
            spark_abs("shock_harga")
        ).alias("food_shock"),

        first(
            "bansos_normalized"
        ).alias("bansos_normalized")
    )
    .orderBy(
        "provinsi",
        "tanggal"
    )
)

province_daily.show(20, truncate=False)

province_daily.write.mode("overwrite").parquet(
    "/workspace/output/gold/province_daily_series.parquet"
)

spark.stop()
