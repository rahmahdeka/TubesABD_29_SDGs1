import pandas as pd
from pathlib import Path

TARGET_COMMODITIES = [
    "Beras",
    "Daging Ayam",
    "Daging Sapi",
    "Telur Ayam",
    "Bawang Merah",
    "Bawang Putih",
    "Cabai Merah",
    "Cabai Rawit",
    "Minyak Goreng",
    "Gula Pasir"
]

BASE_DIR = Path("data/pihps")

all_data = []

for province_dir in BASE_DIR.iterdir():

    if not province_dir.is_dir():
        continue

    province = province_dir.name

    for file in province_dir.glob("*.xlsx"):

        if file.name.startswith("~$"):
            continue

        print(f"Processing {file.name}")

        df = pd.read_excel(file)

        df = df[df["Komoditas (Rp)"].isin(TARGET_COMMODITIES)]

        df = df.drop(columns=["No"])

        df_long = df.melt(
            id_vars=["Komoditas (Rp)"],
            var_name="tanggal",
            value_name="harga"
        )

        df_long["provinsi"] = province

        df_long = df_long.rename(
            columns={"Komoditas (Rp)": "komoditas"}
        )

        all_data.append(df_long)

result = pd.concat(all_data, ignore_index=True)

result["harga"] = (
    result["harga"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

result["harga"] = pd.to_numeric(
    result["harga"],
    errors="coerce"
)

result["tanggal"] = pd.to_datetime(
    result["tanggal"],
    dayfirst=True,
    errors="coerce"
)

result = result.dropna(subset=["tanggal"])

result = result.sort_values(
    ["provinsi", "komoditas", "tanggal"]
)

all_groups = []

for (provinsi, komoditas), group in result.groupby(
    ["provinsi", "komoditas"]
):

    full_dates = pd.date_range(
        start=group["tanggal"].min(),
        end=group["tanggal"].max(),
        freq="D"
    )

    group = (
        group.set_index("tanggal")
        .reindex(full_dates)
        .rename_axis("tanggal")
        .reset_index()
    )

    group["provinsi"] = provinsi
    group["komoditas"] = komoditas

    group["harga"] = (
        group["harga"]
        .ffill()
        .bfill()
    )

    all_groups.append(group)

result = pd.concat(all_groups, ignore_index=True)

print("\nShape akhir:")
print(result.shape)

print("\nMissing harga:")
print(result["harga"].isna().sum())

output_dir = Path("workspace/output/silver")
output_dir.mkdir(parents=True, exist_ok=True)

result.to_parquet(
    output_dir / "pihps_silver.parquet",
    index=False
)

print("\nSaved!")
