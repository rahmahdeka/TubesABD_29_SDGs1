import pandas as pd
import sqlite3

df = pd.read_parquet(
    "/mnt/d/tubes_abd/workspace/output/gold/gold_dataset.parquet"
)

print(df.shape)

conn = sqlite3.connect(
    "/mnt/d/tubes_abd/workspace/output/gold/gold.db"
)

df.to_sql(
    "gold_dataset",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Done")
