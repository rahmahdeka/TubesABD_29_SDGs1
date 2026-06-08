import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://superset:superset@localhost:5432/superset"
)

datasets = {
    "province_shock_summary":
        "output/analytics/province_shock_summary.parquet",

    "province_lag_optimal":
        "output/analytics/province_lag_optimal.parquet",

    "province_commodity_correlation":
        "output/analytics/province_commodity_correlation.parquet",
}

for table_name, parquet_path in datasets.items():

    print(f"Loading {table_name} ...")

    df = pd.read_parquet(parquet_path)

    print(f"Rows: {len(df)}")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
    )

    print(f"{table_name} uploaded")

print("===================================")
print("SEMUA DATASET ANALYTICS TERUPLOAD")
print("===================================")
