# GENIE -> OncoKB processing scripts 🧬🧬

This repository contains small Python scripts that prepare AACR Project GENIE derived variant data for annotation with the OncoKB annotator. The scripts perform common preprocessing steps (mapping tumour types to OncoTree codes, removing duplicate/recurrent variant records, and formatting columns) so the final file(s) match the expectations of an OncoKB annotation pipeline.

The final script includes the instructions for OncoKB annotation. Annotation requires a locally installed OncoKB annotator, as well as a private token from OncoKB. 

Important: the GENIE clinical and genomic data used with these scripts are NOT included in this repository. GENIE data are controlled and subject to data access agreements. Run these scripts only on data you are authorized to use.

## Dataflow 👩🏽‍💻

These scripts are a preprocessing chain — run them in the order below for correct transformation and annotation. 

1. `01_add_oncotree.py`: Map Tumor_Sample_Barcode to OncoTree codes. This harmonises sample tumour type labels with OncoTree so downstream annotation can use the correct tumour context.
2. `02_deduplicate_variants.py`: Remove duplicate or recurrent variants. 
3. `03_prepare_for_oncokb.py`: Rename/select columns and output a MAF-like table with the column set expected by the OncoKB annotator.
4. `04_oncokb_annotation.sh`: Shell script that executes the locally installed MafAnnotator.py from OncoKB. It passes the processed files from step 3 and interfaces with the OncoKB Web API. Requires a private token from OncoKB. 

## Requirements 💻
- Python 3.10+
- R 4.2+

## External Data Requirements 
| File | Source | Used in Script |
| :--- | :--- | :--- |
| `data_clinical_sample.txt` | [GENIE data (requires access from synapse.org), synapse ID: syn68719152](https://www.synapse.org) | `01_add_oncotree.py` |
| `data_mutations_extended.txt` | [GENIE data (requires access from synapse.org), synapse ID: syn68719152](https://www.synapse.org) | `01_add_oncotree.py` |

## External Dependencies 
- OncoKB annotator v.3.4 (MafAnnotator.py):  https://github.com/oncokb/oncokb-annotator/tree/master
  Required for Oncogencity classification of somatic variant data. Used in script `04_oncokb_annotations.sh`

## Setup Instructions 🔧

1. **Clone the repository:**
```
git clone [https://github.com/anekleiven/genie_oncokb_processing_scripts.git](https://github.com/ditt-brukernavn/genie_oncokb_processing_scripts.git)
cd genie_oncokb_processing_scripts

```

2. **Create Virtual Environment:**
`python -m venv .venv`

3. **Activate Virtual Environment:**
`. .venv/bin/activate`

4. **Install Python Requirements:**
`pip install -r requirements.txt`


## Data Policy and Citations

- AACR Project GENIE data are subject to access controls and a publication policy. Do not share controlled data publicly. Obtain GENIE data only via the official GENIE data access procedures and comply with their terms.
- OncoKB is a separate resource with its own license and citation requirements. When using OncoKB for annotation or publication, follow OncoKB's licensing and citation instructions.

## Recommended Sources 🛜

- AACR Project GENIE: https://www.aacr.org/professionals/research/aacr-project-genie/
- Synapse (for access to GENIE data): https://www.synapse.org/
- OncoKB: https://www.oncokb.org
- OncoKB annotator: https://github.com/oncokb/oncokb-annotator

