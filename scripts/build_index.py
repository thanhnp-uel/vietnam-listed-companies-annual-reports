from pathlib import Path
import re
import hashlib
import pandas as pd

PROJECT_ROOT = Path(r"D:\VN_BCTN_PROJECT")
DATA_ROOT = PROJECT_ROOT / "full_data"
META_DIR = PROJECT_ROOT / "metadata"
META_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_filename(file_name: str):
    """
    Nhận diện các dạng tên file phổ biến:

    ACB_06N_BCTN.pdf   -> 2006
    ACB_19N_BCTN.pdf   -> 2019
    ACB_20CN_BCTN.pdf  -> 2020
    ACB_25CN_BCTN.pdf  -> 2025

    Quy ước:
    - XYZ là mã cổ phiếu
    - 06, 07, ..., 25 là năm 2006, 2007, ..., 2025
    - N hoặc CN đều được chấp nhận
    - BCTN là Báo cáo thường niên
    """

    stem = Path(file_name).stem.upper().strip()

    # Chuẩn hóa dấu cách nếu có
    stem = stem.replace(" ", "")

    patterns = [
        # ACB_06N_BCTN hoặc ACB_20CN_BCTN
        r"^([A-Z0-9]{3,10})_(\d{2})(?:C)?N_BCTN",

        # ACB-06N-BCTN hoặc ACB-20CN-BCTN
        r"^([A-Z0-9]{3,10})-(\d{2})(?:C)?N-BCTN",

        # ACB_2025_BCTN nếu sau này có file dạng 4 số
        r"^([A-Z0-9]{3,10})_(20[0-2][0-9])_BCTN",
    ]

    for pattern in patterns:
        match = re.search(pattern, stem)
        if match:
            ticker = match.group(1)

            year_raw = match.group(2)

            if len(year_raw) == 2:
                yy = int(year_raw)

                # Dataset kỳ vọng 2000–2025
                if 0 <= yy <= 25:
                    year_full = 2000 + yy
                else:
                    year_full = None
            else:
                year_full = int(year_raw)

            return ticker, year_full

    return None, None


def assign_period(year_full):
    if pd.isna(year_full):
        return "unknown"

    year_full = int(year_full)

    if 2000 <= year_full <= 2005:
        return "2000_2005"
    elif 2006 <= year_full <= 2010:
        return "2006_2010"
    elif 2011 <= year_full <= 2015:
        return "2011_2015"
    elif 2016 <= year_full <= 2020:
        return "2016_2020"
    elif 2021 <= year_full <= 2025:
        return "2021_2025"
    else:
        return "out_of_scope"


def main():
    rows = []

    # Nhận cả .pdf và .PDF
    pdf_files = [
        p for p in DATA_ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() == ".pdf"
    ]

    for pdf_path in pdf_files:
        folder_ticker = pdf_path.parent.name.upper().strip()
        file_name = pdf_path.name

        ticker_from_file, year_full = parse_filename(file_name)

        relative_path = pdf_path.relative_to(DATA_ROOT).as_posix()
        size_bytes = pdf_path.stat().st_size
        sha256 = sha256_file(pdf_path)

        status = "ok"
        notes = ""

        if ticker_from_file is None or year_full is None:
            status = "needs_review"
            notes = "Filename does not match expected patterns: XYZ_06N_BCTN or XYZ_20CN_BCTN"

        if ticker_from_file and ticker_from_file != folder_ticker:
            status = "needs_review"
            notes = "Ticker in filename differs from folder name"

        archive_period = assign_period(year_full)

        rows.append({
            "record_id": f"{ticker_from_file or folder_ticker}_{year_full or 'unknown'}_{sha256[:8]}",
            "ticker_folder": folder_ticker,
            "ticker_file": ticker_from_file,
            "year_full": year_full,
            "archive_period": archive_period,
            "document_type": "annual_report",
            "file_name": file_name,
            "relative_path": relative_path,
            "file_size_bytes": size_bytes,
            "file_size_mb": round(size_bytes / 1024 / 1024, 2),
            "sha256": sha256,
            "status": status,
            "notes": notes,
        })

    df = pd.DataFrame(rows)

    if len(df) == 0:
        print("No PDF files found.")
        return

    df = df.sort_values(["ticker_folder", "year_full", "file_name"])

    out_index = META_DIR / "file_index_full.csv"
    out_checksum = META_DIR / "checksums_pdf_sha256.csv"
    out_coverage_year = META_DIR / "coverage_by_year.csv"
    out_coverage_period = META_DIR / "coverage_by_period.csv"
    out_needs_review = META_DIR / "needs_review.csv"

    df.to_csv(out_index, index=False, encoding="utf-8-sig")

    df[["sha256", "relative_path", "file_size_bytes"]].to_csv(
        out_checksum,
        index=False,
        encoding="utf-8-sig"
    )

    coverage_year = (
        df.groupby("year_full", dropna=False)
        .agg(
            n_files=("relative_path", "count"),
            n_tickers=("ticker_folder", "nunique"),
            total_size_gb=("file_size_bytes", lambda x: round(x.sum() / 1024**3, 2)),
        )
        .reset_index()
        .sort_values("year_full")
    )
    coverage_year.to_csv(out_coverage_year, index=False, encoding="utf-8-sig")

    coverage_period = (
        df.groupby("archive_period", dropna=False)
        .agg(
            n_files=("relative_path", "count"),
            n_tickers=("ticker_folder", "nunique"),
            total_size_gb=("file_size_bytes", lambda x: round(x.sum() / 1024**3, 2)),
        )
        .reset_index()
        .sort_values("archive_period")
    )
    coverage_period.to_csv(out_coverage_period, index=False, encoding="utf-8-sig")

    needs_review = df[df["status"] != "ok"]
    needs_review.to_csv(out_needs_review, index=False, encoding="utf-8-sig")

    print("=" * 80)
    print("BUILD INDEX COMPLETED")
    print("=" * 80)
    print(f"Total PDF files indexed: {len(df):,}")
    print(f"OK files: {(df['status'] == 'ok').sum():,}")
    print(f"Needs review: {(df['status'] != 'ok').sum():,}")
    print()
    print("Coverage by archive period:")
    print(coverage_period)
    print()
    print(f"Saved: {out_index}")
    print(f"Saved: {out_coverage_period}")
    print(f"Saved: {out_needs_review}")


if __name__ == "__main__":
    main()