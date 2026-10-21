
import csv
from pathlib import Path

import pyodbc

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "sales_clean.csv"

# Replace this with your actual SSMS server name.
SERVER = r".\SQLSERVERSS"
DATABASE = "SalesWarehouse"
DRIVER = "ODBC Driver 18 for SQL Server"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {INPUT_FILE}. "
            "Run transform_sales.py first."
        )

    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("No records to load.")
        return

    with pyodbc.connect(connection_string) as connection:
        cursor = connection.cursor()

        # Avoid duplicate-key errors when this script is run again.
        # Existing order IDs are updated; new ones are inserted.
        for row in rows:
            cursor.execute(
                """
                UPDATE dbo.FactSales
                SET customer = ?,
                    product = ?,
                    quantity = ?,
                    unit_price = ?,
                    total_amount = ?
                WHERE order_id = ?
                """,
                row["customer"],
                row["product"],
                int(row["quantity"]),
                row["unit_price"],
                row["total_amount"],
                int(row["order_id"]),
            )

            if cursor.rowcount == 0:
                cursor.execute(
                    """
                    INSERT INTO dbo.FactSales
                        (order_id, customer, product, quantity,
                         unit_price, total_amount)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    int(row["order_id"]),
                    row["customer"],
                    row["product"],
                    int(row["quantity"]),
                    row["unit_price"],
                    row["total_amount"],
                )

        cursor.execute("SELECT COUNT(*) FROM dbo.FactSales")
        count = cursor.fetchone()[0]

        print(f"Load completed. Warehouse row count: {count}")


if __name__ == "__main__":
    main()
