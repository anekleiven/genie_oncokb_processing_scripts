#!/bin/env bash

# This script annotates unique variants with OncoKB annotations
# Requires a locally installed OncoKB annotator as well as a private OncoKB API token. 

# Update these paths to match your setup 
INPUT="data/data_mutations_unique_with_oncotree_maf_ready.txt"
OUTPUT="data/annotated_output.maf"
TOKEN="YOUR_PRIVATE_TOKEN"

# OncoKB annotator execution 
# Assumes your annotator is in the same directory or in your PATH 
python MafAnnotator.py \
-i "$INPUT" \
-o "$OUTPUT" \ 
-b "$TOKEN" 

echo "Annotation Complete. Saved as $OUTPUT."