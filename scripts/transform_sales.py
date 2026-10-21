
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "sales.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "sales_clean.csv"


def transform_sales():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_records = []
    seen_order_ids = set()

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        required_fields = {
            "order_id",
            "customer",
            "product",
            "quantity",
            "unit_price",
        }

        if not required_fields.issubset(reader.fieldnames or []):
            raise ValueError("The CSV is missing required columns.")

        for row in reader:
            try:
                order_id = int(row["order_id"])
                quantity = int(row["quantity"])
                unit_price = Decimal(row["unit_price"])
                customer = row["customer"].strip()
                product = row["product"].strip()
            except (ValueError, InvalidOperation, TypeError) as error:
                raise ValueError(
                    f"Invalid data in row: {row}"
                ) from error

            if order_id in seen_order_ids:
                raise ValueError(f"Duplicate order ID: {order_id}")

            if not customer or not product:
                raise ValueError(
                    f"Customer and product are required: {row}"
                )

            if quantity <= 0:
                raise ValueError(
                    f"Quantity must be positive: {row}"
                )

            if not unit_price.is_finite() or unit_price < 0:
                raise ValueError(
                    f"Unit price must be a valid non-negative number: {row}"
                )

            seen_order_ids.add(order_id)
            total_amount = unit_price * quantity

            cleaned_records.append({
                "order_id": order_id,
                "customer": customer,
                "product": product,
                "quantity": quantity,
                "unit_price": f"{unit_price:.2f}",
                "total_amount": f"{total_amount:.2f}",
            })

    fields = [
        "order_id",
        "customer",
        "product",
        "quantity",
        "unit_price",
        "total_amount",
    ]

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(cleaned_records)

    print("Transformation completed successfully!")
    print(f"Rows processed: {len(cleaned_records)}")
    print(f"Output file: {OUTPUT_FILE}")
    print("\nTransformed sales:")

    for record in cleaned_records:
        print(
            f"Order {record['order_id']}: "
            f"{record['product']} x {record['quantity']} "
            f"= ${record['total_amount']}"
        )


if __name__ == "__main__":
    transform_sales()
