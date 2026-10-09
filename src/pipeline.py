from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def bronze():
    """Ingest raw CSV files and persist an immutable-like Parquet copy."""
    for name in ("customers", "orders"):
        df = pd.read_csv(DATA / "raw" / f"{name}.csv")
        df["_ingested_at"] = pd.Timestamp.now(tz="UTC")
        df.to_parquet(DATA / "bronze" / f"{name}.parquet", index=False)


def silver():
    """Clean, type and deduplicate Bronze data."""
    customers = pd.read_parquet(DATA / "bronze" / "customers.parquet")
    orders = pd.read_parquet(DATA / "bronze" / "orders.parquet")

    customers = customers.drop_duplicates(subset=["customer_id"]).copy()
    customers["name"] = customers["name"].str.strip().str.title()
    customers["city"] = customers["city"].str.strip().str.title()

    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["amount"] = pd.to_numeric(orders["amount"], errors="coerce")
    orders = orders.dropna(subset=["order_id", "customer_id", "order_date", "amount"])
    orders = orders[orders["amount"] >= 0]

    customers.to_parquet(DATA / "silver" / "customers.parquet", index=False)
    orders.to_parquet(DATA / "silver" / "orders.parquet", index=False)


def gold():
    """Build a simple business aggregate ready for BI consumption."""
    customers = pd.read_parquet(DATA / "silver" / "customers.parquet")
    orders = pd.read_parquet(DATA / "silver" / "orders.parquet")

    enriched = orders.merge(customers[["customer_id", "city"]], on="customer_id", how="left")
    sales_by_city = (
        enriched.groupby("city", as_index=False)
        .agg(total_sales=("amount", "sum"), orders=("order_id", "nunique"))
        .sort_values("total_sales", ascending=False)
    )
    sales_by_city.to_parquet(DATA / "gold" / "sales_by_city.parquet", index=False)
    sales_by_city.to_csv(DATA / "gold" / "sales_by_city.csv", index=False)


if __name__ == "__main__":
    bronze()
    silver()
    gold()
    print("Pipeline completed: Bronze -> Silver -> Gold")
