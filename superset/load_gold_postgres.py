import pandas as pd
from sqlalchemy import create_engine

# baca gold
df = pd.read_parquet(
    "/mnt/d/tubes_abd/workspace/output/gold/gold_dataset.parquet"
)

print("Rows:", len(df))

engine = create_engine(
    "postgresql+psycopg2://superset:superset@localhost:5432/superset"
)

df.to_sql(
    "gold_dataset",
    engine,
    if_exists="replace",
    index=False,
    chunksize=5000,
)

print("Upload selesai")
