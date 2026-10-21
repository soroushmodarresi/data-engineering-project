
import csv
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "sales.csv"
METADATA_FILE = OUTPUT_DIR / "sales_metadata.json"

sales = [
    {
        "order_id": 1001,
        "customer": "Alice",
        "product": "Laptop",
        "quantity": 1,
        "unit_price": 1200.00,
    },
    {
        "order_id": 1002,
        "customer": "Bob",
        "product": "Mouse",
        "quantity": 2,
        "unit_price": 25.00,
    },
    {
        "order_id": 1003,
        "customer": "Charlie",
        "product": "Keyboard",
        "quantity": 1,
        "unit_price": 75.00,
    },
]


def validate_sales(records):
    """Check that each sales record has valid values."""
    required_fields = {
        "order_id",
        "customer",
        "product",
        "quantity",
        "unit_price",
    }

    seen_order_ids = set()

    for record in records:
        missing = required_fields - record.keys()
        if missing:
            raise ValueError(f"Missing fields: {missing}")

        if not isinstance(record["order_id"], int):
            raise ValueError("order_id must be an integer")

        if record["order_id"] in seen_order_ids:
            raise ValueError(
                f"Duplicate order_id: {record['order_id']}"
            )

        seen_order_ids.add(record["order_id"])

        if not record["customer"].strip():
            raise ValueError("Customer cannot be empty")

        if not record["product"].strip():
            raise ValueError("Product cannot be empty")

        if record["quantity"] <= 0:
            raise ValueError("Quantity must be greater than zero")

        if record["unit_price"] < 0:
            raise ValueError("Unit price cannot be negative")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Validate before writing anything.
    validate_sales(sales)

    fields = [
        "order_id",
        "customer",
        "product",
        "quantity",
        "unit_price",
    ]

    with OUTPUT_FILE.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sales)

    # Store information about this pipeline run.
    metadata = {
        "pipeline": "sales_ingestion",
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(sales),
        "output_file": str(OUTPUT_FILE),
        "status": "success",
    }

    with METADATA_FILE.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(metadata, file, indent=4)

    print("Ingestion completed successfully!")
    print(f"Records written: {len(sales)}")
    print(f"CSV file: {OUTPUT_FILE}")
    print(f"Metadata file: {METADATA_FILE}")


if __name__ == "__main__":
    main()
