
import csv

import pytest

from scripts import transform_sales


def write_input_csv(path, rows):
    fields = [
        "order_id",
        "customer",
        "product",
        "quantity",
        "unit_price",
    ]

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


@pytest.fixture
def setup_files(tmp_path, monkeypatch):
    input_file = tmp_path / "sales.csv"
    output_dir = tmp_path / "processed"
    output_file = output_dir / "sales_clean.csv"

    monkeypatch.setattr(transform_sales, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform_sales, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(transform_sales, "OUTPUT_FILE", output_file)

    return input_file, output_file


def test_valid_sales_are_transformed(setup_files):
    input_file, output_file = setup_files

    write_input_csv(input_file, [
        {
            "order_id": 1001,
            "customer": " Alice ",
            "product": "Laptop",
            "quantity": 2,
            "unit_price": "1200.00",
        }
    ])

    transform_sales.transform_sales()

    with output_file.open(
        newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["customer"] == "Alice"
    assert rows[0]["total_amount"] == "2400.00"


def test_duplicate_order_ids_are_rejected(setup_files):
    input_file, _ = setup_files

    write_input_csv(input_file, [
        {
            "order_id": 1001,
            "customer": "Alice",
            "product": "Laptop",
            "quantity": 1,
            "unit_price": "1200.00",
        },
        {
            "order_id": 1001,
            "customer": "Bob",
            "product": "Mouse",
            "quantity": 1,
            "unit_price": "25.00",
        },
    ])

    with pytest.raises(ValueError, match="Duplicate order ID"):
        transform_sales.transform_sales()


def test_zero_quantity_is_rejected(setup_files):
    input_file, _ = setup_files

    write_input_csv(input_file, [
        {
            "order_id": 1002,
            "customer": "Bob",
            "product": "Mouse",
            "quantity": 0,
            "unit_price": "25.00",
        }
    ])

    with pytest.raises(ValueError, match="Quantity must be positive"):
        transform_sales.transform_sales()


def test_rejects_non_positive_order_id(tmp_path, monkeypatch):
    from scripts import transform_sales

    input_file = tmp_path / "sales.csv"
    output_dir = tmp_path / "processed"

    input_file.write_text(
        "order_id,customer,product,quantity,unit_price\n"
        "0,Alice,Laptop,1,1200.00\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(transform_sales, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform_sales, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(
        transform_sales,
        "OUTPUT_FILE",
        output_dir / "sales_clean.csv",
    )

    import pytest

    with pytest.raises(ValueError, match="Order ID must be positive"):
        transform_sales.transform_sales()


def test_rejects_empty_sales_file(tmp_path, monkeypatch):
    from scripts import transform_sales
    import pytest

    input_file = tmp_path / "sales.csv"
    output_dir = tmp_path / "processed"

    input_file.write_text(
        "order_id,customer,product,quantity,unit_price\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(transform_sales, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform_sales, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(
        transform_sales,
        "OUTPUT_FILE",
        output_dir / "sales_clean.csv",
    )

    with pytest.raises(ValueError, match="no sales records"):
        transform_sales.transform_sales()


def test_rejects_missing_customer(tmp_path, monkeypatch):
    from scripts import transform_sales
    import pytest

    input_file = tmp_path / "sales.csv"
    output_dir = tmp_path / "processed"

    input_file.write_text(
        "order_id,customer,product,quantity,unit_price\n"
        "1001,,Laptop,1,1200.00\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(transform_sales, "INPUT_FILE", input_file)
    monkeypatch.setattr(transform_sales, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(
        transform_sales,
        "OUTPUT_FILE",
        output_dir / "sales_clean.csv",
    )

    with pytest.raises(ValueError, match="Customer and product are required"):
        transform_sales.transform_sales()
