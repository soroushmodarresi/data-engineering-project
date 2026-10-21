
import subprocess
import sys

from pipeline_logger import get_logger

logger = get_logger("pipeline")

PROJECT_ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent

STEPS = [
    ("Extract sales data", PROJECT_ROOT / "ingestion" / "extract_sales.py"),
    ("Upload raw files to data lake", PROJECT_ROOT / "ingestion" / "upload_to_lake.py"),
    ("Download raw CSV from data lake", PROJECT_ROOT / "ingestion" / "download_from_lake.py"),
    ("Transform sales data", PROJECT_ROOT / "scripts" / "transform_sales.py"),
    ("Load data into SQL Server", PROJECT_ROOT / "scripts" / "load_to_sqlserver.py"),
]
def main():
    logger.info("Pipeline started")

    for step_name, script_path in STEPS:
        logger.info("Starting step: %s", step_name)

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=PROJECT_ROOT,
                check=True
            )
            logger.info("Completed step: %s", step_name)

        except subprocess.CalledProcessError:
            logger.exception("Failed step: %s", step_name)
            raise SystemExit(1)

    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    main()
