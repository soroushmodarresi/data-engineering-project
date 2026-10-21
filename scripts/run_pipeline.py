
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("Extract sales", "ingestion/extract_sales.py"),
    ("Transform sales", "scripts/transform_sales.py"),
    ("Load SQL Server", "scripts/load_to_sqlserver.py"),
]


def main():
    started_at = datetime.now(timezone.utc)
    print(f"Pipeline started at {started_at.isoformat()}")

    for step_name, script_path in STEPS:
        print(f"\n--- {step_name} ---")

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / script_path)],
            cwd=PROJECT_ROOT,
            check=False,
        )

        if result.returncode != 0:
            print(f"Pipeline failed during: {step_name}")
            raise SystemExit(result.returncode)

    finished_at = datetime.now(timezone.utc)
    print("\nPipeline completed successfully!")
    print(f"Started:  {started_at.isoformat()}")
    print(f"Finished: {finished_at.isoformat()}")


if __name__ == "__main__":
    main()

