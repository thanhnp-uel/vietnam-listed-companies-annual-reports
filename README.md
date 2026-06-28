# Vietnam Listed Companies Annual Reports Dataset (2000–2025)

A structured collection of annual report PDFs for companies listed on the
Vietnamese stock market, spanning 25 years from 2000 to 2025.

**Zenodo DOI:** https://doi.org/10.5281/zenodo.20949551

---

## Overview

This dataset provides annual reports (*Báo cáo thường niên*) published by
Vietnamese listed companies, organized by stock ticker. It is intended for
use in corporate disclosure research, text mining, NLP, ESG analysis, and
Vietnamese capital market studies.

- **Coverage:** Vietnamese listed firms, 2000–2025  
- **Format:** PDF  
- **Organization:** By stock ticker  
- **Version:** 1.0.0  

---

## File Naming Convention

```
{TICKER}_{YY}N_BCTN.pdf       # Standard year (e.g., 2019)
{TICKER}_{YY}CN_BCTN.pdf      # Current-year variant (e.g., 2025)
```

**Examples:**

```
ACB_19N_BCTN.pdf    → ACB annual report, 2019
ACB_25CN_BCTN.pdf   → ACB annual report, 2025
```

---

## Folder Structure

```
full_data/
├── ACB/
│   ├── ACB_06N_BCTN.pdf
│   ├── ACB_07N_BCTN.pdf
│   └── ACB_25CN_BCTN.pdf
├── CTG/
│   ├── CTG_10N_BCTN.pdf
│   └── CTG_21CN_BCTN.pdf
└── ...
```

---

## Getting Started

1. Download the ZIP archives from [Zenodo](https://doi.org/10.5281/zenodo.20949551)
2. Extract all ZIPs into the same directory
3. Use `file_index_full.csv` to locate reports by ticker and year
4. Verify file integrity with `checksums_pdf_sha256.csv`
5. Use the scripts in `scripts/` to rebuild or audit the metadata index

### Archive Files on Zenodo

| Archive | Years |
|---|---|
| `vn_bctn_2000_2005.zip` | 2000–2005 |
| `vn_bctn_2006_2010.zip` | 2006–2010 |
| `vn_bctn_2011_2015.zip` | 2011–2015 |
| `vn_bctn_2016_2020.zip` | 2016–2020 |
| `vn_bctn_2021_2025.zip` | 2021–2025 |

---

## Metadata Files

| File | Description |
|---|---|
| `file_index_full.csv` | Master index: ticker, year, filename, path, size, checksum, status |
| `checksums_pdf_sha256.csv` | SHA-256 checksums for all PDFs |
| `checksums_archives_sha256.csv` | SHA-256 checksums for ZIP archives |
| `coverage_by_year.csv` | Number of reports per year |
| `coverage_by_period.csv` | Number of reports per archive period |
| `data_dictionary.csv` | Variable descriptions for all metadata fields |

A small sample is available in this repository as `sample_index.csv`.

---

## Repository Contents

```
README.md              This file
CITATION.cff           Citation metadata
LICENSE                License information
data_dictionary.csv    Metadata variable descriptions
sample_index.csv       Sample of the file index
scripts/               Python scripts for indexing and packaging
docs/                  Additional documentation
```

---

## Use Cases

- Corporate disclosure research  
- Accounting and finance research  
- Text mining and NLP  
- ESG disclosure analysis  
- Annual report readability studies  
- Digital transformation disclosure research  
- Vietnamese stock market research  

---

## Citation

```bibtex
@dataset{ngo2026vietnam,
  author    = {Ngo, Phu Thanh},
  title     = {Vietnam Listed Companies Annual Reports PDF Dataset, 2000--2025},
  year      = {2026},
  version   = {1.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20949551},
  url       = {https://doi.org/10.5281/zenodo.20949551}
}
```

---

## Author

**Ngo Phu Thanh**  
University of Economics and Law (UEL), Vietnam  
✉ thanhnp@uel.edu.vn