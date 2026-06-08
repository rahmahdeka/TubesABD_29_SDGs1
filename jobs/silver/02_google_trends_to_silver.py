import pandas as pd
from pathlib import Path

BASE_DIR = Path("data/google_trends")

all_data = []

for province_dir in BASE_DIR.iterdir():

    if not province_dir.is_dir():
        continue

    province = province_dir.name

    print(f"\nProcessing province: {province}")

    # =========================
    # Anchor Bulanan
    # =========================
    anchor_file = province_dir / f"anchor_{province}.csv"

    anchor = pd.read_csv(anchor_file)

    anchor.columns = [
        c.strip().replace('"', '')
        for c in anchor.columns
    ]

    anchor["Time"] = pd.to_datetime(anchor["Time"])

    anchor["year_month"] = (
        anchor["Time"]
        .dt.to_period("M")
    )

    anchor = anchor.rename(
        columns={
            "bansos": "anchor_value"
        }
    )

    anchor = anchor[
        ["year_month", "anchor_value"]
    ]

    # =========================
    # Data Harian
    # =========================
    province_daily = []

    for file in province_dir.glob("*.csv"):

        if "anchor" in file.name.lower():
            continue

        print(f"  Reading {file.name}")

        df = pd.read_csv(file)

        # kasus kolom jadi:
        # Time,"bansos"
        if len(df.columns) == 1:

            df = pd.read_csv(
                file,
                names=["tanggal", "bansos"],
                skiprows=1
            )

        else:

            df.columns = [
                c.strip().replace('"', '')
                for c in df.columns
            ]

            df = df.rename(
                columns={
                    "Time": "tanggal",
                    "bansos": "bansos"
                }
            )

        province_daily.append(df)

    daily = pd.concat(
        province_daily,
        ignore_index=True
    )

    daily["tanggal"] = pd.to_datetime(
        daily["tanggal"]
    )

    daily["bansos"] = pd.to_numeric(
        daily["bansos"],
        errors="coerce"
    )

    # =========================
    # Hilangkan overlap tanggal
    # =========================
    daily = (
        daily.groupby("tanggal", as_index=False)
        .agg({"bansos": "mean"})
    )

    daily["year_month"] = (
        daily["tanggal"]
        .dt.to_period("M")
    )

    # =========================
    # Join Anchor
    # =========================
    daily = daily.merge(
        anchor,
        on="year_month",
        how="left"
    )

    # =========================
    # Normalisasi
    # =========================
    daily["bansos_raw"] = daily["bansos"]

    daily["bansos_normalized"] = (
        daily["bansos_raw"]
        * daily["anchor_value"]
        / 100
    )

    daily["provinsi"] = province

    all_data.append(daily)

# =========================
# Gabungkan Semua Provinsi
# =========================
result = pd.concat(
    all_data,
    ignore_index=True
)

result = result[
    [
        "tanggal",
        "year_month",
        "provinsi",
        "bansos_raw",
        "anchor_value",
        "bansos_normalized"
    ]
]

print("\nShape:")
print(result.shape)

print("\nMissing:")
print(result.isna().sum())

print("\nSample:")
print(result.head())

# =========================
# Save Silver
# =========================
output_dir = Path(
    "workspace/output/silver"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

result.to_parquet(
    output_dir / "google_trends_silver.parquet",
    index=False
)

print("\nSaved!")
