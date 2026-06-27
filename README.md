\# Vietnam Listed Companies Annual Reports PDF Dataset, 2000–2025



This repository provides documentation, metadata, sample index files, and processing scripts for the \*\*Vietnam Listed Companies Annual Reports PDF Dataset, 2000–2025\*\*.



The full PDF dataset is archived on Zenodo and can be cited using the DOI provided below.



\## Dataset Description



This dataset contains annual report PDF files of listed companies on the Vietnamese stock market from 2000 to 2025.



The files are organized by stock ticker. The original file naming format is:



```text

XYZ\_25CN\_BCTN.pdf

XYZ\_19N\_BCTN.pdf

```



Where:



\* `XYZ` is the stock ticker.

\* `25` indicates the report year 2025.

\* `19` indicates the report year 2019.

\* `BCTN` refers to Báo cáo thường niên, meaning Annual Report in Vietnamese.



\## Folder Structure



The original dataset is organized as follows:



```text

full\_data/

├── ACB/

│   ├── ACB\_06N\_BCTN.pdf

│   ├── ACB\_07N\_BCTN.pdf

│   ├── ACB\_20CN\_BCTN.pdf

│   └── ACB\_25CN\_BCTN.pdf

├── CTG/

│   ├── CTG\_10N\_BCTN.pdf

│   ├── CTG\_21CN\_BCTN.pdf

│   └── ...

└── ...

```



\## Dataset Coverage



\* Country: Vietnam

\* Market: Vietnamese listed firms

\* Document type: Annual reports

\* File format: PDF

\* Period: 2000–2025

\* Organization: By stock ticker

\* Dataset version: 1.0.0



\## Full Dataset



The full dataset is available on Zenodo:



\*\*Zenodo DOI:\*\* `to be updated after publication`



After the Zenodo record is published, replace this line with the official DOI, for example:



```text

https://doi.org/10.5281/zenodo.xxxxxxx

```



\## Repository Contents



```text

README.md                 Project overview

CITATION.cff              Citation metadata for GitHub

LICENSE                   License information

data\_dictionary.csv       Description of metadata variables

sample\_index.csv          Small sample of the file index

scripts/                  Python scripts for indexing and packaging data

docs/                     Additional documentation

```



\## Metadata



The full Zenodo dataset includes the following metadata files:



```text

file\_index\_full.csv

checksums\_pdf\_sha256.csv

checksums\_archives\_sha256.csv

coverage\_by\_year.csv

coverage\_by\_period.csv

data\_dictionary.csv

```



The main file is:



```text

file\_index\_full.csv

```



This file includes:



\* stock ticker

\* report year

\* file name

\* relative file path

\* file size

\* SHA256 checksum

\* archive period

\* file status



A small sample is provided in this GitHub repository as:



```text

sample\_index.csv

```



\## Archive Structure on Zenodo



The full PDF dataset is divided into year-based ZIP files:



```text

vn\_bctn\_2000\_2005.zip

vn\_bctn\_2006\_2010.zip

vn\_bctn\_2011\_2015.zip

vn\_bctn\_2016\_2020.zip

vn\_bctn\_2021\_2025.zip

```



\## How to Use



1\. Download the ZIP files from Zenodo.

2\. Extract all ZIP files into the same folder.

3\. Use `file\_index\_full.csv` to locate reports by ticker and year.

4\. Use `checksums\_pdf\_sha256.csv` to verify file integrity.

5\. Use the Python scripts in `scripts/` to rebuild or audit the metadata index.



\## Example Use Cases



This dataset may be useful for:



\* corporate disclosure research

\* accounting and finance research

\* text mining

\* natural language processing

\* ESG disclosure analysis

\* digital transformation disclosure analysis

\* annual report readability analysis

\* Vietnamese stock market research



\## Citation



Please cite the dataset as:



```text

Ngo, P. T. (2026). Vietnam Listed Companies Annual Reports PDF Dataset, 2000–2025 (Version 1.0.0) \[Data set]. Zenodo. https://doi.org/10.5281/zenodo.xxxxxxx

```



The DOI will be updated after the Zenodo record is published.



\## Author



Ngo Phu Thanh

Email: \[thanhnp@uel.edu.vn](mailto:thanhnp@uel.edu.vn)



