# GENIE -> OncoKB processing scripts 🤓🤓

This repository contains small Python scripts that prepare AACR Project GENIE-derived variant data for annotation with the OncoKB annotator. The scripts perform common preprocessing steps (mapping tumour types to OncoTree codes, removing duplicate/recurrent variant records, and formatting columns) so the final file(s) match the expectations of an OncoKB/annotation pipeline.

Important: the GENIE clinical and genomic data used with these scripts are NOT included in this repository. GENIE data are controlled and subject to data access agreements. Run these scripts only on data you are authorized to use.

## Requirements 💻
- Python 3.10+
- R 4.2+

## Setup Instructions 🔧

1. **Create Virtual Environment:**
`python -m venv .venv`
`. .venv/bin/activate`

2. **Install Python Requirements:**
`pip install -r requirements.txt`

## Purpose and workflow 👩🏽‍💻

These scripts are a preprocessing chain — run them in the order below to transform raw GENIE-derived variant tables into MAF-like files suitable for OncoKB annotation.

1. `01_add_oncotree.py` — add or map tumour/tissue type columns to OncoTree codes. This harmonises sample tumour type labels with OncoTree so downstream annotation can use the correct tumour context.
2. `02_deduplicate_variants.py` — remove duplicate or recurrent variants. 
3. `03_prepare_for_oncokb.py` — final formatting step: rename/select columns and output a MAF-like table with the column set expected by the OncoKB annotator.

Check the top of each script for any script-specific arguments or required input column names.

## How these scripts relate to OncoKB

The output of `03_prepare_for_oncokb.py` should be a tabular file with the columns and value formats expected by your OncoKB annotation pipeline or the OncoKB annotator tool. These scripts do not perform annotation themselves — they prepare and normalise the inputs so the OncoKB annotator can run reliably.

## Data policy and citations

- AACR Project GENIE data are subject to access controls and a publication policy. Do not share controlled data publicly. Obtain GENIE data only via the official GENIE data access procedures and comply with their terms.
- OncoKB is a separate resource with its own license and citation requirements. When using OncoKB for annotation or publication, follow OncoKB's licensing and citation instructions.

Recommended links:

- AACR Project GENIE: https://www.aacr.org/professionals/research/aacr-project-genie/
- OncoKB: https://www.oncokb.org
