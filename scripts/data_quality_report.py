
import csv
import json
from decimal import Decimal
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "sales_clean.csv"
REPORT_FILE = PROJECT_ROOT / "data" / "processed" / "data_quality_report.json"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Processed file not found: {INPUT_FILE}")

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    order_ids = [record["order_id"] for record in records]

    duplicate_count = len(order_ids) - len(set(order_ids))
    missing_fields = sum(
        1
        for record in records
        if not record["customer"].strip()
        or not record["product"].strip()
    )

    invalid_amounts = 0
    total_sales = Decimal("0.00")

    for record in records:
        quantity = int(record["quantity"])
        unit_price = Decimal(record["unit_price"])
        total_amount = Decimal(record["total_amount"])

        if quantity <= 0 or unit_price < 0:
            invalid_amounts += 1

        if unit_price * quantity != total_amount:
            invalid_amounts += 1

        total_sales += total_amount

    passed = (
        len(records) > 0
        and duplicate_count == 0
        and missing_fields == 0
        and invalid_amounts == 0
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records_checked": len(records),
        "duplicate_order_ids": duplicate_count,
        "records_with_missing_fields": missing_fields,
        "invalid_amount_checks": invalid_amounts,
        "total_sales": str(total_sales),
        "status": "PASS" if passed else "FAIL",
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))

    if not passed:
        raise SystemExit("Data quality checks failed.")


if __name__ == "__main__":
    main()
