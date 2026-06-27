from pathlib import Path
import zipfile
import hashlib
import pandas as pd
import shutil

PROJECT_ROOT = Path(r"D:\VN_BCTN_PROJECT")
DATA_ROOT = PROJECT_ROOT / "full_data"
META_DIR = PROJECT_ROOT / "metadata"
OUT_DIR = PROJECT_ROOT / "zenodo_upload"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = META_DIR / "file_index_full.csv"

BLOCKS = [
    ("2000_2005", 2000, 2005),
    ("2006_2010", 2006, 2010),
    ("2011_2015", 2011, 2015),
    ("2016_2020", 2016, 2020),
    ("2021_2025", 2021, 2025),
]


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def make_zip_for_period(df: pd.DataFrame, period_name: str, start_year: int, end_year: int):
    block = df[
        (df["year_full"] >= start_year)
        & (df["year_full"] <= end_year)
        & (df["status"] == "ok")
    ].copy()

    zip_path = OUT_DIR / f"vn_bctn_{period_name}.zip"

    print("=" * 80)
    print(f"Creating archive: {zip_path.name}")
    print(f"Years: {start_year}–{end_year}")
    print(f"PDF files: {len(block):,}")
    print("=" * 80)

    if len(block) == 0:
        print(f"WARNING: No files found for period {period_name}. Empty ZIP will not be created.")
        return {
            "archive_name": zip_path.name,
            "archive_period": period_name,
            "year_start": start_year,
            "year_end": end_year,
            "n_pdf_files": 0,
            "size_bytes": 0,
            "size_gb": 0,
            "sha256": "",
            "status": "empty",
        }

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as zf:
        for _, row in block.iterrows():
            src = DATA_ROOT / row["relative_path"]

            if not src.exists():
                print(f"Missing file: {src}")
                continue

            # Giữ cấu trúc folder theo mã chứng khoán
            arcname = Path("full_data") / row["relative_path"]
            zf.write(src, arcname.as_posix())

    size_bytes = zip_path.stat().st_size

    return {
        "archive_name": zip_path.name,
        "archive_period": period_name,
        "year_start": start_year,
        "year_end": end_year,
        "n_pdf_files": len(block),
        "size_bytes": size_bytes,
        "size_gb": round(size_bytes / 1024**3, 2),
        "sha256": sha256_file(zip_path),
        "status": "ok",
    }


def main():
    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find {INDEX_FILE}. Please run build_index.py first."
        )

    df = pd.read_csv(INDEX_FILE)

    # Ép year_full về numeric để tránh lỗi so sánh kiểu string
    df["year_full"] = pd.to_numeric(df["year_full"], errors="coerce")

    print("=" * 80)
    print("CHECK YEAR DISTRIBUTION BEFORE ARCHIVING")
    print("=" * 80)
    print(df.groupby("year_full").size().sort_index())
    print()

    print("=" * 80)
    print("CHECK PERIOD DISTRIBUTION BEFORE ARCHIVING")
    print("=" * 80)
    print(df.groupby("archive_period").size())
    print()

    archive_rows = []

    for period_name, start_year, end_year in BLOCKS:
        archive_rows.append(
            make_zip_for_period(df, period_name, start_year, end_year)
        )

    archive_df = pd.DataFrame(archive_rows)

    archive_checksum_file = OUT_DIR / "checksums_archives_sha256.csv"
    archive_df.to_csv(
        archive_checksum_file,
        index=False,
        encoding="utf-8-sig"
    )

    # Copy metadata files to Zenodo upload folder
    metadata_files = [
        "file_index_full.csv",
        "checksums_pdf_sha256.csv",
        "coverage_by_year.csv",
        "coverage_by_period.csv",
        "data_dictionary.csv",
        "needs_review.csv",
    ]

    for file_name in metadata_files:
        src = META_DIR / file_name
        if src.exists():
            shutil.copy2(src, OUT_DIR / file_name)

    print("=" * 80)
    print("ZENODO ARCHIVES COMPLETED")
    print("=" * 80)
    print(archive_df)
    print()
    print(f"Saved archive checksums: {archive_checksum_file}")
    print(f"Zenodo upload folder: {OUT_DIR}")


if __name__ == "__main__":
    main()