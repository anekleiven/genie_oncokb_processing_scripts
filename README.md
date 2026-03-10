# GENIE -> OncoKB processing scripts 🤓🤓

This repository contains small Python scripts that prepare AACR Project GENIE-derived variant data for annotation with the OncoKB annotator. The scripts perform common preprocessing steps (mapping tumour types to OncoTree codes, removing duplicate/recurrent variant records, and formatting columns) so the final file(s) match the expectations of an OncoKB annotation pipeline.

The final script includes the instructions for OncoKB annotation. Annotation requires a locally installed OncoKB annotator, as well as a private token from OncoKB. 

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

These scripts are a preprocessing chain — run them in the order below for correct transformation and annotation. 

1. `01_add_oncotree.py` — add or map tumour/tissue type columns to OncoTree codes. This harmonises sample tumour type labels with OncoTree so downstream annotation can use the correct tumour context.
2. `02_deduplicate_variants.py` — remove duplicate or recurrent variants. 
3. `03_prepare_for_oncokb.py` — final formatting step: rename/select columns and output a MAF-like table with the column set expected by the OncoKB annotator.
4. `04_oncokb_annotation.sh` - this shell script executes the locally installed MafAnnotator.py from OncoKB. It passes the processed files from step 3 and interfaces with the OncoKB Web API. 

Check the top of each script for any script-specific requirements.


## Data policy and citations

- AACR Project GENIE data are subject to access controls and a publication policy. Do not share controlled data publicly. Obtain GENIE data only via the official GENIE data access procedures and comply with their terms.
- OncoKB is a separate resource with its own license and citation requirements. When using OncoKB for annotation or publication, follow OncoKB's licensing and citation instructions.

Recommended links:

- AACR Project GENIE: https://www.aacr.org/professionals/research/aacr-project-genie/
- OncoKB: https://www.oncokb.org
